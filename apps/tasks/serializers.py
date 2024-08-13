from rest_framework import serializers

from apps.tasks.models import Task, SubTask
from django.utils import timezone


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ('uuid', 'creator', 'created_at', 'updated_at')


class SubtaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('uuid', 'title', 'status', 'deadline', 'assign_to',)


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('uuid', 'title', 'status', 'deadline', )


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('uuid', 'creator', 'subtasks', 'sent_to_customer', 'created_at', 'updated_at')

    def validate_deadline(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("The deadline cannot be in the past.")
        return value


class TaskDetailViewSerializer(serializers.ModelSerializer):
    subtasks = SubtaskListSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
