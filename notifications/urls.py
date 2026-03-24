from django.urls import path
from .views import NotificationListView, NotificationMarkReadView, mark_read



app_name = 'notifications'

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('<int:id>/read/', NotificationMarkReadView.as_view(), name='notifications-mark-read'),
    path('mark_read/<int:id>/', mark_read, name='mark_read'),
]