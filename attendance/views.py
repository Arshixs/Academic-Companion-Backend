from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from user.models import Enrollment
from .serializers import EnrollmentAttendanceSerializer

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
                "name": enrollment.course.course_name,
                "total_class": total_classes,
                "present": present_count,
                "absent": absent_count,
            })

        # Serialize the result
        serializer = AttendanceSummarySerializer(attendance_summary, many=True)
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

    
# Example view for fetching user details (GET request)
# class UserDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]  # Require authentication via JWT

#     def get(self, request, *args, **kwargs):
#         user = request.user  # This will be populated by JWT authentication
#         user_data = {
#             "id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "branch": user.branch,
#             "current_semester": user.current_semester,
#             "college": user.college.college_name if user.college else None,
#         }
#         return Response(user_data, status=200)
    
    