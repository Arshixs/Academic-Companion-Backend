# core_app/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # Add password field explicitly with write-only permission
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'branch', 'current_semester', 'college', 'created_at', 'password']

    # Override the create method to hash the password
    def create(self, validated_data):
        # Remove the password from the validated data
        password = validated_data.pop('password', None)
        # Create a new User instance without the password
        instance = self.Meta.model(**validated_data)
        if password is not None:
            # Set the hashed password using set_password
            instance.set_password(password)
        # Save the user instance
        instance.save()
        return instance
