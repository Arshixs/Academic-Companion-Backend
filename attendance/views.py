from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from user.models import Enrollment
from .serializers import EnrollmentAttendanceSerializer,AttendancePostSerializer
from django.shortcuts import get_object_or_404
from datetime import datetime


from .models import Attendance, Enrollment
from .serializers import AttendanceSummarySerializer

class UserAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication via JWT

    def get(self, request, *args, **kwargs):
        # Get the authenticated user from the JWT token
        user = request.user

        # Filter enrollments based on the authenticated user's ID
        enrollments = Enrollment.objects.filter(user_id=user.id)
        attendance_summary = []

        # Loop through each enrolled course
        for enrollment in enrollments:
            attendance_records = Attendance.objects.filter(enrollment=enrollment)
            present_count = attendance_records.filter(status='present').count()
            absent_count = attendance_records.filter(status='absent').count()
            total_classes = present_count + absent_count

            attendance_summary.append({
                "course_id": enrollment.course.course_id,
                "name": enrollment.course.course_name,
                "total_class": total_classes,
                "present": present_count,
                "absent": absent_count,
            })
        # Serialize the result
        serializer = AttendanceSummarySerializer(attendance_summary, many=True)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UserAttendanceDetailedView(APIView):
    permission_classes = [IsAuthenticated]  # Require JWT authentication

    def get(self, request, *args, **kwargs):
        # Get the authenticated user from the JWT token
        user = request.user
        
        # Filter enrollments based on the authenticated user's ID
        enrollments = Enrollment.objects.filter(user_id=user.id)

        # Serialize the data
        serializer = EnrollmentAttendanceSerializer(enrollments, many=True)

        # Prepare the final dictionary structure with course_id as keys
        attendance_data = {item['course_id']: item['attendance_records'] for item in serializer.data}

        return Response(attendance_data)
    
class AttendanceCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Require JWT authentication
    
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        date_str = request.data.get("date")
        status_str = request.data.get("status")

        # Parse date format from DD/MM/YYYY to YYYY-MM-DD
        try:
            attendance_date = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use DD/MM/YYYY."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if enrollment exists for the given user and course
        enrollment = Enrollment.objects.filter(user=user, course__course_id=course_id).first()
        if not enrollment:
            return Response({"error": "Enrollment not found for this course and user."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create or update attendance record
        attendance, created = Attendance.objects.update_or_create(
            enrollment=enrollment,
            attendance_date=attendance_date,
            defaults={"status": status_str.lower()}
        )
        
        return Response(
            {"message": "Attendance created" if created else "Attendance updated"},
            status=status.HTTP_201_CREATED
        )