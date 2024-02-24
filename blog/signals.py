# signals.py: Created to define signal receivers that listen for the post_save event of the User model.
# When a user is saved, it either creates a new profile (if the user is newly created) or updates an existing one.

from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.apps import apps
from django.core.exceptions import ValidationError


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile = apps.get_model('blog', 'Profile')
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# This signal handler might not work as intended since apps.get_model('auth', 'User') can't be used with @receiver
@receiver(pre_save, sender=User)  # Directly using User model for simplicity
def check_email_uniqueness(sender, instance, **kwargs):
    if instance and instance.email:
        User = apps.get_model('auth', 'User')  # Correct usage inside the function
        if User.objects.filter(email=instance.email).exclude(pk=instance.pk).exists():
            raise ValidationError("A user with that email already exists.")
