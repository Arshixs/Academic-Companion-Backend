from rest_framework import serializers
from .models import Attendance
from user.models import Enrollment

class AttendanceSummarySerializer(serializers.Serializer):
    name = serializers.CharField()
    total_class = serializers.IntegerField()
    present = serializers.IntegerField()
    absent = serializers.IntegerField()


from .models import Attendance
from user.models import Enrollment

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['attendance_date', 'status']

class EnrollmentAttendanceSerializer(serializers.ModelSerializer):
    # Nested serializer for the attendance records
    attendance_records = serializers.SerializerMethodField()

    # Get course_id from the related Course model
    course_id = serializers.CharField(source='course.course_id')

    class Meta:
        model = Enrollment
        fields = ['course_id', 'attendance_records']

    def get_attendance_records(self, obj):
        # Get all attendance records for the enrollment and format the data
        attendance = Attendance.objects.filter(enrollment=obj).order_by('attendance_date')
        return {record.attendance_date.strftime('%Y-%m-%d'): record.status for record in attendance}