from celery import shared_task
from django.contrib.auth import get_user_model

from apps.expertiseMainFlow.models import File, ExpertiseFolder
from apps.notifications.models import Notification
from apps.expertiseMainFlow.backup.gcs import upload_file_to_gcs, upload_file_to_drive
from apps.notifications.tasks import send_notification
from .backup.drive import create_folder, get_folder_by_name, upload_file, check_if_folder_exists_on_drive

User = get_user_model()


@shared_task
def create_folder_on_drive_task(folder_id):
    folder = ExpertiseFolder.objects.get(pk=folder_id)
    parent_folder_id = get_folder_by_name(folder.owner.username)
    created_folder_id = create_folder(folder.title, parent_folder_id=parent_folder_id)
    print(f"created folder {created_folder_id}")


@shared_task
def upload_file_to_google_drive_task(file_id):
    # TODO - create folder if not exists
    file_instance = File.objects.get(pk=file_id)
    print()
    upload_file(file_instance.title, file_instance.file.path, file_instance.folder.get_drive_folder_id())


@shared_task
def upload_file_to_google_cloud(file_id):
    try:
        file_instance = File.objects.get(pk=file_id)

        # Get the file's path on the server
        source_file_name = file_instance.file.name
        source_file_path = file_instance.file.path

        print(source_file_name)
        print(source_file_path)

        upload_file_to_gcs(source_file_path, source_file_name)

        # create notification for user
        notification = Notification(
            initiator=file_instance.owner,
            receiver=file_instance.owner,
            title="File uploaded to Google Cloud Successfully",
            message=f"Now You can open and edit uploaded file",
            level=Notification.Level.SUCCESS
        )
        notification.save()

        send_notification.delay(notification.uuid)
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")

