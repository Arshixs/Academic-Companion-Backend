# First, let's create serializers
from rest_framework import serializers
from .models import Label,Assignment

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class AssignmentSerializer(serializers.ModelSerializer):
    label_name = serializers.CharField(source='label.name', read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'status', 'priority', 
                 'label', 'label_name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
