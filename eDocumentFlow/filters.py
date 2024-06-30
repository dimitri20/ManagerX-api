import django_filters
from .models import Document, SendDocumentToVerifyEvent


class DocumentsFilter(django_filters.FilterSet):

    class Meta:
        model = Document
        fields = ['documentNumber', 'title', 'owner', 'is_signed', 'is_verified', 'created_at']
