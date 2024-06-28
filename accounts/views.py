from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import UserAccount
from djoser.serializers import UserSerializer
from rest_framework.response import Response


# Create your views here.

class UserListView(ListAPIView):
    serializer_class = UserAccount

    def get(self, request, *args, **kwargs):
        users = UserAccount.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
