from allauth.socialaccount.models import SocialToken
from django.contrib import admin

from apps.accounts.models import UserAccount, UserProfile

# from .models import UserAccount

# Register your models here.

admin.site.register(UserAccount)
admin.site.register(UserProfile)
# admin.site.register(SocialToken)