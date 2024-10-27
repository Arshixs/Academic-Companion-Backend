from rest_framework import serializers
from .models import Attendance
from user.models import Enrollment

class AttendanceSummarySerializer(serializers.Serializer):
    course_id = serializers.CharField()
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
    
class AttendancePostSerializer(serializers.ModelSerializer):
    course_id = serializers.CharField(write_only=True)
    date = serializers.CharField(write_only=True)
    
    class Meta:
        model = Attendance
        fields = ['course_id', 'date', 'status']

    def validate(self, data):
        # Parse and validate date format
        try:
            data['attendance_date'] = datetime.strptime(data['date'], "%d/%m/%Y").date()
        except ValueError:
            raise serializers.ValidationError("Date format should be DD/MM/YYYY.")

        # Verify enrollment based on the course_id
        course_id = data.get('course_id')
        enrollment = Enrollment.objects.filter(course__course_id=course_id).first()
        if not enrollment:
            raise serializers.ValidationError("Enrollment with the given course_id does not exist.")
        
        data['enrollment'] = enrollment
        return data

    def create(self, validated_data):
        validated_data.pop('course_id')
        validated_data.pop('date')
        return Attendance.objects.create(**validated_data)