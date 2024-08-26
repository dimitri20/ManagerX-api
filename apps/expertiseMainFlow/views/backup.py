from rest_framework import status
from rest_framework.views import APIView

from rest_framework.response import Response

from apps.expertiseMainFlow.backup.drive import create_shared_folder_for_each_user
from apps.expertiseMainFlow.serializers import SharedFolderDataSerializer
from apps.notifications.models import Notification
from apps.expertiseMainFlow.tasks import send_notification

class CreateUserFoldersOnDrive(APIView):

    def post(self, request, *args, **kwargs):

        created_folders = create_shared_folder_for_each_user()
        serializer = SharedFolderDataSerializer(data=created_folders, many=True)

        if serializer.is_valid():
            # Bulk create instances
            shared_folder_data_instances = serializer.save()

            notification = Notification(
                initiator=self.request.user,
                receiver=self.request.user,
                title="Your working folder shared with you on google drive",
                message=f"Now you can edit files from workplace or modify them from drive",
                level=Notification.Level.SUCCESS
            )
            notification.save()

            send_notification.delay(notification.uuid)

            # Return the created instances
            return Response(SharedFolderDataSerializer(shared_folder_data_instances, many=True).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


