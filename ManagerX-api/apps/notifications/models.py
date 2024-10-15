from email.policy import default

from django.db import models


from django.contrib.auth import get_user_model
from django.db import models
from time import timezone
import uuid

User = get_user_model()

class Notification(models.Model):

    class Level(models.TextChoices):
        SUCCESS = 'success',
        INFO = 'info',
        WARNING = 'warning',
        ERROR = 'error',

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiator', blank=True, null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    unread = models.BooleanField(default=True, blank=True, null=True)
    emailed = models.BooleanField(default=False, blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True, null=True)
    level = models.CharField(choices=Level.choices, default=Level.INFO, max_length=20, blank=True, null=True)
    additional_data = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']