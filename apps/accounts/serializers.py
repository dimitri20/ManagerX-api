from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.serializers import LoginSerializer

User = get_user_model()

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User  # Use your custom user model
        fields = ('id', 'username', 'email', 'first_name', 'last_name', )  # Add your custom fields



# class UserCreateSerializer(UserCreateSerializer):
#     class Meta(UserCreateSerializer.Meta):
#         model = User
#         fields = ('id', 'email', 'name', 'password')
