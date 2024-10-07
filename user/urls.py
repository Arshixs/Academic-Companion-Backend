# core_app/urls.py
from django.urls import path
from .views import UserCreateAPIView, UserListAPIView, EnrollmentCreateAPIView,UserLoginAPIView, UserLogoutAPIView, UserProfileAPIView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user_logout'),
    path('user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('list/', UserListAPIView.as_view(), name='user-list'),
    path('enroll/create/', EnrollmentCreateAPIView.as_view(), name='enroll'),
]
