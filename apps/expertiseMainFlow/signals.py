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
            instance.owner.notify("Folder synced with drive", "google folder created", initiator=instance.owner, level=Notification.Level.SUCCESS)
            print(f"Google folder creation triggered for folder ID: {folder_id}")
        except Exception as e:
            print(f"Failed to create Google folder for folder ID: {folder_id}. Error: {e}")

@receiver(post_save, sender=File)
def upload_file_to_drive_signal(sender, instance, created, **kwargs):
    #TODO
    pass
    # if created:
    #     file_id = instance.uuid
    #     try:
    #         upload_file_to_google_drive_task.delay(instance.uuid)
    #         instance.owner.notify("File synced with drive", "google file uploaded successfully", initiator=instance.owner, level=Notification.Level.SUCCESS)
    #         print(f"Google folder creation triggered for folder ID: {file_id}")
    #     except Exception as e:
    #         print(f"Failed to create Google folder for folder ID: {file_id}. Error: {e}")
