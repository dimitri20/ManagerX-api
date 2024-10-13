# your custom adapter file
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework.serializers import ValidationError

class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):

    def complete_login(self, request, app, token, **kwargs):
        login = super().complete_login(request, app, token, **kwargs)

        # if not login.user.is_superuser:
        #     raise ValidationError("This user is not a superuser.")

        return login