from django.contrib import admin
from .models import CourseGiven
from .models import CourseTaken
# Register your models here.
admin.site.register(CourseGiven)
admin.site.register(CourseTaken)