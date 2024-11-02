from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Enrollment
from .serializers import UserSerializer, EnrollmentSerializer
from college.serializers import CourseSerializer
from college.models import Course

class UserCreateAPIView(generics.CreateAPIView):
    """
    API view for user registration
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "Registration successful",
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListAPIView(generics.ListAPIView):
    """
    API view to list all users (admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow staff/admin to see all users
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.none()

class UserLoginAPIView(APIView):
    """
    API view for user login
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                "error": "Username and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            
            return Response({
                "message": "Login successful",
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        return Response({
            "error": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutAPIView(APIView):
    """
    API view for user logout
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "message": "Logout successful"
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "error": "Invalid token"
            }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(APIView):
    """
    API view for user profile operations
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCoursesAPIView(APIView):
    """
    API view to get user's enrolled courses
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
        courses = [enrollment.course for enrollment in enrollments]
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class EnrollmentCreateAPIView(generics.CreateAPIView):
    """
    API view for course enrollment
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        course_name = self.request.data.get('course_name')
        
        try:
            course = Course.objects.get(
                course_name=course_name, 
                college=user.college
            )
            serializer.save(user=user, course=course)
        except Course.DoesNotExist:
            raise serializers.ValidationError({
                "error": f"Course '{course_name}' does not exist in your college."
            })

# Optional: Add API view for searching users by college
class CollegeUsersAPIView(generics.ListAPIView):
    """
    API view to list users from a specific college
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        college_name = self.request.query_params.get('college_name')
        if college_name:
            return User.objects.filter(college__college_name=college_name)
        return User.objects.none()