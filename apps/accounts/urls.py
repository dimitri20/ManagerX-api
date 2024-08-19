from django.urls import include
from django.urls import path

from .views import GoogleLogin, UserListView

# path('auth/registration/', include('dj_rest_auth.registration.urls')), - registration urls

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('accounts/', include('allauth.urls')),
    path('users/list/', UserListView.as_view(), name='users_list'),
]
