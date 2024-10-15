from rest_framework import serializers

class RemoteItemSerializer(serializers.Serializer):
    Path = serializers.CharField()
    Name = serializers.CharField()
    Size = serializers.IntegerField()
    MimeType = serializers.CharField()
    ModTime = serializers.DateTimeField()
    IsDir = serializers.BooleanField()
    ID = serializers.CharField()

class ListRemoteResponseSerializer(serializers.Serializer):
    list = RemoteItemSerializer(many=True)

class PublicLinkResponseSerializer(serializers.Serializer):
    url = serializers.URLField()
