from django.contrib import admin
from .models import Enrollment,User

# Register your models here.
admin.site.register(User)
admin.site.register(Enrollment)