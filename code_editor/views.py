from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import subprocess
import tempfile
import os
from rest_framework.permissions import IsAuthenticated

from .serializers import CodeExecutionSerializer, CodeSnippetSerializer
from .models import CodeSnippet


class RunCodeView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def get(self, request):
        """Retrieve all code snippets for the authenticated user."""
        snippets = CodeSnippet.objects.filter(user=request.user)
        serializer = CodeSnippetSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Execute a code snippet and optionally save it."""
        language = request.data.get('language')
        code = request.data.get('code')
        save_code = request.data.get('save', False)  # Check if the user wants to save the code

        if not all([language, code]):
            return Response({
                'error': 'Language and code are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(code.encode())
            tmp_file_path = tmp_file.name

        try:
            # Configure command based on language
            commands = {
                'python': ['python', tmp_file_path],
                'javascript': ['node', tmp_file_path],
                'cpp': [
                    f'g++ {tmp_file_path} -o {tmp_file_path}.out',
                    f'{tmp_file_path}.out'
                ],
                'c': [
                    f'gcc {tmp_file_path} -o {tmp_file_path}.out',
                    f'{tmp_file_path}.out'
                ]
            }

            command = commands.get(language)
            if not command:
                return Response({
                    'error': 'Unsupported language'
                }, status=status.HTTP_400_BAD_REQUEST)

            # For C/C++, we need to compile first
            if language in ['cpp', 'c']:
                subprocess.run(command[0], shell=True, check=True)
                process = subprocess.run(command[1], shell=True, capture_output=True, text=True)
            else:
                process = subprocess.run(command, capture_output=True, text=True)

            # Save the code snippet if requested
            if save_code:
                CodeSnippet.objects.create(
                    user=request.user,
                    language=language,
                    code=code
                )

            return Response({
                'output': process.stdout,
                'error': process.stderr
            })

        except subprocess.CalledProcessError as e:
            return Response({
                'error': str(e.stderr)
            }, status=status.HTTP_400_BAD_REQUEST)

        finally:
            # Clean up temporary files
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
            if language in ['cpp', 'c'] and os.path.exists(f'{tmp_file_path}.out'):
                os.unlink(f'{tmp_file_path}.out')

    def put(self, request, pk=None):
        """Update a specific code snippet."""
        try:
            snippet = CodeSnippet.objects.get(pk=pk, user=request.user)
        except CodeSnippet.DoesNotExist:
            return Response({'error': 'Snippet not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CodeSnippetSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Delete a specific code snippet."""
        try:
            snippet = CodeSnippet.objects.get(pk=pk, user=request.user)
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CodeSnippet.DoesNotExist:
            return Response({'error': 'Snippet not found'}, status=status.HTTP_404_NOT_FOUND)
