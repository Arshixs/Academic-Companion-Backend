from django.urls import path
from .views import UserAttendanceAPIView,UserAttendanceDetailedView

urlpatterns = [
    path('data/', UserAttendanceAPIView.as_view(), name='user-attendance'),
    path('detailed/', UserAttendanceDetailedView.as_view(), name='attendance-for-user'),
]
