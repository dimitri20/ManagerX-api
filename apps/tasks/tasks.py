from asgiref.sync import async_to_sync
from celery import shared_task
from apps.notifications.models import Notification


@shared_task
def send_notification_to_assignee(task):
    pass
