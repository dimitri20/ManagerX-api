from django.urls import path
from . import views

urlpatterns = [
    path('folder/', views.CreateExpertiseFolderView.as_view(), name='folder'),
    path('folder/<str:uuid>/details/', views.ExpertiseFolderDetailsView.as_view(), name='folder-details'),
    path('file/', views.UploadFileView.as_view(), name='upload-file'),
    path('folder/list/', views.ListExpertiseFolderView.as_view(), name='folder-list'),
    path('folder/custom-fields/', views.CustomFieldViewSet.as_view(), name='custom-fields'),
    path('folder/folder-data/', views.FolderDataViewSet.as_view(), name='folder-data'),
    path('folder/custom-fields/list/', views.CustomFieldListViewSet.as_view(), name='custom-fields-list'),

    path('email/<str:name>/messages/list/', views.EMailMessagesListView.as_view(), name='email-messages-list'),
    path('email/messages/import-files/', views.ImportAttachmentsFromMail.as_view(), name='email-import-files'),
    path('email/<str:name>/fetch/', views.FetchMailWithServer.as_view(), name='fetch-mail'),
]
