from rest_framework import serializers
from .models import CalendarEvent

class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = ['id', 'title', 'description', 'date', 'start_time', 
                 'end_time', 'color', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']