from django.contrib import admin
from django.urls import path
from blog.views import register, home, user_login, user_logout

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
