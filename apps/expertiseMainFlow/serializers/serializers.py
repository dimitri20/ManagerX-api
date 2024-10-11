from rest_framework import serializers
from apps.expertiseMainFlow.models import File, ExpertiseFolder, Tag, CustomField, ExpertiseAdditionalData, \
    ExpertiseData
from django_mailbox.models import Message, Mailbox
from django_mailbox.models import MessageAttachment


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('uuid', 'title', 'owner', 'created_at', 'updated_at')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class EmailMessageAttachmentSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()

    class Meta:
        model = MessageAttachment
        fields = '__all__'

    def get_filename(self, obj):
        return obj.get_filename()


class EmailSerializer(serializers.ModelSerializer):
    attachments = EmailMessageAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        exclude = ('body',)

    def get_attachments(self, obj):
        return EmailMessageAttachmentSerializer.objects.get(message_id=obj.id)


class ImportAttachmentsFromMailSerializer(serializers.Serializer):
    email_id = serializers.IntegerField()
    copy_to_folder_id = serializers.CharField(max_length=255, allow_blank=False, allow_null=False)



class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    """
    Based on https://stackoverflow.com/a/62579804
    """

    def __init__(self, method_name=None, *args, **kwargs):
        self.method_name = method_name
        kwargs["source"] = "*"
        super(serializers.SerializerMethodField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}


class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = ['id', 'name', 'data_type']


class KeyValuePairSerializer(serializers.Serializer):
    field = serializers.PrimaryKeyRelatedField(queryset=CustomField.objects.all())
    value = ReadWriteSerializerMethodField(allow_null=True)


class FolderDataCreateSerializer(serializers.Serializer):
    expertise_data = serializers.PrimaryKeyRelatedField(queryset=ExpertiseData.objects.all())
    key_value_pair = KeyValuePairSerializer(many=True)

    def create_or_update_folder_data(self, expertise_data, key_value_pair):
        type_to_data_store_name_map = {
            CustomField.FieldDataType.STRING: "value_string",
            CustomField.FieldDataType.URL: "value_url",
            CustomField.FieldDataType.DATE: "value_date",
            CustomField.FieldDataType.BOOL: "value_bool",
            CustomField.FieldDataType.INT: "value_int",
            CustomField.FieldDataType.FLOAT: "value_float",
        }

        instances = []
        for pair in key_value_pair:
            custom_field = pair.get('field')
            value = pair.get('value')
            data_store_name = type_to_data_store_name_map[custom_field.data_type]

            instance, _ = ExpertiseAdditionalData.objects.update_or_create(
                expertise_data=expertise_data,
                field=custom_field,
                defaults={data_store_name: value},
            )
            instances.append(instance)
        return instances

    def get_value(self, obj: ExpertiseAdditionalData):
        return obj.value


class FolderDataSerializer(serializers.ModelSerializer):
    value = ReadWriteSerializerMethodField(allow_null=True)
    field = CustomFieldSerializer(read_only=True)

    class Meta:
        model = ExpertiseAdditionalData
        fields = ['field', 'value']

    def get_value(self, obj: ExpertiseAdditionalData):
        return obj.value

class ExpertiseDataCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseData
        fields = '__all__'
        read_only_fields = ('uuid',)

class ExpertiseDataSerializer(serializers.ModelSerializer):
    custom_fields = FolderDataSerializer(many=True, read_only=True)

    class Meta:
        model = ExpertiseData
        fields = '__all__'
        read_only_fields = ('uuid', 'custom_fields', )
        depth = 1

class ExpertiseFolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpertiseFolder
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')

    def get_custom_fields(self, obj):
        return ExpertiseAdditionalData.objects.get(expertise_folder=obj.uuid)

    def validate_title(self, value):
        # Get the user from the context (provided in the view)
        user = self.context['request'].user

        # Check if the title already exists for this user
        if ExpertiseFolder.objects.filter(owner=user, title=value).exists():
            raise serializers.ValidationError('This title already exists for this user.')

        return value



class ExpertiseFolderDetailsSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = ExpertiseFolder
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')

    def get_files(self, obj):
        return File.objects.get(folder=obj.uuid)

    def get_custom_fields(self, obj):
        return ExpertiseAdditionalData.objects.get(expertise_folder=obj.uuid)


class ExpertiseFolderSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseFolder
        fields = ['uuid', 'title']
