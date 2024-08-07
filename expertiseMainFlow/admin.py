from django.contrib import admin

from expertiseMainFlow import models

# Register your models here.

admin.site.register(models.Tag)
admin.site.register(models.ExpertiseFolder)
admin.site.register(models.File)
