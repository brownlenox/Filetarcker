from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser or (hasattr(user, 'userprofile') and user.userprofile.role == 'director'):
            # Count unread notifications for admin/director only
            new_notifications_count = Notification.objects.filter(is_read_by_admin=False)
        else:
            # Count unread notifications for handling officers
            new_notifications_count = Notification.objects.filter(is_read_by_handling_officer=False, project__handling_officer=user).count()
    else:
        new_notifications_count = 0
    return {'new_notifications_count': new_notifications_count}
