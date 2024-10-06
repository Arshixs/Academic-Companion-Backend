# core_app/urls.py
from django.urls import path
from .views import UserCreateAPIView, UserListAPIView, EnrollmentCreateAPIView

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('list/', UserListAPIView.as_view(), name='user-list'),
    path('enroll/create/', EnrollmentCreateAPIView.as_view(), name='enroll'),
]
