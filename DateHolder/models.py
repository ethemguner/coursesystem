from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class DateHolder(models.Model):
    image_upload_date= models.DateTimeField(max_length=100, null=True, blank=False, editable=True,
                                        verbose_name="Document uploaded date:")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True,
                                verbose_name="Who uploaded:")

    class Meta:
        verbose_name_plural = "Document Upload Dates"

    def __str__(self):
        return "{} has uploaded a document on {}-{}-{}.".format(self.user.username, self.image_upload_date.day,
                                                                       self.image_upload_date.month,
                                                                       self.image_upload_date.year)