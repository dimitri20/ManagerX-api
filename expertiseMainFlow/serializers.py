from rest_framework import serializers
from .models import File, ExpertiseFolder, Tag
from django_mailbox.models import Message, Mailbox
from django_mailbox.models import MessageAttachment


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class ExpertiseFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseFolder
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class ExpertiseFolderDetailsSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = ExpertiseFolder
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')

    def get_files(self, obj):
        return File.objects.get(folder=obj.uuid)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class EmailMessageAttachmentSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()

    class Meta:
        model = MessageAttachment
        fields = '__all__'

    def get_filename(self, obj):
        return obj.get_filename()


class EmailSerializer(serializers.ModelSerializer):
    attachments = EmailMessageAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        exclude = ('body',)

    def get_attachments(self, obj):
        return EmailMessageAttachmentSerializer.objects.get(message_id=obj.id)


class ImportAttachmentsFromMailSerializer(serializers.Serializer):
    email_id = serializers.IntegerField()
    copy_to_folder_id = serializers.CharField(max_length=255, allow_blank=False, allow_null=False)
