from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserCreateAPIView,
    UserListAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserProfileAPIView,
    UserCoursesAPIView,
    EnrollmentCreateAPIView,
    CollegeUsersAPIView,
)

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('courses/', UserCoursesAPIView.as_view(), name='user-courses'),
    path('enroll/', EnrollmentCreateAPIView.as_view(), name='course-enroll'),
    path('college-users/', CollegeUsersAPIView.as_view(), name='college-users'),
]