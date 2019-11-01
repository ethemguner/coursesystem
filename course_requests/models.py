from django.db import models
from django.contrib.auth.models import User

class CourseGiven(models.Model):
    request_title = models.CharField(max_length=250, null=True, blank=False)
    request_content = models.TextField(max_length=2000, null=True, blank=False)
    limit_min = models.IntegerField(null=True, blank=False)
    limit_max = models.IntegerField(null=True, blank=False)
    user = models.ForeignKey(User, null=True, blank=False, verbose_name="User who want to give course:",
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Course Giving Requests"

    def __str__(self):
        return "{} has sent a request about giving course.".format(self.user.get_full_name())

class CourseTaken(models.Model):
    request_title = models.CharField(max_length=250, null=True, blank=False)
    request_content = models.TextField(max_length=2000, null=True, blank=False)
    user = models.ForeignKey(User, null=True, blank=False, verbose_name="User who want to take course:",
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Course Taking Requests"

    def __str__(self):
        return "{} has sent a request about taking course.".format(self.user.get_full_name())