from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .serializers import DocumentSerializer, DocumentSignEventSerializer, DocumentVerifyEventSerializer, \
    TaskRegisterEventSerializer
from .models import Document

User = get_user_model()


class UploadDocumentView(CreateAPIView):
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        # assume request.user would be set to the authenticated user - TODO
        # access file like: uploaded_file = serializer.validated_data['file']

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # uncomment this if you want to automatically assign logged in user
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)
    #     return super().perform_create(serializer)


class SignDocumentView(CreateAPIView):
    serializer_class = DocumentSignEventSerializer

    def post(self, request, *args, **kwargs):
        # TODO - assume request.user would be set to the authenticated user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # TODO - add document signing logic
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyDocumentView(CreateAPIView):
    serializer_class = DocumentVerifyEventSerializer

    def post(self, request, *args, **kwargs):
        # TODO - assume request.user would be set to the authenticated user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # TODO - add document verifying logic
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterTaskView(CreateAPIView):
    serializer_class = TaskRegisterEventSerializer

    def post(self, request, *args, **kwargs):
        # TODO - assume request.user would be set to the authenticated user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # TODO - add document verifying logic
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

