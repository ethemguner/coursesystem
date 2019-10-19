from django.db import models
from django.contrib.auth.models import User

class PreRegistration(models.Model):
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE, verbose_name="Kullanıcı:")

    class Meta:
        verbose_name_plural = "Ön Başvurular"

    def __str__(self):
        return "{} ön başvurusu.".format(self.user.get_full_name())