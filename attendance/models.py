from django.db import models
from user.models import Enrollment

# Model representing attendance records
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('no class', 'No Class'),
    ]

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('enrollment', 'attendance_date')

    def __str__(self):
        return f'{self.enrollment} - {self.attendance_date} - {self.status}'