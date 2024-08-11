from django.db import models
from django.contrib.auth import get_user_model
import uuid

from expertiseMainFlow.utils import get_upload_to

User = get_user_model()


class Tag(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    tags = models.ManyToManyField(Tag, related_name="folder_tags", blank=True)
    # TODO - change comment as jsonfield
    comment = models.TextField(max_length=5000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class File(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=get_upload_to, null=True, blank=True)
    folder = models.ForeignKey(ExpertiseFolder, related_name='files', on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, related_name="file_tags", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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


class FolderData(models.Model):
    field = models.ForeignKey(
        CustomField,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="fields",
        editable=False,
    )

    expertise_folder = models.ForeignKey(
        ExpertiseFolder,
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
                return self.value_int
            case CustomField.FieldDataType.INT:
                return self.value_int
            case CustomField.FieldDataType.FLOAT:
                return self.value_float
            case _:
                raise NotImplementedError(self.field.data_type)
