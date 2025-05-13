from django.contrib import admin
from apps.accounts.models import UserAccount, UserProfile

admin.site.register(UserAccount)
admin.site.register(UserProfile)
