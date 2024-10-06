from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from .models import College,Course
from .serializers import CollegeSerializer,CourseSerializer

class CollegeCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CollegeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def handle_exception(self, exc):
        # Handle validation errors gracefully
        if isinstance(exc, ValidationError):
            return Response({
                "error": exc.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        # Handle any unexpected server errors
        return Response({
            "error": "Something went wrong. Please try again later."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def handle_exception(self, exc):
        return Response({
            "error": "Something went wrong. Please try again later."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



