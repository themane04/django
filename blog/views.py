import json
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from rest_framework import viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import UserRegisterForm, PostForm, CommentForm, ProfileUpdateForm, UserUpdateForm
from .models import Post, Comment, Notification, Profile
from .serializers import PostSerializer


# function that handles the creation of a new comment
@receiver(post_save, sender=Comment)
def create_notification(sender, instance, created, **kwargs):
    with transaction.atomic():
        if created and instance.author != instance.post.author:
            Notification.objects.create(
                post=instance.post,
                sender=instance.author,
                receiver=instance.post.author,
                notification_type=Notification.COMMENT,
                is_read=False
            )


# function that checks if a user is logged in
def is_loggedin(request):
    if not request.user.is_authenticated:
        return redirect('login')


# function that handles the logout of a user
@csrf_exempt
def user_logout(request):
    request.session.flush()
    return redirect('home')


# function that handles the home page of the website
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


# function that handles the profile page of a user
def user_profile(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'users/user_profile.html', {'user_posts': user_posts})


# function that handles the public profile page of a user
def user_public_profile(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    posts = Post.objects.filter(author=user_profile.user)
    return render(request, 'user_public_profile.html', {'profile_user': user_profile.user, 'posts': posts})


# class that handles the creation of a new post
class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


# class that handles the registration of a new user
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = User.objects.create_user(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password1']
            )
            user.save()
            return JsonResponse({"success": "User created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        # Parse the JSON body of the request
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:
            # Authenticate the user
            user = authenticate(request, username=User.objects.get(email=email).username, password=password)
            if user is not None:
                # User is authenticated, log them in
                login(request, user)

                # Retrieve or create the token for the user
                refresh = RefreshToken.for_user(user)

                # Return a successful response with the token
                return Response({"access": str(refresh.access_token)}, status=200)
            else:
                # Authentication failed
                return JsonResponse({"error": "Invalid email or password"}, status=400)
        except User.DoesNotExist:
            # No user found with the provided email
            return JsonResponse({"error": "Invalid email or password"}, status=400)


# class that allows a user to create a new post
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class CreatePostView(APIView):
    print('CreatePostView')

    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(request, 'home.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
        return render(request, 'home.html', {'form': form})


# class that allows a user to delete a post
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class PostDeleteView(View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            return HttpResponse(status=403)  # Forbidden access
        post.image.delete()
        post.delete()
        return redirect('home')

    def delete(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)

        if post.author != request.user:
            # Forbidden access, user is not the author of the post
            return JsonResponse({'error': 'You do not have permission to delete this post'}, status=403)

        # If the post has an associated image, delete it as well
        if post.image:
            post.image.delete()

        post.delete()
        # For an API view, instead of redirecting, return a JSON response indicating success
        return JsonResponse({'message': 'Post deleted successfully'}, status=204)


# class that allows a user to edit a post
@method_decorator(csrf_exempt, name='dispatch')
class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'users/edit_post.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if 'remove_image' in self.request.POST:
            self.object = form.save(commit=False)
            self.object.image.delete()
            self.object.image = None
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# class that allows a user to view and comment a post
class PostDetailView(DetailView):
    model = Post
    template_name = 'users/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.all().order_by('-created_at')
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post-detail', post_id=post.id)
        return self.get(request, *args, **kwargs)


# class that allows a user to delete a comment
@method_decorator(csrf_exempt, name='dispatch')
class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.author or request.user == comment.post.author:
            if hasattr(comment, 'image') and comment.image:
                comment.image.delete()
            comment.delete()
            return redirect('post-detail', post_id=comment.post.id)
        else:
            return HttpResponseForbidden('You do not have permission to delete this comment.')

    def delete(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=comment_id)

        # Check if the request user is the author of the comment or an admin
        if request.user == comment.author or request.user.is_superuser:
            comment.delete()
            return JsonResponse({'message': 'Comment successfully deleted'}, status=204)
        else:
            # If the user does not have permission to delete the comment
            return JsonResponse({'error': 'You do not have permission to delete this comment'}, status=403)


# function that allows a user to edit his profile information
@method_decorator(csrf_exempt, name='dispatch')
class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'users/profile_information.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            # Check if there are changes in the forms
            user_changed = user_form.has_changed()
            profile_changed = profile_form.has_changed()

            if user_changed or profile_changed:
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile has been updated!')

                # Optionally re-authenticate or update the session, if needed
                # This section may need adjustment as per your authentication flow

                return redirect('edit_profile')
            else:
                messages.info(request, 'No changes were made to your profile.')

        return render(request, 'users/profile_information.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })


# class that allows a user to delete his profile
@method_decorator(csrf_exempt, name='dispatch')
class DeleteProfileView(LoginRequiredMixin, View):
    template_name = 'users/confirm_delete.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'Your profile was successfully deleted.')
        return redirect('home')


# class that allows a user to create a comment
@method_decorator(csrf_exempt, name='dispatch')
class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.image = form.cleaned_data.get('image')
            new_comment.save()

            if post.author != request.user:
                notification_exists = Notification.objects.filter(
                    post=post,
                    sender=request.user,
                    receiver=post.author,
                    notification_type=Notification.COMMENT
                ).exists()
                if not notification_exists:
                    Notification.objects.create(
                        post=post, sender=request.user, receiver=post.author,
                        notification_type=Notification.COMMENT
                    )

            return redirect(post.get_absolute_url())
        else:
            return render(request, 'users/post_detail.html', {'form': form, 'post': post})

    def get(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm()
        return render(request, 'users/post_detail.html', {'form': form, 'post': post})


class NotificationsAllView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'users/user_notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.user.received_notifications.filter(is_read=False).update(is_read=True)
        context['unread_count'] = 0
        return context


# function that marks a notification as read
@method_decorator(csrf_exempt, name='dispatch')
class MarkNotificationReadView(LoginRequiredMixin, View):
    def post(self, request, notification_id, *args, **kwargs):
        notification = get_object_or_404(Notification, pk=notification_id, receiver=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'message': 'Notification marked as read', 'post_id': notification.post.id}, status=200)


# function that clears all notifications
@method_decorator(csrf_exempt, name='dispatch')  # Consider CSRF protection strategy for your case
class ClearAllNotificationsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request.user.received_notifications.all().delete()
        return JsonResponse({'message': 'All notifications cleared successfully'}, status=200)


@method_decorator(require_POST, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        like_count = post.likes.count()

        if liked and user != post.author:
            notification_exists = Notification.objects.filter(
                sender=user,
                receiver=post.author,
                post=post,
                notification_type=Notification.LIKE,
            ).exists()

            if not notification_exists:
                Notification.objects.create(
                    post=post,
                    sender=user,
                    receiver=post.author,
                    notification_type=Notification.LIKE,
                    is_read=False
                )

        return JsonResponse({
            'liked': liked,
            'like_count': like_count,
        })
