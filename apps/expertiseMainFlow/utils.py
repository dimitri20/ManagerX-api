from django.conf import settings


# def get_upload_to(instance, filename):
#     return f"{instance.owner.id}/uploads/{instance.folder.uuid}/{instance.uuid}_{filename.replace(' ', '_')}"


def get_upload_to(instance, filename):
    return f"{settings.GDRIVE_UPLOADS_PATH}/{filename.replace(' ', '_')}"
