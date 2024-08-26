from rest_framework import serializers

from apps.accounts.serializers import CustomUserDetailsSerializer
from apps.expertiseMainFlow.serializers import ExpertiseFolderSimpleSerializer
from apps.tasks.models import Task, SubTask
from django.utils import timezone

class SubtaskCreateSerializer(serializers.ModelSerializer):
    creator = CustomUserDetailsSerializer()
    assign_to = CustomUserDetailsSerializer()
    folder = ExpertiseFolderSimpleSerializer()

    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ('uuid', 'creator', 'created_at', 'updated_at')


class SubtaskListSerializer(serializers.ModelSerializer):
    creator = CustomUserDetailsSerializer()
    assign_to = CustomUserDetailsSerializer()
    folder = ExpertiseFolderSimpleSerializer()

    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ('uuid', 'creator', 'created_at', 'updated_at')
        depth = 1

    def validate_deadline_to(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("The deadline cannot be in the past.")
        return value

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('uuid', 'creator', 'sent_to_customer', 'created_at', 'updated_at')

    def validate_deadline_to(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("The deadline cannot be in the past.")
        return value

class TaskListSerializer(serializers.ModelSerializer):
    subtasks = SubtaskListSerializer(many=True, read_only=True)
    creator = CustomUserDetailsSerializer(read_only=True)
    assign_to = CustomUserDetailsSerializer(read_only=True)
    folder = ExpertiseFolderSimpleSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('uuid', 'creator', 'sent_to_customer', 'created_at', 'updated_at')
        depth = 1