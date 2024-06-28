from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('list/', views.UserListView.as_view(), name="accounts-list")
]
