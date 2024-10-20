from django.urls import path
from .views import UserAttendanceAPIView

urlpatterns = [
    path('<int:user_id>/', UserAttendanceAPIView.as_view(), name='user-attendance'),
]
