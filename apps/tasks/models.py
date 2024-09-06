from django.contrib.auth import get_user_model
from django.db import models
import uuid
from django.utils import timezone



User = get_user_model()


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'TODO', 'To Do'
        INPROGRESS = 'INPROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'
        REJECTED = 'REJECTED', 'Rejected'
        UNCERTAIN = 'UNCERTAIN', 'Uncertain'

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=255, choices=Status.choices, null=False, blank=False)
    comment = models.JSONField(max_length=20000, null=True, blank=True)
    creator = models.ForeignKey(User, related_name='task_creator', on_delete=models.CASCADE, null=False)
    assign_to = models.ForeignKey(User, related_name='task_assign_to', on_delete=models.CASCADE, null=True, blank=True)
    deadline_from = models.DateField(null=True, blank=True)
    deadline_to = models.DateField(null=True, blank=True)
    drive_folder_path = models.CharField(max_length=255, null=True, blank=True)
    sent_to_customer = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_overdue(self):
        return self.deadline_to and self.deadline_to < timezone.now()


class SubTask(models.Model):
    class Status(models.TextChoices):
        TODO = 'TODO', 'To Do'
        INPROGRESS = 'INPROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'
        REJECTED = 'REJECTED', 'Rejected'

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=255, choices=Status.choices, null=False, blank=False)
    comment = models.JSONField(max_length=20000, null=True, blank=True)
    creator = models.ForeignKey(User, related_name='subtask_creator', on_delete=models.CASCADE, null=False)
    assign_to = models.ForeignKey(User, related_name='subtask_assign_to', on_delete=models.CASCADE, null=False)
    deadline_from = models.DateField(null=True, blank=True)
    deadline_to = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_overdue(self):
        return self.deadline_to and self.deadline_to < timezone.now()