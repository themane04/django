from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import UserRegisterForm, PostForm, CommentForm
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
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
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


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()  # Model has a related_name='comments' in the ForeignKey of Comment model
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post  # Assuming your Comment model has a 'post' ForeignKey to Post
            new_comment.author = request.user  # Assuming your Comment model has an 'author' ForeignKey to User
            new_comment.save()
            return redirect('post_detail', post_id=post_id)  # Redirect to the same page to display the new comment
    else:
        comment_form = CommentForm()
    return render(request, 'users/post_detail.html',
                  {'post': post, 'comments': comments, 'comment_form': comment_form})


def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = comment.post
    if request.user.is_authenticated and request.user == post.author:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect(reverse('post_detail', args=[post.id]))
    else:
        return HttpResponseForbidden()
