from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.TaskListView.as_view(), name='task-list'),
    path('create/', views.TaskCreateView.as_view(), name='create-task'),
    path('<uuid:uuid>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('<uuid:uuid>/update/', views.TaskUpdateView.as_view(), name='update-task'),
    path('<uuid:uuid>/delete/', views.TaskDeleteView.as_view(), name='delete-task'),

    path('subtasks/list/', views.SubtaskListView.as_view(), name='task-list'),
    path('subtasks/create/', views.SubtaskCreateView.as_view(), name='create-task'),
    path('subtasks/<uuid:uuid>/', views.SubtaskDetailView.as_view(), name='task-detail'),
    path('subtasks/<uuid:uuid>/update/', views.SubtaskUpdateView.as_view(), name='update-task'),
    path('subtasks/<uuid:uuid>/delete/', views.SubtaskDeleteView.as_view(), name='delete-task'),

    path('subtasks/comments/create/', views.SubtaskCommentCreateView.as_view(), name='create-subtask-comment'),
    path('subtasks/comments/<uuid:uuid>/edit/', views.SubtaskCommentUpdateView.as_view(), name='update-subtask-comment'),
    path('subtasks/comments/<uuid:uuid>/delete/', views.SubtaskCommentDeleteView.as_view(), name='delete-subtask-comment'),

    path('notes/list/', views.NoteListView.as_view(), name='note-list'),
    path('notes/create/', views.NoteCreateView.as_view(), name='note-create'),
    path('notes/<uuid:uuid>/', views.NoteDetailView.as_view(), name='note-detail'),
    path('notes/<uuid:uuid>/update/', views.NoteUpdateView.as_view(), name='note-update'),
    path('notes/<uuid:uuid>/delete', views.NoteDetailView.as_view(), name='note-detail'),
]
