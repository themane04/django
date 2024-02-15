from django.urls import path
from blog.views import register, home, user_login, user_logout, create_post, post_delete, edit_post, post_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('post/new', create_post, name='create-post'),
    path('post/delete/<int:post_id>', post_delete, name='post-delete'),
    path('post/edit/<int:post_id>', edit_post, name='edit-post'),
    path('post/<int:post_id>', post_detail, name='post_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
