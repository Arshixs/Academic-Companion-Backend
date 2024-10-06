from rest_framework import serializers
from .models import College,Course

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['college_name', 'college_location']


class CourseSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(write_only=True)

    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'college_name', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        # Retrieve the college by name
        college_name = validated_data.pop('college_name')
        try:
            college = College.objects.get(college_name=college_name)
        except College.DoesNotExist:
            raise serializers.ValidationError(f"College with name '{college_name}' does not exist.")

        # Create the course with the retrieved college
        course = Course.objects.create(college=college, **validated_data)
        return course