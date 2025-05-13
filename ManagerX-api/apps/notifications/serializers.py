from rest_framework import serializers

from apps.accounts.serializers import CustomUserDetailsSerializer
from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    initiator = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'