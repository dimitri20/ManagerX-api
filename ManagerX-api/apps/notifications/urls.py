from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.NotificationListView.as_view(), name='notification-list'),
    path('<uuid:uuid>/', views.NotificationDetailsView.as_view(), name='notification-mark-as-read'),
    path('<uuid:uuid>/update/', views.NotificationUpdateView.as_view(), name='task-list'),
    path('<uuid:uuid>/delete/', views.NotificationDeleteView.as_view(), name='task-list'),
    path('user/<uuid:user_id>/list/', views.UserNotificationsListView.as_view(), name='user_notifications_list'),
]
