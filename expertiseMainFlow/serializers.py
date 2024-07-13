from rest_framework import serializers
from .models import File, ExpertiseFolder, Tag


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class ExpertiseFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseFolder
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class ExpertiseFolderDetailsSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = ExpertiseFolder
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')

    def get_files(self, obj):
        return File.objects.get(folder=obj.uuid)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')
