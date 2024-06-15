from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        new_notifications_count = Notification.objects.filter(is_read=False, project__handling_officer=request.user).count()
    else:
        new_notifications_count = 0
    return {'new_notifications_count': new_notifications_count}
