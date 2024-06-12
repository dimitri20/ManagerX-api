from rest_framework import serializers
from .models import Document, DocumentSignEvent, DocumentVerifyEvent, TaskRegisteringEvent


class DocumentSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(read_only=False)

    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('uuid', 'is_signed', 'is_verified', 'creation_date', 'updated_ad')


class DocumentSignEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentSignEvent
        fields = '__all__'
        read_only_fields = ('uuid', 'signed_at', )


class DocumentVerifyEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentVerifyEvent
        fields = '__all__'
        read_only_fields = ('uuid', 'verified_at', )


class TaskRegisterEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskRegisteringEvent
        fields = '__all__'
        read_only_fields = ('uuid', 'sent_at', 'updated_ad')
