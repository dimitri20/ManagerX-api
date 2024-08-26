from celery import shared_task
from django.contrib.auth import get_user_model

from apps.expertiseMainFlow.backup.drive import create_shared_folder_for_user

User = get_user_model()

@shared_task
def create_shared_folder_for_user_task(user_id):
    user = User.objects.get(pk=user_id)
    created_folder = create_shared_folder_for_user(user)
    if created_folder:
        print(f"folder created successfully for user {user}", created_folder)