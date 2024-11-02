from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CalendarEvent(models.Model):
    COLOR_CHOICES = [
        ('blue', 'Blue'),
        ('red', 'Red'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    color = models.CharField(max_length=6, choices=COLOR_CHOICES, default='blue')  # Max length set to longest choice
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.title} on {self.date} from {self.start_time} to {self.end_time}"
