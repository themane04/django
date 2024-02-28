"""
The function add_notification_to_context is designed to be used as a context processor in a Django project. Its purpose
is to add notification-related data to the context of each template rendering process, provided the user
is authenticated.
"""


def add_notification_to_context(request):
    if request.user.is_authenticated:
        unread_notifications = request.user.received_notifications.filter(is_read=False)
        unread_count = unread_notifications.count()
        return {
            'notifications': unread_notifications,
            'unread_count': unread_count
        }
    return {}
