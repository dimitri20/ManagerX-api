from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


# Create your models here.
# TODO - correct updated_ad into updated_at
class Document(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    documentNumber = models.BigIntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True)
    have_to_sign_users = models.ManyToManyField(User, related_name='have_to_sign_users', blank=True)
    have_to_verify_users = models.ManyToManyField(User, related_name='have_to_verify_users', blank=True)
    verified_by_users = models.ManyToManyField(User, related_name='verified_by_users', blank=True)
    signed_by_users = models.ManyToManyField(User, related_name='signed_by_users', blank=True)
    is_signed = models.BooleanField(default=False, blank=True, null=True)
    is_verified = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_ad = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ", " + self.file.name.split("/")[-1]


class TaskRegisteringEvent(models.Model):

    class TaskType(models.TextChoices):
        VERIFY = 'VERIFY',
        SIGN = 'SIGN',

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    taskType = models.CharField(max_length=255, choices=TaskType.choices, null=False, blank=False)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.SET_NULL, null=True)
    recipient = models.ForeignKey(User, related_name="recipient", on_delete=models.SET_NULL, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_ad = models.DateTimeField(auto_now=True)


class SendDocumentToVerifyEvent(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    sender = models.ForeignKey(User, related_name="sendDocumentToVerify_sender", on_delete=models.SET_NULL, null=True)
    recipient = models.ForeignKey(User, related_name="sendDocumentToVerify_recipient", on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_ad = models.DateTimeField(auto_now=True)


class SendDocumentToSignEvent(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    sender = models.ForeignKey(User, related_name="sendDocumentToSign_sender", on_delete=models.SET_NULL, null=True)
    recipient = models.ForeignKey(User, related_name="sendDocumentToSign_recipient", on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_ad = models.DateTimeField(auto_now=True)


class DocumentSignEvent(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    signer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=False)
    task = models.ForeignKey(TaskRegisteringEvent, on_delete=models.SET_NULL, null=True)
    signed_at = models.DateTimeField(auto_now_add=True)


class DocumentVerifyEvent(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    verifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=False)
    task = models.ForeignKey(TaskRegisteringEvent, on_delete=models.SET_NULL, null=True)
    verified_at = models.DateTimeField(auto_now_add=True)

class DocumentFlow(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    sign_event = models.ForeignKey(DocumentSignEvent, on_delete=models.SET_NULL, null=True)
    verify_event = models.ForeignKey(DocumentVerifyEvent, on_delete=models.SET_NULL, null=True)

# class DocumentSignature(models.Model):
#     uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=False)
#     signer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     signed_at = models.DateTimeField(auto_now_add=True)
#
# class DocumentFlow(models.Model):
#     uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=False)
#     sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     recipients = models.ManyToManyRel(User)
#     sent_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField() #pending, signed, verified
