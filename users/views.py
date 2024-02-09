from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login



def signup_view(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'auth/login_signup.html', {'form': form})


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('/')
    return render(request, 'auth/login_signup.html', {'form': form})
