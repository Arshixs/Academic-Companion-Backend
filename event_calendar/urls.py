from django.urls import path
from .views import CalendarEventViewSet

urlpatterns = [
    path('', CalendarEventViewSet.as_view({'get': 'list', 'post': 'create'}), name='event-list'),
    path('<int:pk>/', CalendarEventViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='event-detail'),
]