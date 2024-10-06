from django.urls import path
from .views import CollegeCreateAPIView

urlpatterns = [
    path('create/', CollegeCreateAPIView.as_view(), name='college-create'),
]
