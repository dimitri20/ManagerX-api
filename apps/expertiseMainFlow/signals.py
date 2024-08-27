from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.expertiseMainFlow.models import ExpertiseFolder, File
from apps.expertiseMainFlow.tasks import create_folder_on_drive_task, upload_file_to_google_drive_task
from apps.notifications.models import Notification


@receiver(post_save, sender=ExpertiseFolder)
def create_folder_on_drive_signal(sender, instance, created, **kwargs):
    if created:
        folder_id = instance.uuid
        try:
            create_folder_on_drive_task.delay(folder_id)
            print(f"Google folder creation triggered for folder ID: {folder_id}")
        except Exception as e:
            print(f"Failed to create Google folder for folder ID: {folder_id}. Error: {e}")

@receiver(post_save, sender=File)
def upload_file_to_drive_signal(sender, instance, created, **kwargs):
    if created:
        file_id = instance.uuid
        upload_file_to_google_drive_task.delay(file_id)
