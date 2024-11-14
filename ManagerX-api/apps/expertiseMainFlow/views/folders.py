import uuid

from allauth.headless.base.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from apps.expertiseMainFlow.filters import FolderListFilter
from apps.expertiseMainFlow.models import ExpertiseFolder, CustomField, ExpertiseAdditionalData, ExpertiseData
from apps.expertiseMainFlow.paginations import StandardPagination
from apps.expertiseMainFlow.serializers.serializers import ExpertiseFolderSerializer, \
    ExpertiseFolderDetailsSerializer, \
    CustomFieldSerializer, FolderDataCreateSerializer, ExpertiseDataSerializer, ExpertiseDataCreateSerializer, \
    UpdateCustomFieldSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class ListDataViewSet(ListAPIView):
    serializer_class = ExpertiseDataSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = StandardPagination
    ordering_fields = '__all__'
    queryset = ExpertiseData.objects.all()

class CustomFieldViewSet(CreateAPIView):
    serializer_class = CustomFieldSerializer
    queryset = CustomField.objects.all()

class UpdateCustomFieldViewSet(UpdateAPIView):
    serializer_class = UpdateCustomFieldSerializer
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
    serializer_class = ExpertiseDataCreateSerializer
    queryset = ExpertiseAdditionalData.objects.all()



