from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import User,Enrollment
from .serializers import UserSerializer,EnrollmentSerializer
from college.serializers import CourseSerializer
from college.models import Course,College
from rest_framework_simplejwt.tokens import RefreshToken

# Create User API
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# List all users API
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginAPIView(APIView):
    permission_classes = []  # Allow unauthenticated users to log in

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Fetch additional user data
            curr_user = User.objects.get(username=user.username)

            # Prepare user data to send in the response
            user_data = {
                "id": curr_user.id,
                "username": curr_user.username,
                "email": curr_user.email,
                "first_name": curr_user.first_name,
                "last_name": curr_user.last_name,
                "branch": curr_user.branch,
                "current_semester": curr_user.current_semester,
                "college": curr_user.college.college_name if curr_user.college else None,
            }

            return Response({
                "message": "Logged in successfully",
                "user_data": user_data,
                "refresh_token": str(refresh),
                "access_token": str(access_token)
            }, status=status.HTTP_200_OK)

        # If authentication fails
        return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

# Class-based Logout API View
class UserLogoutAPIView(APIView):
    permission_classes = []  # You can add permissions if required

    def post(self, request, *args, **kwargs):
        # Log the user out
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    

class UserProfileAPIView(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # User is authenticated, return user details
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # User is not authenticated
            return Response({"error": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN)



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
            
class UserCoursesAPIView(APIView):
    def get(self, request, user_id: int, *args, **kwargs):
        try:
            # Get all courses for the given user_id
            enrollments = Enrollment.objects.filter(user_id=user_id).select_related('course')
            courses = [enrollment.course for enrollment in enrollments]
            serializer = CourseSerializer(courses, many=True)  # Serialize course data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Enrollment.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)