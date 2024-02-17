
# apps.py: Modified the BlogConfig class by overriding the ready method to import blog.signals, ensuring signal
# registration upon app startup.

from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        import blog.signals

