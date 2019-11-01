from django.db import models
from prereg.models import PreRegistration
from Payments.models import Payment
from django.contrib.auth.models import User
from courses.models import Course

class FinalRegistration(models.Model):
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, null=True, blank=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=False, on_delete=models.CASCADE)
    registering_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = "Certain Registrations"

    def __str__(self):
        notice = "{}'s final registration has been applied for {}".format(self.user.get_full_name(),self.course.name)
        return notice