from django.contrib.auth import get_user_model
from rest_framework.generics import UpdateAPIView, DestroyAPIView

from apps.tasks.filters import TaskListFilter, SubtaskListFilter
from apps.tasks.models import Task, SubTask
from apps.tasks.paginations import StandardPagination
from apps.tasks.serializers import TaskListSerializer, SubtaskListSerializer, TaskCreateSerializer, \
    SubtaskCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter
from apps.notifications.tasks import send_notification
from ..notifications.models import Notification

User = get_user_model()

class TaskCreateView(CreateAPIView):
    serializer_class = TaskCreateSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data['creator'] = self.request.user
        serializer.save()

        if 'assign_to' in serializer.validated_data:
            serializer.validated_data['assigned_to'].notify(
                initiator=self.request.user,
                receiver=serializer.validated_data['assign_to'],
                title="Created task",
                message=f"User {self.request.user.username} created for you",
                level=Notification.Level.INFO
            )


class TaskDetailView(RetrieveAPIView):
    serializer_class = TaskListSerializer
    queryset = Task.objects.all()
    lookup_field = 'uuid'


class TaskUpdateView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    lookup_field = 'uuid'


class TaskDeleteView(DestroyAPIView):
    serializer_class = TaskCreateSerializer
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
    serializer_class = SubtaskCreateSerializer
    queryset = SubTask.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data['creator'] = self.request.user
        serializer.save()


class SubtaskDetailView(RetrieveAPIView):
    serializer_class = SubtaskListSerializer
    queryset = SubTask.objects.all()
    lookup_field = 'uuid'


class SubtaskUpdateView(UpdateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubtaskCreateSerializer
    lookup_field = 'uuid'


class SubtaskDeleteView(DestroyAPIView):
    serializer_class = SubtaskCreateSerializer
    queryset = SubTask.objects.all()
    lookup_field = 'uuid'


class SubtaskListView(ListAPIView):
    serializer_class = SubtaskListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SubtaskListFilter
    pagination_class = StandardPagination
    ordering_fields = '__all__'
    queryset = SubTask.objects.all()
