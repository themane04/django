"""
URL configuration for bennote project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path, include
from .views import home
from users.views import login_view, signup_view
from rest_framework.routers import DefaultRouter
from notes.views import NoteViewSet

router = DefaultRouter(trailing_slash=False)
router.register('notes', NoteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='Home'),
    path('notes/', include('notes.urls')),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('api/', include(router.urls)),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
