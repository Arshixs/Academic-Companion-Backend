from django.urls import path
from .views import CollegeCreateAPIView,CourseCreateAPIView,CourseListAPIView

urlpatterns = [
    path('create/', CollegeCreateAPIView.as_view(), name='college-create'),
    path('course/create/', CourseCreateAPIView.as_view(), name='course-create'),
    path('course/list/', CourseListAPIView.as_view(), name='course-list'),
]
