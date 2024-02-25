from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST, require_http_methods
from .forms import UserRegisterForm, PostForm, CommentForm, ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Post, Comment, Notification
from rest_framework import viewsets
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy


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


# function that marks a notification as read
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, receiver=request.user)
    notification.is_read = True
    notification.save()
    return redirect('post_detail', post_id=notification.post.id)


# function that clears all notifications
@login_required
def clear_all_notifications(request):
    request.user.received_notifications.all().delete()
    return redirect('notifications_all')


# function that handles the creation of a new comment
@receiver(post_save, sender=Comment)
def create_notification(sender, instance, created, **kwargs):
    if created and instance.author != instance.post.author:
        Notification.objects.create(
            post=instance.post,
            sender=instance.author,
            receiver=instance.post.author,
            notification_type=Notification.COMMENT,
            is_read=False
        )


# class that handles the creation of a new post
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


# class that handles the registration of a new user
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        return render(request, 'users/register.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/login.html', {'error': None})

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        context = {'error': None}
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            context['error'] = 'Invalid email or password.'
            return render(request, 'users/login.html', context)

        user = authenticate(username=user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context['error'] = 'Invalid email or password.'
            return render(request, 'users/login.html', context)


# class that handles the profile page of a user
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class CreatePostView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(request, 'users/create_post.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
        return render(request, 'users/create_post.html', {'form': form})


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


# class that allows a user to edit a post
class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'users/edit_post.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
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
            return redirect('post_detail', post_id=post.id)
        return self.get(request, *args, **kwargs)


# class that allows a user to delete a comment
class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.author or request.user == comment.post.author:
            if hasattr(comment, 'image') and comment.image:
                comment.image.delete()
            comment.delete()
            return redirect('post_detail', post_id=comment.post.id)
        else:
            return HttpResponseForbidden('You do not have permission to delete this comment.')


# function that allows a user to edit his profile information
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
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')

            # Re-authenticate the user to update session information if necessary
            updated_user = authenticate(username=user_form.cleaned_data['username'], password=request.user.password)
            if updated_user:
                auth_login(request, updated_user)
            return redirect('edit_profile')
        return render(request, 'users/profile_information.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })


# class that allows a user to create a comment
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
        context['unread_count'] = self.get_queryset().filter(is_read=False).count()
        return context


@method_decorator(require_POST, name='dispatch')
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        liked = False

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
