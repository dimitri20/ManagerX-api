import django_filters

from apps.notifications.models import Notification


class ListNotificationsFilter(django_filters.FilterSet):
    class Meta:
        model = Notification
        fields = ['uuid', 'initiator', 'receiver']