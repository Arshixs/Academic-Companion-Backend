from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
from django.utils import timezone # type: ignore
from datetime import datetime, date
from college.models import College,Course
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
# Custom User Model inheriting from AbstractUser to extend default Django User
class User(AbstractUser):
    # Additional fields for the user
    branch = models.CharField(max_length=100, null=True, blank=True)
    current_semester = models.PositiveIntegerField(null=True, blank=True)
    college = models.ForeignKey(College, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # Ensure unique enrollment for each user in a course

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.course_name}"
    
    
