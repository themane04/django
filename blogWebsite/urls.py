from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from blog import views

from blog.views import register, home, user_login, user_logout, create_post, post_delete, edit_post, post_detail, \
    edit_profile, like_post, PostViewSet, mark_notification_read, notifications_all, clear_all_notifications, \
    user_profile, is_loggedin, comment_delete, create_comment

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter(trailing_slash=False)
router.register('posts', PostViewSet)

urlpatterns = [
                  path('', home, name='home'),
                  path('register/', register, name='register'),
                  path('login/', user_login, name='login'),
                  path('logout/', user_logout, name='logout'),
                  path('post/new', create_post, name='create-post'),
                  path('post/delete/<int:post_id>', post_delete, name='post-delete'),
                  path('post/edit/<int:post_id>', edit_post, name='edit-post'),
                  path('post/<int:post_id>', post_detail, name='post_detail'),
                  path('comment/<int:comment_id>/delete/', comment_delete, name='comment-delete'),
                  path('post/<int:post_id>/comment/create/', create_comment, name='comment-create'),
                  path('profile/', edit_profile, name='edit_profile'),
                  path('view-profile/', user_profile, name='user_profile'),
                  path('like/<int:post_id>', like_post, name='like_post'),
                  #path('api/', include(router.urls)),
                  #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('notification/<int:notification_id>/read/', mark_notification_read,
                       name='mark_notification_read'),
                  path('notifications/', notifications_all, name='notifications_all'),
                  path('clear-notifications/', clear_all_notifications, name='clear_notifications'),
                  path('is-loggedin/', is_loggedin, name='is_loggedin')
              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)  # This line is added for the purpose of serving media
# files during development

# ensuring that the media files are served during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
