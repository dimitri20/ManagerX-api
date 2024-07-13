from django.db import models
from django.contrib.auth import get_user_model
import uuid

import dcs.settings
from expertiseMainFlow.utils import get_upload_to

User = get_user_model()


class Tag(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TagCreateEvent(models.Model):
    pass


class ExpertiseFolder(models.Model):
    class Status(models.TextChoices):
        TODO = 'TODO', 'To Do'
        INPROGRESS = 'INPROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'
        REJECTED = 'REJECTED', 'Rejected'
        UNCERTAIN = 'UNCERTAIN', 'Uncertain'

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    customer = models.CharField(max_length=255, null=True, blank=True)
    case = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=Status.choices, null=False, blank=False)
    path = models.CharField(max_length=255, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="folder_tags", blank=True)
    comment = models.TextField(max_length=5000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ExpertiseFolderCreateEvent(models.Model):
    pass


class File(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=get_upload_to, null=True, blank=True)
    folder = models.ForeignKey(ExpertiseFolder, related_name='files', on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, related_name="file_tags", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FileAddEvent(models.Model):
    pass


class ExpertiseFolderStatusChanged(models.Model):
    pass
