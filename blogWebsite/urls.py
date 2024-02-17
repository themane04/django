from django.urls import path

from blog import views
from blog.views import register, home, user_login, user_logout, create_post, post_delete, edit_post, post_detail, \
    edit_profile, like_post
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
                  path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
                  path('profile/', edit_profile, name='edit_profile'),
                  path('like/<int:post_id>', like_post, name='like_post'),
              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)  # This line is added for the purpose of serving media
                                                                        # files during development

# ensuring that the media files are served during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
