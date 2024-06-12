from django.contrib import admin
from .models import Document, DocumentVerifyEvent, DocumentSignEvent
# Register your models here.

admin.site.register(Document)
admin.site.register(DocumentVerifyEvent)
admin.site.register(DocumentSignEvent)
