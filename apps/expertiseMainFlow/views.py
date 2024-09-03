from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django_mailbox.models import Message, MessageAttachment, Mailbox
from rest_framework.filters import OrderingFilter
from rest_framework.generics import UpdateAPIView, DestroyAPIView

from apps.expertiseMainFlow.filters import EMailMessagesListFilter
from apps.expertiseMainFlow.models import ExpertiseFolder, File, CustomField, FolderData
from apps.expertiseMainFlow.paginations import StandardPagination

import shutil
import uuid

from apps.expertiseMainFlow.serializers.serializers import ImportAttachmentsFromMailSerializer, EmailSerializer


class SendEmailTestView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        subject = 'Test Email'
        message = 'This is a test email sent using SMTP in Django.'
        from_email = 'dito.gulua03@gmail.com'
        recipient_list = ['dimitri.gulua@geolab.edu.ge']

        send_mail(subject, message, from_email, recipient_list)

        return Response("hehe")


class FetchMailWithServer(GenericAPIView):

    def get(self, request, *args, **kwargs):
        mailbox = Mailbox.objects.filter(name=kwargs['name'])
        mailbox.get_new_mail()

        return Response(request.data, status=status.HTTP_200_OK)


class EMailMessagesListView(ListAPIView):
    serializer_class = EmailSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EMailMessagesListFilter
    pagination_class = StandardPagination
    ordering_fields = '__all__'

    def get_queryset(self):
        return Message.objects.filter(mailbox__name=self.kwargs['name'])


class ImportAttachmentsFromMail(GenericAPIView):
    serializer_class = ImportAttachmentsFromMailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            attachments = MessageAttachment.objects.filter(message_id=serializer.validated_data['email_id'])
            attachments = [{'path': attachment.document.path, 'name': attachment.get_filename()} for attachment in
                           attachments]
            expertise_folder = ExpertiseFolder.objects.get(pk=serializer.validated_data['copy_to_folder_id'])
            print("attachments", attachments)
            print("expertise_folder", expertise_folder)
            # TODO - check if file exists in mail folder
            for attachment in attachments:
                file = File.objects.filter(title=attachment['name'])
                if not file.exists():
                    shutil.copyfile(
                        attachment['path'],
                        f"{expertise_folder.path}{attachment['name']}"
                    )
                    file_path = f"{expertise_folder.path}{attachment['name']}".split("/")
                    del file_path[0]

                    file_instance = File(
                        title=attachment['name'],
                        file="/".join(file_path),
                        folder=expertise_folder
                    )
                    file_instance.save()

            return Response({'attachments': attachments}, status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




