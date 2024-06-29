from django.urls import path
from . import views

urlpatterns = [
    path('document/upload/', views.UploadDocumentView.as_view(), name='upload-document'),
    path('document/sign/', views.SignDocumentView.as_view(), name='sign-document'),
    path('document/verify/', views.VerifyDocumentView.as_view(), name='verify-document'),
    path('document/send-to-verify/', views.SendToVerifyDocumentView.as_view(), name='send-to-verify'),
    path('document/send-to-sign/', views.SendToSignDocumentView.as_view(), name='send-to-sign'),
    path('task/create/', views.RegisterTaskView.as_view(), name='register-task'),

    path('document/list/', views.DocumentListView.as_view(), name='document-list'),
    path('document/<str:uuid>/', views.DocumentDetailView.as_view(), name='document-details'),
]
