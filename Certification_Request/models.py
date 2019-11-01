from django.db import models
from django.contrib.auth.models import User
import os
from courses.models import Course

def upload_to(instance, filename):
    extension = filename.split('.')[-1]
    new_name = "{}CERTIFICATE.{}".format(instance.user.get_full_name(), extension)
    unique_id = instance.user.username
    return os.path.join('certifications', unique_id, new_name)

class Certificate(models.Model):
    certificate = models.FileField(verbose_name="Certificate:", blank=True, null=True, upload_to=upload_to)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User:", blank=False, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, null=True,
                               verbose_name="Course:")
    upload_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_downloadable = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        verbose_name_plural = "Uploaded Certifications & Requests"

    def __str__(self):
        return "There is a certificate request from {} for {}.".format(self.user.get_full_name(), self.course.name)