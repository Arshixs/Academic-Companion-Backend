# serializers.py
from rest_framework import serializers
from .models import CodeSnippet
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CodeSnippetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    execution_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = CodeSnippet
        fields = [
            'id',
            'title',
            'description',
            'code',
            'language',
            'user',
            'is_public',
            'created_at',
            'updated_at',
            'execution_count'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CodeExecutionSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    language = serializers.ChoiceField(
        choices=CodeSnippet.LANGUAGE_CHOICES,
        required=True
    )
    save_snippet = serializers.BooleanField(default=False)
    snippet_title = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255
    )
    snippet_description = serializers.CharField(
        required=False,
        allow_blank=True
    )
    is_public = serializers.BooleanField(default=False)
    
    def validate(self, data):
        if data.get('save_snippet'):
            if not data.get('snippet_title'):
                raise serializers.ValidationError({
                    'snippet_title': 'Title is required when saving snippet'
                })
        return data

class CodeSnippetListSerializer(serializers.ModelSerializer):
    """serializer for list views"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CodeSnippet
        fields = [
            'id',
            'title',
            'language',
            'user',
            'is_public',
            'created_at'
        ]