from django.urls import path
from .views import files, folders, rclone

urlpatterns = [
    path('data/custom-fields/', folders.CustomFieldViewSet.as_view(), name='custom-fields'),
    path('data/custom-fields/<id:int>/edit/', folders.UpdateCustomFieldViewSet.as_view(), name='custom-fields-update'),
    path('data/create/', folders.CreateExpertiseDataView.as_view(), name='data'),
    path('data/create-expertise-data/', folders.FolderDataViewSet.as_view(), name='folder-data'),
    path('data/custom-fields/list/', folders.CustomFieldListViewSet.as_view(), name='custom-fields-list'),
    path('data/list/', folders.ListDataViewSet.as_view(), name='list-data'),

    path('attachment/upload/', files.UploadFileView.as_view(), name='upload-file'),
    path('attachment/<uuid:uuid>/delete/', files.DeleteFileView.as_view(), name='delete-file'),
    path('attachment/<uuid:uuid>/download/', files.DownloadFileView.as_view(), name='download-file'),

    path('rclone/uploadfile/', rclone.UploadFileView.as_view(), name='rclone-uploadfile'),
    path('rclone/list/', rclone.ListRemoteView.as_view(), name="list-file-rclone"),
    path('rclone/mkdir/', rclone.RcloneMkDirView.as_view(), name="mkdir-file-rclone"),
    path('rclone/movefile/', rclone.RcloneMoveFileView.as_view(), name="mv-file-rclone"),
    path('rclone/publiclink/', rclone.RclonePublicLinkView.as_view(), name="pub-link-rclone"),
    path('rclone/generate-conclusion/', rclone.GenerateConclusionView.as_view(), name="generate-conclusion"),
    path('rclone/share-folder/', rclone.ShareFolderWithUserView.as_view(), name="share-folder"),
]
