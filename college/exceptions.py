from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler to get the standard error response
    response = exception_handler(exc, context)

    # Log the exception for debugging purposes
    logger.error(f"Exception: {exc}, Context: {context}")

    # Check for IntegrityError (unique constraint violation, etc.)
    if isinstance(exc, IntegrityError):
        return Response({
            'error': 'A unique constraint violation occurred. Please check your data and try again.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Handle the 400 BAD REQUEST errors (e.g., validation errors)
    if response is not None:
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            return Response({
                'error': response.data
            }, status=status.HTTP_400_BAD_REQUEST)

        # Handle 500 INTERNAL SERVER ERROR (unexpected server error)
        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                'error': 'A server error occurred. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Fallback for any other unexpected error
    return Response({
        'error': 'Something went wrong. Please try again later.'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
