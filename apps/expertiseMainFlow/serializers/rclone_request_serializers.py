from rest_framework import serializers

class BaseRemoteRequestSerializer(serializers.Serializer):
    fs = serializers.CharField(required=True)
    remote = serializers.CharField(default="", required=False, allow_blank=True)

class ListRemoteOptionsSerializer(serializers.Serializer):
    recurse = serializers.BooleanField(required=False, default=False)
    noModTime = serializers.BooleanField(required=False, default=False)
    showEncrypted = serializers.BooleanField(required=False, default=False)
    showOrigIDs = serializers.BooleanField(required=False, default=False)
    showHash = serializers.BooleanField(required=False, default=False)
    noMimeType = serializers.BooleanField(required=False, default=False)
    dirsOnly = serializers.BooleanField(required=False, default=False)
    filesOnly = serializers.BooleanField(required=False, default=False)
    metadata = serializers.BooleanField(required=False, default=False)
    hashTypes = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )

class ListRemoteRequestSerializer(BaseRemoteRequestSerializer):
    opt = ListRemoteOptionsSerializer(required=False)

class MoveFileRequestSerializer(serializers.Serializer):
    srcFs = serializers.CharField(max_length=255)
    srcRemote = serializers.CharField(max_length=255)
    dstFs = serializers.CharField(max_length=255)
    dstRemote = serializers.CharField(max_length=255)

class PublicLinkRequestSerializer(BaseRemoteRequestSerializer):
    unlink = serializers.BooleanField(required=False, default=False)
    expire = serializers.CharField(default="", required=False, allow_blank=True)
