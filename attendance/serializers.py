from rest_framework import serializers
from .models import Attendance

class AttendanceSummarySerializer(serializers.Serializer):
    name = serializers.CharField()
    total_class = serializers.IntegerField()
    present = serializers.IntegerField()
    absent = serializers.IntegerField()
