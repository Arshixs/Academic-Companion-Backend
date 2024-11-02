from django.db import models
from user.models import User  # Direct import of User model
from user.models import Enrollment
from django.db.models.signals import post_save
from django.dispatch import receiver



class Label(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='labels')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'user']  # Ensure label names are unique per user

    def __str__(self):
        return f"{self.name} - {self.user.username}"


class Assignment(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in-progress', 'In Progress'),
        ('done', 'Done'),
        ('backlog', 'Backlog'),
        ('canceled', 'Canceled'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.title}"


# Signal to create label when user enrolls in a course
@receiver(post_save, sender=Enrollment)
def create_course_label(sender, instance, created, **kwargs):
    if created:
        # Create a new label for the course
        Label.objects.get_or_create(
            name=f"Course-{instance.course.course_id}",
            user=instance.user,
            defaults={
                'name': f"Course-{instance.course.course_id}"
            }
        )