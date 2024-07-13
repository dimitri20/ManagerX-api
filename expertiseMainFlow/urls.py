from django.urls import path
from . import views

urlpatterns = [
    path('expertise/folder/', views.CreateExpertiseFolderView.as_view(), name='folder'),
    path('expertise/folder/<str:uuid>/details/', views.ExpertiseFolderDetailsView.as_view(), name='folder-details'),
    path('expertise/file/', views.UploadFileView.as_view(), name='upload-file'),
    path('expertise/folder/list/', views.ListExpertiseFolderView.as_view(), name='folder-list'),
    path('email/test/', views.SendEmailTestView.as_view(), name='email-test')
]
