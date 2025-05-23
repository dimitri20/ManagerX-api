from django.contrib.auth import get_user_model
from rest_framework.generics import UpdateAPIView, DestroyAPIView, GenericAPIView

from apps.tasks.filters import TaskListFilter, SubtaskListFilter
from apps.tasks.models import Task, SubTask, Comment, Note
from apps.tasks.paginations import StandardPagination
from apps.tasks.serializers import TaskListSerializer, SubtaskListSerializer, TaskCreateSerializer, \
    SubtaskCreateSerializer, CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer, NoteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter
from apps.notifications.tasks import send_notification
from ..expertiseMainFlow.models import ExpertiseData
from ..notifications.models import Notification

User = get_user_model()

class TaskCreateView(CreateAPIView):
    serializer_class = TaskCreateSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data['creator'] = self.request.user
        saved_task = serializer.save()

        expertise_data = ExpertiseData(task=saved_task)
        expertise_data.save()

        if 'assign_to' in serializer.validated_data:

            serializer.validated_data['assign_to'].notify(
                initiator=self.request.user,
                title="შეიქმნა პროექტი",
                message=f"მომხმარებელმა {self.request.user} დაგავალათ პროექტი: {serializer.validated_data['title']}",
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

        if 'assign_to' in serializer.validated_data:

            serializer.validated_data['assign_to'].notify(
                initiator=self.request.user,
                title="დავალება",
                message=f"მომხმარებელმა {self.request.user} დაგავალათ დავალება: {serializer.validated_data['title']}",
                level=Notification.Level.INFO
            )


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

class SubtaskCommentCreateView(CreateAPIView):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data['creator'] = self.request.user
        serializer.save()

        serializer.validated_data['subtask'].creator.notify(
            initiator=self.request.user,
            title="დავალება",
            message=f"მომხმარებელმა {self.request.user} დაამატა კომენტარი დავალებაზე: {serializer.validated_data['subtask'].title}",
            level=Notification.Level.INFO
        )

class SubtaskCommentDeleteView(DestroyAPIView):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()
    lookup_field = 'uuid'

class SubtaskCommentUpdateView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    lookup_field = 'uuid'

class NoteListView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'uuid'

class NoteCreateView(CreateAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

class NoteDetailView(RetrieveAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    lookup_field = 'uuid'

class NoteUpdateView(UpdateAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    lookup_field = 'uuid'

class NoteDeleteView(DestroyAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    lookup_field = 'uuid'
