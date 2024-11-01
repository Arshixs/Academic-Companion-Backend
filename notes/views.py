from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer

class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user, is_archived=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_pin(self, request, pk=None):
        note = self.get_object()
        note.is_pinned = not note.is_pinned
        note.save()
        return Response({'status': 'note updated'})

    @action(detail=True, methods=['post'])
    def toggle_archive(self, request, pk=None):
        note = self.get_object()
        note.is_archived = not note.is_archived
        note.save()
        return Response({'status': 'note updated'})