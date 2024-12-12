def notifications(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications': request.user.notification_set.filter(is_read=False).count()
        }
    return {'unread_notifications': 0}