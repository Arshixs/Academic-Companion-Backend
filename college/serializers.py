from rest_framework import serializers
from .models import College

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['college_name', 'college_location']
