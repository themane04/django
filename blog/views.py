import logging

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
@csrf_exempt
@login_required
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    return render(request, 'users/create_post.html', {'form': form})


# function that allows a user to delete a post
@csrf_exempt
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponse()
    post.image.delete()
    post.delete()
    return redirect('home')


# function that allows a user to edit a post
@csrf_exempt
@login_required
# @require_http_methods(['PUT', 'PATCH'])
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)
    if request.user != post.author:
        return redirect('home')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'users/edit_post.html', {'form': form})


# function that allows a user to view and comment a post
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all().order_by('-created_at')
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', post_id=post_id)  # Redirect to the same page to display the new comment
    else:
        comment_form = CommentForm()
    return render(request, 'users/post_detail.html',
                  {'post': post, 'comments': comments, 'comment_form': comment_form})


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user == comment.post.author:
        if comment.image:
            comment.image.delete()
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
    else:
        return redirect('post_detail', post_id=comment.post.id)


# function that allows a user to like a post
@require_POST
def like_post(request, post_id):
    if not request.user.is_authenticated:
        # Return a 403 Forbidden response for unauthenticated users
        return JsonResponse({'error': 'You must be logged in to like a post.'}, status=403)

    post = get_object_or_404(Post, id=post_id)
    liked = not post.likes.filter(id=request.user.id).exists()
    if liked:
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)

    return JsonResponse({
        'liked': liked,
        'like_count': post.likes.count()
    })


# function that allows a user to edit his profile information
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')

            updated_user = authenticate(username=user_form.cleaned_data['username'], password=request.user.password)
            if updated_user:
                auth_login(request, updated_user)
            return redirect('edit_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile_information.html', context)


def user_profile(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'users/user_profile.html', {'user_posts': user_posts})


@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.image = form.cleaned_data.get('image')
            new_comment.save()

            # Notification logic
            if post.author != request.user:
                Notification.objects.create(post=post, sender=request.user, receiver=post.author,
                                            notification_type=Notification.COMMENT)

            # Redirect to the same page to display the new comment, or wherever appropriate
            return redirect(post.get_absolute_url())  # Assuming your Post model has a get_absolute_url method
        else:
            # If the form is not valid, render the form with error messages (or handle as needed)
            return render(request, 'users/post_detail.html', {'form': form, 'post': post})
    else:
        form = CommentForm()  # An unbound form

    # If GET request, you might want to show an empty form or redirect
    # Adjust the 'your_template.html' and context as needed
    return render(request, 'users/post_detail.html', {'form': form, 'post': post})


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


def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, receiver=request.user)
    notification.is_read = True
    notification.save()
    return redirect('post_detail', post_id=notification.post.id)


def notifications_all(request):
    notifications = Notification.objects.filter(receiver=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'users/user_notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


@login_required
def clear_all_notifications(request):
    request.user.received_notifications.all().delete()
    return redirect('notifications_all')


@login_required
@require_POST
def like_post(request, post_id):
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
