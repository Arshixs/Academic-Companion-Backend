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

    def create(self, validated_data):
        # Extract college data
        college_name = validated_data.pop('college_name')
        college_location = validated_data.pop('college_location')
        password = validated_data.pop('password', None)

        # Retrieve existing college or create new one if it doesn't exist
        college, created = College.objects.get_or_create(
            college_name=college_name,
            defaults={'college_location': college_location}
        )

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
            college, created = College.objects.get_or_create(
                college_name=college_name,
                defaults={'college_location': college_location}
            )
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
        
class ProfileUpdateSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(required=False)
    college_location = serializers.CharField(required=False)
    branch = serializers.CharField(required=False)
    current_semester = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['branch', 'current_semester', 'college_name', 'college_location']

    def validate(self, data):
        # Validate that college_location is provided if college_name is new
        if 'college_name' in data:
            college_exists = College.objects.filter(
                college_name=data['college_name']
            ).exists()
            if not college_exists and 'college_location' not in data:
                raise serializers.ValidationError({
                    "college_location": "College location is required when creating a new college"
                })
        return data

    def update(self, instance, validated_data):
        # Handle college update if provided
        college_name = validated_data.pop('college_name', None)
        college_location = validated_data.pop('college_location', None)

        if college_name:
            college, created = College.objects.get_or_create(
                college_name=college_name,
                defaults={'college_location': college_location or ''}
            )
            instance.college = college

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
