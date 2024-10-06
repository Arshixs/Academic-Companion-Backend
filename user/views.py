from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer,EnrollmentSerializer
from college.serializers import CourseSerializer
from college.models import Course

# Create User API
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# List all users API
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EnrollmentCreateAPIView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        user_college = user.college  # Get the user's college
        
        # Get or create the course based on the request data
        course_name = self.request.data.get('course_name')
        course_id = self.request.data.get('course_id')

        try:
            # Check if the course exists in the user's college
            course = Course.objects.get(course_name=course_name, college=user_college)

            # If course exists, enroll the user
            serializer.save(user=user, course=course)

        except Course.DoesNotExist:
            # If course does not exist, ask for more details to create the course
            course_data = {
                'course_id': course_id,
                'course_name': course_name,
                'college': user_college.id
            }
            # Check if all course creation fields are provided
            if not course_id:
                raise ValidationError('Course does not exist in your college. Please provide a course_id to create the course.')

            # Create the course
            course_serializer = CourseSerializer(data=course_data)
            if course_serializer.is_valid():
                course = course_serializer.save()

                # Enroll the user in the newly created course
                serializer.save(user=user, course=course)
            else:
                # Return errors if the course creation data is invalid
                return Response(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST)