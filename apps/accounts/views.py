from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .adapters import CustomGoogleOAuth2Adapter
from django.conf import settings

from .filters import UserListFilter
from .models import UserAccount
from .paginations import StandardPagination

User = get_user_model()

class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return "redirect-url"


class UserListView(ListAPIView):
    serializer_class = UserDetailsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserListFilter
    pagination_class = StandardPagination
    ordering_fields = '__all__'
    queryset = UserAccount.objects.all()


class GoogleLogin(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
    callback_url = settings.GOOGLE_REDIRECT_URL
    client_class = OAuth2Client