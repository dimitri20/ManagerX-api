from django.urls import path
from .views import files, folders, backup

urlpatterns = [
    path('folder/create/', folders.CreateExpertiseFolderView.as_view(), name='folder'),
    path('folder/<str:uuid>/update/', folders.UpdateExpertiseFolderView.as_view(), name='update'),
    path('folder/<str:uuid>/details/', folders.ExpertiseFolderDetailsView.as_view(), name='folder-details'),
    path('folder/<str:uuid>/delete/', folders.DeleteExpertiseFolderView.as_view(), name='folder-delete'),
    path('folder/list/', folders.ListExpertiseFolderView.as_view(), name='folder-list'),
    path('folder/custom-fields/', folders.CustomFieldViewSet.as_view(), name='custom-fields'),
    path('folder/folder-data/', folders.FolderDataViewSet.as_view(), name='folder-data'),
    path('folder/custom-fields/list/', folders.CustomFieldListViewSet.as_view(), name='custom-fields-list'),

    path('file/upload/', files.UploadFileView.as_view(), name='upload-file'),
    path('file/list/', files.ListFileView.as_view(), name='file-list'),
    path('file/<uuid:uuid>/update/', files.UpdateFileView.as_view(), name='update-file'),
    path('file/<uuid:uuid>/details/', files.FileDetailsView.as_view(), name='update-file'),
    path('file/<uuid:uuid>/delete/', files.DeleteFileView.as_view(), name='delete-file'),
    path('file/<uuid:uuid>/download/', files.DownloadFileView.as_view(), name='download-file'),

    path('rclone/upload/', backup.RcloneUploadView.as_view(), name="upload-file-rclone"),
    path('rclone/list/', backup.ListRemoteView.as_view(), name="list-file-rclone")
    # path('email/<str:name>/messages/list/', views.EMailMessagesListView.as_view(), name='email-messages-list'),
    # path('email/messages/import-files/', views.ImportAttachmentsFromMail.as_view(), name='email-import-files'),
    # path('email/<str:name>/fetch/', views.FetchMailWithServer.as_view(), name='fetch-mail'),
]
