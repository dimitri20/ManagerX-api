import django_filters
from django_mailbox.models import Message



class EMailMessagesListFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['id', 'mailbox', 'message_id']

