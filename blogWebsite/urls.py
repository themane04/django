from django.contrib import admin
from django.urls import path
from blog.views import register, index, user_login, custom_logout_view

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', custom_logout_view, name='logout'),
]
