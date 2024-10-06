from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
from django.utils import timezone # type: ignore
from datetime import datetime, date
from college.models import College

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