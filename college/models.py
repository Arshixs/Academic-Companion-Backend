from django.db import models

# Create your models here.
# Model representing a college
class College(models.Model):
    college_name = models.CharField(max_length=255, unique=True)
    college_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.college_name
