from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.http import require_POST, require_http_methods
from .forms import UserRegisterForm, PostForm, CommentForm, ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Post, Comment, Notification
from rest_framework import viewsets
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


# function that handles the registration of a new user
@csrf_exempt
def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # message from django to display a message to the user after the registration is successful
            messages.success(request, f'Account created for {form.cleaned_data['username']}!')
            return redirect('login')
    return render(request, 'users/register.html', {'form': form})


# function that handles the login of a user
@csrf_exempt
def user_login(request):
    context = {'error': None}
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
            context['error'] = 'Invalid email or password.'
        if user is not None:
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    return render(request, 'users/login.html', context)


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
    comments = post.comments.all()  # Model has a related_name='comments' in the ForeignKey of Comment model
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
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
    else:
        return redirect('post_detail', post_id=comment.post.id)


# function that allows a user to like a post
@login_required
@require_POST
def like_post(request, post_id):
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


# function that allows a user to delete a comment
@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = comment.post
    if request.user == comment.author or request.user == post.author:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect(reverse('post_detail', args=[post.id]))
    else:
        return HttpResponseForbidden()


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
            return redirect('edit_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile.html', context)


def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        comment_content = request.POST.get('comment_content')
        Comment.objects.create(post=post, author=request.user, content=comment_content)
        if post.author != request.user:
            Notification.objects.create(post=post, sender=request.user, receiver=post.author,
                                        notification_type=Notification.COMMENT)
        # Redirect or return a response


def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, receiver=request.user)
    notification.is_read = True
    notification.save()
    return redirect('some_view_for_details')
