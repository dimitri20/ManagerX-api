from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView, \
    GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.http import HttpResponse, Http404
from django.conf import settings
import os

from apps.expertiseMainFlow.filters import FileListFilter
from apps.expertiseMainFlow.models import File
from apps.expertiseMainFlow.paginations import StandardPagination
from apps.expertiseMainFlow.serializers.serializers import FileSerializer
from apps.notifications.models import Notification


class UploadFileView(CreateAPIView):
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = self.request.user
            serializer.validated_data['title'] = serializer.validated_data['file'].name
            serializer.save()

            serializer.validated_data['subtask'].creator.notify(
                initiator=self.request.user,
                title="დაემატა დანართი",
                message=f"მომხმარებელმა {self.request.user} დაამატა დანართი დავალებაზე: {serializer.validated_data['title']}",
                level=Notification.Level.INFO
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateFileView(UpdateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    lookup_field = 'uuid'


class FileDetailsView(RetrieveAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()
    lookup_field = 'uuid'


class DeleteFileView(DestroyAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()
    lookup_field = 'uuid'


class ListFileView(ListAPIView):
    serializer_class = FileSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FileListFilter
    pagination_class = StandardPagination
    ordering_fields = '__all__'
    queryset = File.objects.all()


class DownloadFileView(GenericAPIView):

    @swagger_auto_schema(
        operation_description="Download a file by its UUID",
        responses={200: 'File', 404: 'File not found'}
    )
    def get(self, request, uuid):
        try:
            file_instance = File.objects.get(uuid=uuid)
            file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)

            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/force-download')
                    response[
                        'Content-Disposition'] = f'attachment; filename="{file_instance.title or os.path.basename(file_path)}"'
                    return response
            else:
                raise Http404("File not found")
        except File.DoesNotExist:
            return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)