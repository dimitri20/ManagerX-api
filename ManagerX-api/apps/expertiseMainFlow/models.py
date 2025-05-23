from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid
import os
import shutil

from apps.expertiseMainFlow.utils import get_upload_to
from apps.tasks.models import Task, SubTask

User = get_user_model()

class ExpertiseFolder(models.Model):
    class Status(models.TextChoices):
        TODO = 'TODO', 'To Do'
        INPROGRESS = 'INPROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'
        REJECTED = 'REJECTED', 'Rejected'
        UNCERTAIN = 'UNCERTAIN', 'Uncertain'

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    conclusionNumber = models.CharField(max_length=255, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    customer = models.CharField(max_length=255, null=True, blank=True)
    case = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=Status.choices, null=False, blank=False)
    path = models.CharField(max_length=255, null=True, blank=True)
    comment = models.CharField(max_length=10000, null=True, blank=True)
    owner = models.ForeignKey(User, related_name="expertise_folders", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        if self.path:
            # Construct the full path
            full_path = os.path.join(settings.MEDIA_ROOT, self.path)

            # Check if the full path points to a valid directory
            if os.path.isdir(full_path):
                try:
                    # Recursively delete the directory and all its contents
                    shutil.rmtree(full_path)
                except Exception as e:
                    # Handle exceptions (e.g., log them if necessary)
                    raise ValidationError(f"Error deleting directory {full_path}: {e}")

            # Call the superclass delete method to delete the model instance
        super().delete(*args, **kwargs)

class ExpertiseData(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    conclusionNumber = models.CharField(max_length=255, null=True, blank=True)
    task = models.ForeignKey(Task, related_name="expertise_data", on_delete=models.CASCADE, null=True, blank=True, unique=True)

class File(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=get_upload_to, null=True, blank=True)
    owner = models.ForeignKey(User, related_name="expertise_files", on_delete=models.CASCADE, null=True, blank=True)
    subtask = models.ForeignKey(SubTask, related_name="subtask_files", on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.file:
            # Construct the full path to the file
            full_file_path = os.path.join(settings.MEDIA_ROOT, self.file.name)

            # Check if the file exists
            if os.path.isfile(full_file_path):
                try:
                    # Delete the file from the filesystem
                    os.remove(full_file_path)
                except Exception as e:
                    # Raise an error if the file cannot be deleted
                    raise ValidationError(f"Error deleting file {full_file_path}: {e}")

        # Call the superclass delete method to delete the model instance
        super().delete(*args, **kwargs)

class CustomField(models.Model):
    class FieldDataType(models.TextChoices):
        STRING = "string"
        URL = "url"
        DATE = "date"
        BOOL = "boolean"
        INT = "integer"
        FLOAT = "float"

    name = models.CharField(max_length=255, null=False, blank=False)
    label = models.CharField(max_length=255, null=False, blank=False, default=name.__str__())
    data_type = models.CharField(max_length=255, choices=FieldDataType.choices, null=False, blank=False)

class ExpertiseAdditionalData(models.Model):
    field = models.ForeignKey(
        CustomField,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="fields",
        editable=False,
    )

    expertise_data = models.ForeignKey(
        ExpertiseData,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="custom_fields",
        editable=False,
    )

    value_string = models.CharField(max_length=255, null=True)
    value_url = models.URLField(null=True)
    value_date = models.DateField(null=True)
    value_bool = models.BooleanField(null=True)
    value_int = models.IntegerField(null=True)
    value_float = models.FloatField(null=True)

    @property
    def value(self):
        """
        Based on the data type, access the actual value the instance stores
        A little shorthand/quick way to get what is actually here
        """
        match self.field.data_type:
            case CustomField.FieldDataType.STRING:
                return self.value_string
            case CustomField.FieldDataType.URL:
                return self.value_url
            case CustomField.FieldDataType.DATE:
                return self.value_date
            case CustomField.FieldDataType.BOOL:
                return self.value_bool
            case CustomField.FieldDataType.INT:
                return self.value_int
            case CustomField.FieldDataType.FLOAT:
                return self.value_float
            case _:
                raise NotImplementedError(self.field.data_type)
