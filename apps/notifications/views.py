from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from apps.notifications.filters import ListNotificationsFilter
from apps.notifications.models import Notification
from apps.notifications.paginations import StandardPagination
from apps.notifications.serializers import NotificationSerializer


class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ListNotificationsFilter
    pagination_class = StandardPagination
    ordering_fields = '__all__'
    queryset = Notification.objects.all()


class NotificationDetailsView(RetrieveAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    lookup_field = 'uuid'


class NotificationUpdateView(UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = 'uuid'


class NotificationDeleteView(DestroyAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    lookup_field = 'uuid'


class UserNotificationsListView(ListAPIView):
    serializer_class = NotificationSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Notification.objects.filter(receiver=user_id)