# signals.py

from allauth.socialaccount.models import SocialAccount
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
import requests
from .models import UserProfile
from .tasks import create_shared_folder_for_user_task


@receiver(post_save, sender=SocialAccount)
def save_profile_picture(sender, instance, created, **kwargs):
    if created:
        # This is the social account object created after a successful login
        user = instance.user
        profile, created = UserProfile.objects.get_or_create(user=user)

        if instance.provider == 'google':
            picture_url = instance.extra_data.get('picture')
            if picture_url:
                response = requests.get(picture_url)
                if response.status_code == 200:
                    # Save the image in the user's profile
                    profile.profile_image.save(f'{user.username}_profile_image.jpg', ContentFile(response.content), save=True)

        create_shared_folder_for_user_task(user.id)