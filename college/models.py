from django.db import models

# Create your models here.
# Model representing a college
class College(models.Model):
    college_name = models.CharField(max_length=255, unique=True)
    college_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.college_name
    

# Model representing a course
class Course(models.Model):
    course_id = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)
    college = models.ForeignKey(College, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course_id', 'college')  # Ensures course_id is unique within the same college

    def __str__(self):
        return self.course_name
