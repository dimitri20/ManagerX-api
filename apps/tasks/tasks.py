from celery import shared_task


@shared_task
def send_notification_to_assignee(task):
    print('sending notification to assignee ', task['assign_to'])

