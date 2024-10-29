# core_app/urls.py
from django.urls import path
from .views import UserCreateAPIView, UserListAPIView, EnrollmentCreateAPIView,UserLoginAPIView, UserLogoutAPIView, UserProfileAPIView, UserCoursesAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', UserLogoutAPIView.as_view(), name='user_logout'),
    path('user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    # path('list/', UserListAPIView.as_view(), name='user-list'),
    path('enroll/create/', EnrollmentCreateAPIView.as_view(), name='enroll'),
    path('courses/<int:user_id>/', UserCoursesAPIView.as_view(), name='user-courses'), 

]
