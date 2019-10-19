from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from PIL import Image
from uuid import uuid4
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import sys

def upload_to(instance, filename):
    extension = filename.split('.')[-1]
    new_name = "{}.{}".format(str(uuid4()), extension)
    unique_id = instance.user.username
    return os.path.join('odeme_dekontlari', unique_id, new_name)

class Payment(models.Model):
    account_owner = models.CharField(max_length=100, null=True, blank=False)
    payment_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    image = models.ImageField(upload_to=upload_to, verbose_name='Ödeme dekontu:', blank=False)
    user = models.ForeignKey(User, null=True, blank=False, verbose_name="Ödeme yapan kullanıcı:",
                             on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=False, verbose_name="Ödeme yapılan kurs:",
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Ödemeler"

    def __str__(self):
        return "{} tarafindan odeme mevcut.".format(self.user.get_full_name())

    def save(self, *args, **kwargs):
        #Image resize.
        if self.image:
            img = Image.open(self.image)
            output = BytesIO()
            img = img.resize((700,700))
            img.save(output, format='PNG', quality=100)
            output.seek(0)

            self.image = InMemoryUploadedFile(output, 'ImageField', '%s.png' %self.image.name.split('.')[0],
                                              'image/png', sys.getsizeof(output), None)

        super(Payment, self).save(*args, **kwargs)