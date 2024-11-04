from rest_framework import serializers
from .models import College, Course

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'college_name', 'college_location', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

class CourseSerializer(serializers.ModelSerializer):
    college_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'course_id', 'course_name', 'college_name', 'created_at']
        read_only_fields = ['created_at', 'college_name']

    def get_college_name(self, obj):
        return obj.college.college_name if obj.college else None

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                user_college = College.objects.get(user=request.user)
                if Course.objects.filter(
                    course_id=data['course_id'],
                    college=user_college
                ).exists():
                    raise serializers.ValidationError({
                        "course_id": f"Course with ID '{data['course_id']}' already exists in your college."
                    })
            except College.DoesNotExist:
                raise serializers.ValidationError({
                    "college": "You must be associated with a college to create courses."
                })
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError({
                "authentication": "Authentication credentials were not provided."
            })

        try:
            college = College.objects.get(user=request.user)
            course = Course.objects.create(
                college=college,
                **validated_data
            )
            return course
        except College.DoesNotExist:
            raise serializers.ValidationError({
                "college": "You must be associated with a college to create courses."
            })