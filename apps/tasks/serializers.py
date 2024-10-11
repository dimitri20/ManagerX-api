from rest_framework import serializers

from apps.accounts.serializers import CustomUserDetailsSerializer
from apps.expertiseMainFlow.serializers.serializers import ExpertiseFolderSimpleSerializer, FileSerializer
from apps.tasks.models import Task, SubTask, Comment
from django.utils import timezone

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('uuid', 'creator', 'created_at', 'updated_at')

class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)

class CommentSerializer(serializers.ModelSerializer):
    creator = CustomUserDetailsSerializer()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        read_only_fields = ('uuid', 'creator', 'created_at', 'updated_at')
        exclude = ('subtask', 'parent')
        depth = 1

    def get_replies(self, obj):
        child_comments = obj.children()
        return CommentSerializer(child_comments, many=True).data


class SubtaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ('uuid', 'creator', 'created_at', 'updated_at')

    def validate_deadline_to(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("The deadline cannot be in the past.")
        return value

class SubtaskListSerializer(serializers.ModelSerializer):
    creator = CustomUserDetailsSerializer()
    assign_to = CustomUserDetailsSerializer()
    attachments = FileSerializer(source="subtask_files", many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ('uuid', 'creator', 'created_at', 'updated_at')
        depth = 1

    def get_comments(self, obj):
        top_level_comments = obj.subtask_comments.filter(parent__isnull=True)
        return CommentSerializer(top_level_comments, many=True).data


class TaskCreateSerializer(serializers.ModelSerializer):
    subtasks = SubtaskListSerializer(many=True, read_only=True)

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