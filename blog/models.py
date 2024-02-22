from django.db import models
from django.contrib.auth.models import User


# A model for the posts that will be created by the users
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='post_likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# A model for the comments that will be created by the users
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


# A model for the user profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/')
    bio = models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'


class Notification(models.Model):
    # Types of notifications
    COMMENT = 'comment'
    LIKE = 'like'
    # More types can be added as needed

    NOTIFICATION_TYPES = [
        (COMMENT, 'Comment'),
        (LIKE, 'Like'),
    ]

    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'From {self.sender} to {self.receiver} about {self.post}'
