def add_notification_to_context(request):
    if request.user.is_authenticated:
        notifications = request.user.received_notifications.filter(is_read=False)
        return {'notifications': notifications}
    return {}
