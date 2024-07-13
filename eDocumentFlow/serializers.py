from rest_framework import serializers
from .models import Document, DocumentSignEvent, DocumentVerifyEvent, TaskRegisteringEvent, SendDocumentToSignEvent, \
    SendDocumentToVerifyEvent


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('uuid', 'is_signed', 'is_verified', 'verified_by_users', 'creation_date', 'updated_ad')


class DocumentSignEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSignEvent
        fields = '__all__'
        read_only_fields = ('uuid', 'signed_at',)


class DocumentVerifyEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVerifyEvent
        fields = '__all__'
        read_only_fields = ('uuid', 'verifier', 'verified_at',)


class TaskRegisterEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRegisteringEvent
        fields = '__all__'
        read_only_fields = ('uuid', 'sent_at', 'updated_ad')


class SendDocumentToVerifyEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendDocumentToVerifyEvent
        fields = '__all__'
        read_only_fields = ('uuid', 'sent_at', 'updated_ad')


class SendDocumentToSignEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendDocumentToSignEvent
        fields = '__all__'
        read_only_fields = ('uuid', 'sent_at', 'updated_ad')
