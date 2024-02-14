from django.contrib import admin
from django.urls import path
from blog.views import register, index, user_login

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
]
