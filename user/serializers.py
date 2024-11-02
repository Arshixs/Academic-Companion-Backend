# core_app/serializers.py
from rest_framework import serializers
from .models import User,Enrollment

from rest_framework import serializers
from .models import User, Enrollment
from college.models import College
from college.serializers import CollegeSerializer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    college_name = serializers.CharField(write_only=True)
    college_location = serializers.CharField(write_only=True)
    college = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'branch',
            'current_semester',
            'college',
            'college_name',
            'college_location',
            'created_at',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'college': {'read_only': True}
        }

    def get_college(self, obj):
        """Return college name for read operations"""
        return obj.college.college_name if obj.college else None

    def validate_college_name(self, value):
        """Validate college name or prepare for creation"""
        return value

    def create(self, validated_data):
        # Extract college data
        college_name = validated_data.pop('college_name')
        college_location = validated_data.pop('college_location')
        password = validated_data.pop('password', None)
        
        # Try to get existing college or create new one
        try:
            college = College.objects.get(college_name=college_name)
        except College.DoesNotExist:
            # Create new college using CollegeSerializer
            college_serializer = CollegeSerializer(data={
                'college_name': college_name,
                'college_location': college_location
            })
            if college_serializer.is_valid():
                college = college_serializer.save()
            else:
                raise serializers.ValidationError({
                    'college_error': college_serializer.errors
                })

        # Create user instance
        instance = self.Meta.model(
            college=college,
            **validated_data
        )
        
        if password is not None:
            instance.set_password(password)
            
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        # Handle college update if provided
        college_name = validated_data.pop('college_name', None)
        college_location = validated_data.pop('college_location', None)
        
        if college_name is not None:
            try:
                college = College.objects.get(college_name=college_name)
            except College.DoesNotExist:
                # Create new college if it doesn't exist
                college_serializer = CollegeSerializer(data={
                    'college_name': college_name,
                    'college_location': college_location
                })
                if college_serializer.is_valid():
                    college = college_serializer.save()
                else:
                    raise serializers.ValidationError({
                        'college_error': college_serializer.errors
                    })
            instance.college = college

        # Handle password updates
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['user', 'course', 'enrollment_date']
        