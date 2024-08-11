from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django_mailbox.models import Message, MessageAttachment, Mailbox
from rest_framework.filters import OrderingFilter

from expertiseMainFlow.filters import EMailMessagesListFilter
from expertiseMainFlow.models import ExpertiseFolder, File, CustomField, FolderData
from expertiseMainFlow.paginations import StandardPagination
from expertiseMainFlow.serializers import FileSerializer, ExpertiseFolderSerializer, ExpertiseFolderDetailsSerializer, \
    EmailSerializer, ImportAttachmentsFromMailSerializer, EmailMessageAttachmentSerializer, \
    CustomFieldSerializer, FolderDataCreateSerializer

import os
import shutil
import uuid


class UploadFileView(CreateAPIView):
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['title'] = serializer.validated_data['file'].name
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateExpertiseFolderView(CreateAPIView):
    serializer_class = ExpertiseFolderSerializer
    queryset = ExpertiseFolder.objects.all()

    def perform_create(self, serializer):
        customer = serializer.validated_data['customer']
        case = serializer.validated_data['case']
        serializer.validated_data['title'] = f"{customer}, {case}"
        serializer.validated_data['path'] = f"media/uploads/{uuid.uuid4}/"
        serializer.save()


class ExpertiseFolderDetailsView(RetrieveAPIView):
    serializer_class = ExpertiseFolderDetailsSerializer
    queryset = ExpertiseFolder.objects.all()
    lookup_field = "uuid"


class ListExpertiseFolderView(ListAPIView):
    serializer_class = ExpertiseFolderSerializer
    queryset = ExpertiseFolder.objects.all()


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


class CustomFieldViewSet(CreateAPIView):
    serializer_class = CustomFieldSerializer
    queryset = CustomField.objects.all()


class CustomFieldListViewSet(ListAPIView):
    serializer_class = CustomFieldSerializer
    queryset = CustomField.objects.all()


class FolderDataViewSet(GenericAPIView):
    serializer_class = FolderDataCreateSerializer
    queryset = FolderData.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            expertise_folder = serializer.validated_data['expertise_folder']
            key_value_pairs = serializer.validated_data['key_value_pair']

            instances = serializer.create_or_update_folder_data(expertise_folder, key_value_pairs)
            response_data = [
                {'id': instance.id, 'expertise_folder': instance.expertise_folder.uuid, 'field': instance.field.id} for
                instance in instances]
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


