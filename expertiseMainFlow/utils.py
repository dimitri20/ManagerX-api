import dcs.settings


def get_upload_to(instance, filename):
    return f"uploads/{instance.folder.path}{filename}"
