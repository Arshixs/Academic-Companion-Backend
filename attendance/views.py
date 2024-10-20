from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance, Enrollment
from .serializers import AttendanceSummarySerializer

class UserAttendanceAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        enrollments = Enrollment.objects.filter(user_id=user_id)
        attendance_summary = []

        # Loop through each enrolled course
        for enrollment in enrollments:
            attendance_records = Attendance.objects.filter(enrollment=enrollment)
            present_count = attendance_records.filter(status='present').count()
            absent_count = attendance_records.filter(status='absent').count()
            total_classes = present_count+absent_count

            attendance_summary.append({
                "name": enrollment.course.course_name,
                "total_class": total_classes,
                "present": present_count,
                "absent": absent_count,
            })

        # Serialize the result
        serializer = AttendanceSummarySerializer(attendance_summary, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
