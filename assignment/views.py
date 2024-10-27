from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import IntegrityError
from .serializers import LabelSerializer,AssignmentSerializer
from .models import Label,Assignment
from rest_framework import serializers
from django.db.models import Count  # Added this import

# Now, let's create the views
class LabelViewSet(viewsets.ModelViewSet):
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Label.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError(
                {"name": "A label with this name already exists for your account."}
            )

    @action(detail=False, methods=['get'])
    def all_labels(self, request):
        labels = self.get_queryset().values_list('name', flat=True)
        return Response(labels)

class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Assignment.objects.filter(user=self.request.user)
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
            
        # Filter by priority
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
            
        # Filter by label
        label = self.request.query_params.get('label', None)
        if label:
            queryset = queryset.filter(label__name=label)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total_assignments = self.get_queryset().count()
        by_status = self.get_queryset().values('status').annotate(count=Count('id'))
        by_priority = self.get_queryset().values('priority').annotate(count=Count('id'))
        
        return Response({
            'total': total_assignments,
            'by_status': by_status,
            'by_priority': by_priority
        })