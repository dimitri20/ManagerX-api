from django.urls import path
from .views import files, folders, rclone

urlpatterns = [
    # path('folder/create/', folders.CreateExpertiseFolderView.as_view(), name='folder'),
    # path('folder/<str:uuid>/update/', folders.UpdateExpertiseFolderView.as_view(), name='update'),
    # path('folder/<str:uuid>/details/', folders.ExpertiseFolderDetailsView.as_view(), name='folder-details'),
    # path('folder/<str:uuid>/delete/', folders.DeleteExpertiseFolderView.as_view(), name='folder-delete'),
    # path('folder/list/', folders.ListExpertiseFolderView.as_view(), name='folder-list'),

    path('data/custom-fields/', folders.CustomFieldViewSet.as_view(), name='custom-fields'),
    path('data/create/', folders.CreateExpertiseDataView.as_view(), name='data'),
    path('data/create-expertise-data/', folders.FolderDataViewSet.as_view(), name='folder-data'),
    path('data/custom-fields/list/', folders.CustomFieldListViewSet.as_view(), name='custom-fields-list'),
    path('data/list/', folders.ListDataViewSet.as_view(), name='list-data'),

    path('attachment/upload/', files.UploadFileView.as_view(), name='upload-file'),
    # path('attachment/list/', files.ListFileView.as_view(), name='file-list'),
    # path('attachment/<uuid:uuid>/update/', files.UpdateFileView.as_view(), name='update-file'),
    # path('attachment/<uuid:uuid>/details/', files.FileDetailsView.as_view(), name='update-file'),
    path('attachment/<uuid:uuid>/delete/', files.DeleteFileView.as_view(), name='delete-file'),
    path('attachment/<uuid:uuid>/download/', files.DownloadFileView.as_view(), name='download-file'),

    path('rclone/uploadfile/', rclone.UploadFileView.as_view(), name='rclone-uploadfile'),
    path('rclone/list/', rclone.ListRemoteView.as_view(), name="list-file-rclone"),
    path('rclone/mkdir/', rclone.RcloneMkDirView.as_view(), name="mkdir-file-rclone"),
    path('rclone/movefile/', rclone.RcloneMoveFileView.as_view(), name="mv-file-rclone"),
    path('rclone/publiclink/', rclone.RclonePublicLinkView.as_view(), name="pub-link-rclone"),

    # path('email/<str:name>/messages/list/', views.EMailMessagesListView.as_view(), name='email-messages-list'),
    # path('email/messages/import-files/', views.ImportAttachmentsFromMail.as_view(), name='email-import-files'),
    # path('email/<str:name>/fetch/', views.FetchMailWithServer.as_view(), name='fetch-mail'),
]
