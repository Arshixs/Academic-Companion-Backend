from django.urls import path
from .views import LabelViewSet, AssignmentViewSet

urlpatterns = [
    # Label URLs
    path('labels/', LabelViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='label-list'),
    
    path('labels/<int:pk>/', LabelViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='label-detail'),
    
    path('labels/all_labels/', LabelViewSet.as_view({
        'get': 'all_labels'
    }), name='all-labels'),

    # Assignment URLs
    path('assignments/', AssignmentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='assignment-list'),
    
    path('assignments/<int:pk>/', AssignmentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='assignment-detail'),
    
    path('assignments/statistics/', AssignmentViewSet.as_view({
        'get': 'statistics'
    }), name='assignment-statistics'),
]