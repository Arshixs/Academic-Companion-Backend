from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CalendarEvent
from .serializers import CalendarEventSerializer
from rest_framework.response import Response
from datetime import datetime
from rest_framework.decorators import action
from rest_framework import status

class CalendarEventViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter events for the current user
        return CalendarEvent.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Save the event with the authenticated user as the creator
        serializer.save(created_by=self.request.user)

    # List all events for the authenticated user
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Retrieve a single event by ID
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Create a new event
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Update an event (all fields)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # Partial update an event (only specified fields)
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # Delete an event
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Custom action to retrieve events for a specific month
    @action(detail=False, methods=['get'])
    def month_events(self, request):
        # Extract year and month from the request, defaulting to the current date
        year = int(request.query_params.get('year', datetime.now().year))
        month = int(request.query_params.get('month', datetime.now().month))

        # Filter events by year and month
        events = self.get_queryset().filter(
            date__year=year,
            date__month=month
        )
        
        # Serialize the data and return it in the response
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
