from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet

router = DefaultRouter()
router.register(r'note', NoteViewSet, basename='note')  # Use 'note' without 'notes'

urlpatterns = [
    path('', include(router.urls)),
]
