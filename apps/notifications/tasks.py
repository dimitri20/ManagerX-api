import logging

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

logger = logging.getLogger(__name__)

@shared_task
def send_notification(notification_id):
    notification = Notification.objects.get(pk=notification_id)
    logger.info(notification)
    logger.info("send_notification task is running.")

    channel_layer = get_channel_layer()
    group_name = f'notifications_{notification.receiver.id}'
    print(f"group name notification_tasks.py is {group_name}")
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "title": notification.title,
            "message": notification.message,
            "level": notification.level,
        }
    )