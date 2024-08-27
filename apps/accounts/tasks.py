from venv import create

from celery import shared_task
from django.contrib.auth import get_user_model

from apps.expertiseMainFlow.backup.drive import create_shared_folder_for_user
from apps.expertiseMainFlow.models import SharedRootFolderData

User = get_user_model()

@shared_task
def create_shared_folder_for_user_task(user_id):
    user = User.objects.get(pk=user_id)
    created_folder = create_shared_folder_for_user(user)
    if created_folder:
        shared_folder = SharedRootFolderData(
            user=user,
            drive_folder_id=created_folder['drive_folder_id'],
            drive_folder_name=created_folder['drive_folder_name'],
        )
        shared_folder.save()
        print(f"folder created successfully for user {user}", created_folder)
