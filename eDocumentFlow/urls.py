from django.urls import path
from . import views

urlpatterns = [
    path('document/upload/', views.UploadDocumentView.as_view(), name='upload-document'),
    path('document/sign/', views.SignDocumentView.as_view(), name='sign-document'),
    path('document/verify/', views.VerifyDocumentView.as_view(), name='verify-document'),
    path('task/create/', views.RegisterTaskView.as_view(), name='register-task')
]
