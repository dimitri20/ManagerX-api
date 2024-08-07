# myapp/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Task


@shared_task
def check_task_deadlines():
    today = timezone.now().date()
    tasks = Task.objects.filter(deadline__lte=today, is_notified=False)
    for task in tasks:
        # Implement your notification logic here
        send_notification(task)  # Example function to send notification

        # Update the task to prevent further notifications
        task.save()


def send_notification(task):
    # Your notification logic here (e.g., sending an email)
    print(f"Sending notification for task: {task.title}")
