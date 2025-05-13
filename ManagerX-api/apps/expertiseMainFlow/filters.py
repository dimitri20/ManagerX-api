import django_filters
from django_mailbox.models import Message

from apps.expertiseMainFlow.models import File, ExpertiseFolder


class EMailMessagesListFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['id', 'mailbox', 'message_id']


class FileListFilter(django_filters.FilterSet):
    class Meta:
        model = File
        fields = ['uuid', 'title', 'subtask', 'owner', 'created_at', 'updated_at', ]


class FolderListFilter(django_filters.FilterSet):
    class Meta:
        model = ExpertiseFolder
        fields = ['uuid', 'conclusionNumber', 'title', 'customer', 'case', 'status', 'owner', 'created_at', 'updated_at', ]