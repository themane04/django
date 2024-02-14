from django.contrib import admin
from django.urls import path
from blog.views import register, index, login

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]
