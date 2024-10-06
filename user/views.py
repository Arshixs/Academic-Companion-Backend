from rest_framework import generics
from .models import User
from .serializers import UserSerializer

# Create User API
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# List all users API
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
