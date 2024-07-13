from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import DocumentSerializer, DocumentSignEventSerializer, DocumentVerifyEventSerializer, \
    TaskRegisterEventSerializer, SendDocumentToVerifyEventSerializer, SendDocumentToSignEventSerializer
from .models import Document, TaskRegisteringEvent, SendDocumentToVerifyEvent, SendDocumentToSignEvent
from .utils import document_is_verified_by_everyone, document_is_signed_by_everyone, filter_documents_by_sender_and_receiver
from .filters import DocumentsFilter
from .paginations import DocumentLimitOffsetPagination

User = get_user_model()


class UploadDocumentView(CreateAPIView):
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignDocumentView(CreateAPIView):
    serializer_class = DocumentSignEventSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['signer'] = request.user
            serializer.save()

            document = serializer.validated_data['document']
            document.signed_by_users.add(request.user)
            document.have_to_sign_users.remove(request.user)
            document.is_signed = document_is_signed_by_everyone(document)
            document.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyDocumentView(CreateAPIView):
    serializer_class = DocumentVerifyEventSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['verifier'] = request.user
            serializer.save()

            document = serializer.validated_data['document']
            document.verified_by_users.add(request.user)
            document.is_verified = document_is_verified_by_everyone(document)
            document.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterTaskView(CreateAPIView):
    serializer_class = TaskRegisterEventSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['sender'] = request.user

            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendToVerifyDocumentView(CreateAPIView):
    serializer_class = SendDocumentToVerifyEventSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['sender'] = request.user
            serializer.save()

            document = serializer.validated_data['document']
            # if request.validated_data['recipient'] in document.verified_by_users:
            #     return Response("User already verified document.", status=status.HTTP_400_BAD_REQUEST)

            document.have_to_verify_users.add(request.user)
            document.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendToSignDocumentView(CreateAPIView):
    serializer_class = SendDocumentToSignEventSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['sender'] = request.user
            serializer.save()

            document = serializer.validated_data['document']
            # if request.validated_data['recipient'] in document.verified_by_users:
            #     return Response("User already verified document.", status=status.HTTP_400_BAD_REQUEST)

            document.have_to_sign_users.add(request.user)
            document.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetailView(APIView):
    serializer_class = DocumentSerializer

    def get(self, request, uuid):
        user = request.user
        document = get_object_or_404(Document, uuid=uuid)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

    def put(self, request, uuid):
        document = get_object_or_404(Document, uuid=uuid)
        serializer = DocumentSerializer(
            document, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DocumentListView(ListAPIView):
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DocumentsFilter
    pagination_class = DocumentLimitOffsetPagination
    ordering_fields = '__all__'

    def get(self, request, *args, **kwargs):
        self.queryset = filter_documents_by_sender_and_receiver(request)
        return super().get(request, *args, **kwargs)
