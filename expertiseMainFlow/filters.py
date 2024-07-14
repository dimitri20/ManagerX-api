import django_filters
from django_mailbox.models import Message

from expertiseMainFlow.models import Task


class EMailMessagesListFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['id', 'mailbox', 'message_id']


class TaskListFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = '__all__'
