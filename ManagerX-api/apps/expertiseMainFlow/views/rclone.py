import json
import os
import requests
import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.parsers import MultiPartParser, FormParser

from ..backup.drive import move_folder, rename_folder, share_folder_or_file_with_user
from ..models import ExpertiseData
from ..rclone.endpoints import RcloneOperations
from ..rclone.rclone import Rclone
from ..serializers.rclone_request_serializers import ListRemoteRequestSerializer, BaseRemoteRequestSerializer, \
    MoveFileRequestSerializer, PublicLinkRequestSerializer, FileUploadSerializer, GenerateConclusionRequestSerializer, \
    ShareFolderRequestSerializer
from ..serializers.rclone_response_serializers import ListRemoteResponseSerializer, PublicLinkResponseSerializer
from ...accounts.models import UserAccount

from ...notifications.models import Notification
from ...tasks.models import Task

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ListRemoteView(APIView):
    """
        API View for creating a directory using Rclone.

        Rclone docs:

        operations/list: List the given remote and path in JSON format
            This takes the following parameters:

            fs - a remote name string e.g. "drive:"
            remote - a path within that remote e.g. "dir"
            opt - a dictionary of options to control the listing (optional)
                recurse - If set recurse directories
                noModTime - If set return modification time
                showEncrypted - If set show decrypted names
                showOrigIDs - If set show the IDs for each item if known
                showHash - If set return a dictionary of hashes
                noMimeType - If set don't show mime types
                dirsOnly - If set only show directories
                filesOnly - If set only show files
                metadata - If set return metadata of objects also
                hashTypes - array of strings of hash types to show if showHash set

            Returns:
            list

            This is an array of objects as described in the lsjson command
            See the lsjson[https://rclone.org/commands/rclone_lsjson/] command for more information on the above and examples.
    """

    @swagger_auto_schema(request_body=ListRemoteRequestSerializer)
    def post(self, request, *args, **kwargs):
        # Instantiate the Rclone object
        rclone_instance = Rclone()

        # Configure the Rclone instance using the builder pattern and execute the operation
        response = (
            rclone_instance
            .set_operation(RcloneOperations.OPERATIONS_LIST)
            .set_request_serializer(ListRemoteRequestSerializer)
            .set_response_serializer(ListRemoteResponseSerializer)
            .execute(request.data)
        )

        return response


class UploadFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        request_body=FileUploadSerializer,  # Serializer defines the structure of the request
    )
    def post(self, request):
        # Use the serializer to validate the incoming data
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            # Extract validated data
            fs = serializer.validated_data['fs']
            remote = serializer.validated_data['remote']
            file = serializer.validated_data['file']


            files = {
                'file': request.FILES['file'],
            }
            data = {
                'fs': fs,
                'remote': remote,
            }

            # Instantiate the Rclone object
            rclone_instance = Rclone()

            (rclone_instance
            .set_operation(RcloneOperations.OPERATIONS_UPLOAD_FILE)
            .set_request_serializer(BaseRemoteRequestSerializer)  # Ensure this is the correct serializer for the request
            .set_response_serializer(serializers.Serializer))

            return rclone_instance.execute(data=data, files=files)


class RcloneMkDirView(APIView):
    """
    API View for creating a directory using Rclone.

    Rclone docs:

    operations/mkdir: Make a destination directory or container

        This takes the following parameters:
            fs - a remote name string e.g. "drive:"
            remote - a path within that remote e.g. "dir"
            See the mkdir[https://rclone.oUrg/commands/rclone_mkdir/] command for more information on the above.
    """

    @swagger_auto_schema(request_body=BaseRemoteRequestSerializer)
    def post(self, request, *args, **kwargs):
        # Instantiate the Rclone object
        rclone_instance = Rclone()

        # Configure the Rclone instance using the builder pattern and execute the operation
        response = (
            rclone_instance
            .set_operation(RcloneOperations.OPERATIONS_MKDIR)
            .set_request_serializer(BaseRemoteRequestSerializer)  # Ensure this is the correct serializer for the request
            .set_response_serializer(serializers.Serializer)  # Ensure this is the correct serializer for the response
            .execute(request.data)
        )

        return response


class RcloneMoveFileView(APIView):
    """
    API View for moving a file using Rclone.

    Rclone docs:
        operations/movefile: Move a file from source remote to destination remote

        This takes the following parameters:

        srcFs - a remote name string e.g. "drive:" for the source, "/" for local filesystem
        srcRemote - a path within that remote e.g. "file.txt" for the source
        dstFs - a remote name string e.g. "drive2:" for the destination, "/" for local filesystem
        dstRemote - a path within that remote e.g. "file2.txt" for the destination

        example:

        {
          "srcFs": "GoogleDrive:",
          "srcRemote": "hehe.txt",
          "dstFs": "GoogleDrive:",
          "dstRemote": "backup/hehe.txt"
        }

    """

    @swagger_auto_schema(request_body=MoveFileRequestSerializer)
    def post(self, request, *args, **kwargs):
        # Instantiate the Rclone object
        rclone_instance = Rclone()

        # Configure the Rclone instance using the builder pattern and execute the operation
        response = (
            rclone_instance
            .set_operation(RcloneOperations.OPERATIONS_MOVE_FILE)
            .set_request_serializer(MoveFileRequestSerializer)  # Set the request serializer
            .set_response_serializer(serializers.Serializer)  # Set the response serializer
            .execute(request.data)  # Execute the operation
        )

        return response


class RclonePublicLinkView(APIView):
    """
    API View for creating public link to a file using Rclone.

    Rclone docs:
        operations/publiclink: Create or retrieve a public link to the given file or folder.
        This takes the following parameters:

        fs - a remote name string e.g. "drive:"
        remote - a path within that remote e.g. "dir"
        unlink - boolean - if set removes the link rather than adding it (optional)
        expire - string - the expiry time of the link e.g. "1d" (optional)


        Returns:

        url - URL of the resource
        See the link[https://rclone.org/commands/rclone_link/] command for more information on the above.

    """

    @swagger_auto_schema(request_body=PublicLinkRequestSerializer)
    def post(self, request, *args, **kwargs):
        # Instantiate the Rclone object
        rclone_instance = Rclone()

        # Configure the Rclone instance using the builder pattern and execute the operation
        response = (
            rclone_instance
            .set_operation(RcloneOperations.OPERATIONS_PUBLIC_LINK)
            .set_request_serializer(PublicLinkRequestSerializer)  # Set the request serializer
            .set_response_serializer(PublicLinkResponseSerializer)  # Set the response serializer
            .execute(request.data)  # Execute the operation
        )

        return response


class GenerateConclusionView(APIView):

    @swagger_auto_schema(request_body=GenerateConclusionRequestSerializer)
    def post(self, request):
        serializer = GenerateConclusionRequestSerializer(data=request.data)
        if serializer.is_valid():
            task_id = serializer.validated_data['task']
            conclusion_number = serializer.validated_data['conclusionNumber']

            # Find the ExpertiseData entry
            try:
                task = Task.objects.get(pk=task_id)
                expertise_data = ExpertiseData.objects.get(task_id=task_id)
                response = ""
                response_rename_folder = ""

                expertise_data.conclusionNumber = conclusion_number
                expertise_data.save()

                self.request.user.notify(
                    initiator=self.request.user,
                    title="დასკვნა წარმატებით დაგენერირდა",
                    message=f"დასკვნა წარმატებით დაგენერირდა. დასკვნის ნომერი: {conclusion_number}",
                    level=Notification.Level.INFO
                )

                # if task.drive_folder_path:
                #     response = move_folder(task.drive_folder_path, f"საბოლოო დასკვნები")
                #
                #     if "Folder moved successfully to new parent ID" in response:
                #         task.drive_folder_path = f"საბოლოო დასკვნები/{conclusion_number}"
                #         response_rename_folder = rename_folder(task.drive_folder_path, f"{conclusion_number}")
                #         expertise_data.conclusionNumber = conclusion_number
                #         expertise_data.save()
                #         task.save()
                #
                #         self.request.user.notify(
                #             initiator=self.request.user,
                #             title="დასკვნა წარმატებით დაგენერირდა",
                #             message=f"დასკვნა წარმატებით დაგენერირდა. დასკვნის ნომერი: {conclusion_number}, მისამართი: {task.drive_folder_path}",
                #             level=Notification.Level.INFO
                #         )
                #
                #     else:
                #         self.request.user.notify(
                #             initiator=self.request.user,
                #             title="დასკვნა ვერ დაგენერირდა",
                #             message=f"დასკვნა ვერ დაგენერირდა, {response}, {response_rename_folder}",
                #             level=Notification.Level.INFO
                #         )


                return Response({"rename_folder_response": response_rename_folder}, status=status.HTTP_200_OK)
                # return Response({"drive_api_response": str(response), "rename_folder_response": response_rename_folder}, status=status.HTTP_200_OK)
            except Exception as e:

                self.request.user.notify(
                    initiator=self.request.user,
                    title="დასკვნა ვერ დაგენერირდა",
                    message=f"დასკვნა ვერ დაგენერირდა: {e}",
                    level=Notification.Level.INFO
                )
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareFolderWithUserView(APIView):

    @swagger_auto_schema(request_body=ShareFolderRequestSerializer)
    def post(self, request):
        serializer = ShareFolderRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            folder_path = serializer.validated_data['folder_path']

            try:
                user = UserAccount.objects.get(pk=user_id)
                user_email = user.email

                response = share_folder_or_file_with_user(folder_path, user_email)

                if "Folder or file successfully shared with" in response:
                    self.request.user.notify(
                        initiator=self.request.user,
                        title="სამუშაო ფოლდერი წარმატებით გაუზიარდა მომხმარებელს.",
                        message=f"ფოლდერი: {folder_path}",
                        level=Notification.Level.INFO
                    )
                else:
                    self.request.user.notify(
                        initiator=self.request.user,
                        title="სამუშაო ფოლდერი ვერ გაუზიარდა მომხმარებელს.",
                        message=f"ფოლდერი: {folder_path}",
                        level=Notification.Level.INFO
                    )

                    return Response({"response": response}, status=status.HTTP_400_BAD_REQUEST)

                return Response({"response": response}, status=status.HTTP_200_OK)
            except Exception as e:
                self.request.user.notify(
                    initiator=self.request.user,
                    title="სამუშაო ფოლდერი ვერ გაუზიარდა მომხმარებელს.",
                    message=f"ფოლდერი: {folder_path}",
                    level=Notification.Level.INFO
                )
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
