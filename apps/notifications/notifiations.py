from .models import Notification
from .tasks import send_notification

def notify_user(title, message, initiator, receiver, level):
    notification = Notification(
        initiator=initiator,
        receiver=receiver,
        title=title,
        message=message,
        level=level
    )
    notification.save()

    send_notification.delay(notification.uuid)
