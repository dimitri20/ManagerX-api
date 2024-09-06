import uuid

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from apps.expertiseMainFlow.filters import FolderListFilter
from apps.expertiseMainFlow.models import ExpertiseFolder, CustomField, ExpertiseAdditionalData, ExpertiseData
from apps.expertiseMainFlow.paginations import StandardPagination
from apps.expertiseMainFlow.serializers.serializers import ExpertiseFolderSerializer, \
    ExpertiseFolderDetailsSerializer, \
    CustomFieldSerializer, FolderDataCreateSerializer, ExpertiseDataSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class CreateExpertiseFolderView(CreateAPIView):
    serializer_class = ExpertiseFolderSerializer
    queryset = ExpertiseFolder.objects.all()

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['owner'] = self.request.user
        customer = serializer.validated_data['customer']
        case = serializer.validated_data['case']
        title = serializer.validated_data['title']

        if not title:
            if customer and case:
                serializer.validated_data['title'] = f"{customer}, {case}"
            else:
                raise ValueError('Enter customer and case, or document title.')

        uuid4 = uuid.uuid4()
        serializer.validated_data['uuid'] = uuid4
        serializer.validated_data['path'] = f"{self.request.user.id}/uploads/{uuid4}/"
        serializer.save()


class ExpertiseFolderDetailsView(RetrieveAPIView):
    serializer_class = ExpertiseFolderDetailsSerializer
    queryset = ExpertiseFolder.objects.all()
    lookup_field = "uuid"


class ListExpertiseFolderView(ListAPIView):
    serializer_class = ExpertiseFolderSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FolderListFilter
    pagination_class = StandardPagination
    ordering_fields = '__all__'
    queryset = ExpertiseFolder.objects.all()

class ListDataViewSet(ListAPIView):
    serializer_class = ExpertiseDataSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = StandardPagination
    ordering_fields = '__all__'
    queryset = ExpertiseData.objects.all()

class CustomFieldViewSet(CreateAPIView):
    serializer_class = CustomFieldSerializer
    queryset = CustomField.objects.all()


class CustomFieldListViewSet(ListAPIView):
    serializer_class = CustomFieldSerializer
    queryset = CustomField.objects.all()


class FolderDataViewSet(GenericAPIView):
    serializer_class = FolderDataCreateSerializer
    queryset = ExpertiseAdditionalData.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            expertise_folder = serializer.validated_data['expertise_data']
            key_value_pairs = serializer.validated_data['key_value_pair']

            instances = serializer.create_or_update_folder_data(expertise_folder, key_value_pairs)
            response_data = [
                {'id': instance.id, 'expertise_data': instance.expertise_data.uuid, 'field': instance.field.id} for
                instance in instances]
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateExpertiseDataView(CreateAPIView):
    serializer_class = ExpertiseDataSerializer
    queryset = ExpertiseAdditionalData.objects.all()


class UpdateExpertiseFolderView(UpdateAPIView):
    queryset = ExpertiseFolder.objects.all()
    serializer_class = ExpertiseFolderSerializer
    lookup_field = 'uuid'


class DeleteExpertiseFolderView(DestroyAPIView):
    serializer_class = ExpertiseFolderSerializer
    queryset = ExpertiseFolder.objects.all()
    lookup_field = 'uuid'
