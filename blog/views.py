from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, PostForm, CommentForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Post, Comment


def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # message from django to display a message to the user after the registration is successful
            messages.success(request, f'Account created for {form.cleaned_data['username']}!')
            return redirect('home')
    return render(request, 'users/register.html', {'form': form})


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


def user_logout(request):
    request.session.flush()
    return redirect('home')


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


#
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'users/create_post.html', {'form': form})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponse()
    post.delete()
    return redirect('home')


@login_required
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


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'users/post_detail.html', {'post': post, 'form': form})


# def submit_comment(request, post_id):
#     if request.method == 'POST':
#         comment_text = request.POST.get('comment_text')
#         post_id = request.POST.get('post_id')
#         if comment_text and post_id:
#             post = Post.objects.get(id=post_id)
#             Comment.objects.create(post=post, author=request.user, content=comment_text)
#     return redirect('home')


def clean_username(self):
    username = self.cleaned_data.get("username")
    if User.objects.filter(username=username).exists():
        raise ValidationError("A user with that username already exists.")
    return username


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        else:
            u_form = UserRegisterForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request, 'users/profile.html', context)

