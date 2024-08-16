
def get_upload_to(instance, filename):
    return f"{instance.owner.id}/uploads/{instance.folder.uuid}/{instance.uuid}_{filename.replace(' ', '_')}"
