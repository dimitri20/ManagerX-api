from rest_framework.generics import UpdateAPIView, DestroyAPIView

from apps.tasks.filters import TaskListFilter, SubtaskListFilter
from apps.tasks.models import Task, SubTask
from apps.tasks.paginations import StandardPagination
from apps.tasks.serializers import TaskSerializer, TaskDetailViewSerializer, SubtaskSerializer, TaskListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter
from .tasks import send_notification_to_assignee


class TaskCreateView(CreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data['creator'] = self.request.user
        serializer.save()

        # execute tasks
        send_notification_to_assignee.delay(serializer.data)


class TaskDetailView(RetrieveAPIView):
    serializer_class = TaskDetailViewSerializer
    queryset = Task.objects.all()
    lookup_field = 'uuid'


class TaskUpdateView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'uuid'


class TaskDeleteView(DestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = 'uuid'


class TaskListView(ListAPIView):
    serializer_class = TaskListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TaskListFilter
    pagination_class = StandardPagination
    ordering_fields = '__all__'
    queryset = Task.objects.all()


class SubtaskCreateView(CreateAPIView):
    serializer_class = SubtaskSerializer
    queryset = SubTask.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data['creator'] = self.request.user
        serializer.save()


class SubtaskDetailView(RetrieveAPIView):
    serializer_class = SubtaskSerializer
    queryset = SubTask.objects.all()
    lookup_field = 'uuid'


class SubtaskUpdateView(UpdateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubtaskSerializer
    lookup_field = 'uuid'


class SubtaskDeleteView(DestroyAPIView):
    serializer_class = SubtaskSerializer
    queryset = SubTask.objects.all()
    lookup_field = 'uuid'


class SubtaskListView(ListAPIView):
    serializer_class = SubtaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SubtaskListFilter
    pagination_class = StandardPagination
    ordering_fields = '__all__'
    queryset = SubTask.objects.all()
