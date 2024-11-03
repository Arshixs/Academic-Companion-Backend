from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import College, Course
from .serializers import CollegeSerializer, CourseSerializer
from user.models import Enrollment

class CollegeCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Add JWT authentication requirement
    
    def post(self, request, *args, **kwargs):
        serializer = CollegeSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Failed to create college"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CourseCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic  # Use transaction to ensure both course creation and enrollment succeed or fail together
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            try:
                college = College.objects.get(user=user)
            except College.DoesNotExist:
                return Response(
                    {"error": "No college associated with this user"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if the course already exists for this college
            course_id = request.data.get('course_id')
            course_name = request.data.get('course_name')
            
            course = None
            created = False
            
            # Try to get existing course or create new one
            try:
                course = Course.objects.get(
                    course_id=course_id,
                    college=college
                )
            except Course.DoesNotExist:
                # Create new course
                serializer = CourseSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    course = serializer.save()
                    created = True
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Try to enroll the user in the course
            try:
                enrollment, enrollment_created = Enrollment.objects.get_or_create(
                    user=user,
                    course=course
                )
                
                response_data = CourseSerializer(course).data
                response_data['enrollment_status'] = 'enrolled'
                response_data['enrollment_created'] = enrollment_created
                
                status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
                message = 'Course created and enrolled successfully' if created else 'Course exists and enrolled successfully'
                
                return Response({
                    'message': message,
                    'course': response_data
                }, status=status_code)
                
            except Exception as e:
                return Response({
                    'error': 'Failed to enroll in the course',
                    'detail': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except ValidationError as e:
            return Response(
                {"error": str(e.detail)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Something went wrong. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CourseListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Add JWT authentication requirement
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        """
        Override get_queryset to only return courses for the user's college
        """
        try:
            # Get the user's associated college
            college = College.objects.get(user=self.request.user)  # Modify based on your user-college relationship
            return Course.objects.filter(college=college)
        except College.DoesNotExist:
            return Course.objects.none()
    
    def handle_exception(self, exc):
        return Response({
            "error": "Something went wrong. Please try again later."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)