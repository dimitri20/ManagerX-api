from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.TaskListView.as_view(), name='task-list'),
    path('create/', views.TaskCreateView.as_view(), name='create-task'),
    path('<str:uuid>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('<str:uuid>/update/', views.TaskUpdateView.as_view(), name='update-task'),
    path('<str:uuid>/delete/', views.TaskDeleteView.as_view(), name='delete-task'),

    path('subtasks/list/', views.SubtaskListView.as_view(), name='task-list'),
    path('subtasks/create/', views.SubtaskCreateView.as_view(), name='create-task'),
    path('subtasks/<str:uuid>/', views.SubtaskDetailView.as_view(), name='task-detail'),
    path('subtasks/<str:uuid>/update/', views.SubtaskUpdateView.as_view(), name='update-task'),
    path('subtasks/<str:uuid>/delete/', views.SubtaskDeleteView.as_view(), name='delete-task'),

    path('subtasks/comments/create/', views.SubtaskCommentCreateView.as_view(), name='create-subtask-comment'),
    path('subtasks/comments/<str:uuid>/delete/', views.SubtaskCommentDeleteView.as_view(), name='delete-subtask-comment'),
]
