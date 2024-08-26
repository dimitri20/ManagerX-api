from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from apps.accounts.models import UserProfile

User = get_user_model()

class CustomUserDetailsSerializer(UserDetailsSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        model = User  # Use your custom user model
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'avatar',)  # Add your custom fields

    def get_avatar(self, obj):
        request = self.context.get('request')
        try:
            profile = UserProfile.objects.get(user=obj)
            if profile.profile_image:
                profile_image_url = profile.profile_image.url
                # Use request to construct the full URL
                return request.build_absolute_uri(profile_image_url)
        except UserProfile.DoesNotExist:
            return None  # Return None if profile or profile image does not exist
        return None

# class UserCreateSerializer(UserCreateSerializer):
#     class Meta(UserCreateSerializer.Meta):
#         model = User
#         fields = ('id', 'email', 'name', 'password')
