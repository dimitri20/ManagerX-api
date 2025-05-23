from rest_framework import serializers

class BaseRemoteRequestSerializer(serializers.Serializer):
    fs = serializers.CharField(required=True)
    remote = serializers.CharField(default="", required=False, allow_blank=True)

    def validate_fs(self, value):
        # Example validation (you can customize this)
        if not value.endswith(':'):
            raise serializers.ValidationError("The fs field must end with a colon (e.g., 'drive:').")
        return value

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

class FileUploadSerializer(BaseRemoteRequestSerializer):
    file = serializers.FileField(required=True)

class GenerateConclusionRequestSerializer(serializers.Serializer):
    task = serializers.UUIDField(required=True)
    conclusionNumber = serializers.CharField(max_length=255, required=True)

class ShareFolderRequestSerializer(serializers.Serializer):
    folder_path = serializers.CharField(max_length=255, required=True)
    user_id = serializers.UUIDField(required=True)
