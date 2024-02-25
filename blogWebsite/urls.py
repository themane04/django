from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import RegisterView, home, UserLoginView, user_logout, CreatePostView, PostDeleteView, EditPostView, \
    PostDetailView, EditProfileView, LikePostView, PostViewSet, mark_notification_read, NotificationsAllView, \
    clear_all_notifications, user_profile, is_loggedin, CommentDeleteView, CreateCommentView, user_public_profile, \
    DeleteProfileView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter(trailing_slash=False)
router.register('posts', PostViewSet)

urlpatterns = [
                  # path('api/', include(router.urls)),
                  # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('', home, name='home'),
                  path('logout/', user_logout, name='logout'),
                  path('view-profile/', user_profile, name='user_profile'),
                  path('notification/<int:notification_id>/read/', mark_notification_read,
                       name='mark_notification_read'),
                  path('clear-notifications/', clear_all_notifications, name='clear_notifications'),
                  path('is-loggedin/', is_loggedin, name='is_loggedin'),
                  path('profile/<str:username>/', user_public_profile, name='user_public_profile'),
                  path('register/', RegisterView.as_view(), name='register'),
                  path('login/', UserLoginView.as_view(), name='login'),
                  path('post/new', CreatePostView.as_view(), name='create-post'),
                  path('post/delete/<int:post_id>', PostDeleteView.as_view(), name='post-delete'),
                  path('post/edit/<int:post_id>', EditPostView.as_view(), name='edit-post'),
                  path('post/<int:post_id>', PostDetailView.as_view(), name='post-detail'),
                  path('comment/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
                  path('post/<int:post_id>/comment/create/', CreateCommentView.as_view(), name='comment-create'),
                  path('profile/', EditProfileView.as_view(), name='edit_profile'),
                  path('delete-profile/', DeleteProfileView.as_view(), name='delete-profile'),
                  path('like/<int:post_id>', LikePostView.as_view(), name='like_post'),
                  path('notifications/', NotificationsAllView.as_view(), name='notifications_all'),
              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)  # This line is added for the purpose of serving media
# files during development

# ensuring that the media files are served during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
