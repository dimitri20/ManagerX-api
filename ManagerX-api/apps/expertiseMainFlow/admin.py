from django.contrib import admin

from apps.expertiseMainFlow import models

# Register your models here.

admin.site.register(models.ExpertiseFolder)
admin.site.register(models.File)
admin.site.register(models.ExpertiseData)
admin.site.register(models.CustomField)
admin.site.register(models.ExpertiseAdditionalData)
