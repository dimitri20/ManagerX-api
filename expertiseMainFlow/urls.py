from django.urls import path
from . import views

urlpatterns = [
    path('expertise/folder/', views.CreateExpertiseFolderView.as_view(), name='folder'),
    path('expertise/folder/<str:uuid>/details/', views.ExpertiseFolderDetailsView.as_view(), name='folder-details'),
    path('expertise/file/', views.UploadFileView.as_view(), name='upload-file'),
    path('expertise/folder/list/', views.ListExpertiseFolderView.as_view(), name='folder-list'),
    path('email/<str:name>/messages/list/', views.EMailMessagesListView.as_view(), name='email-messages-list'),
    path('email/messages/import-files/', views.ImportAttachmentsFromMail.as_view(), name='email-import-files'),
    path('email/<str:name>/fetch/', views.FetchMailWithServer.as_view(), name='fetch-mail')
]
