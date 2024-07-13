from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail

from expertiseMainFlow.models import ExpertiseFolder
from expertiseMainFlow.serializers import FileSerializer, ExpertiseFolderSerializer, ExpertiseFolderDetailsSerializer


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
        serializer.validated_data['path'] = f"{customer}/{case}/"
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
