from django.db import models
from django.contrib.auth.models import User
import os
import sys
from PIL import Image
from uuid import uuid4
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from courses.models import Course

def upload_to(instance, filename):
    extension = filename.split('.')[-1]
    new_name = "{}.{}".format(str(uuid4()), extension)
    unique_id = instance.user.username
    return os.path.join('documents', unique_id, new_name)

class Profile(models.Model):
    TITLE = (
        (None, 'Choose'),
        ('1', 'Institution or a Group 1'),
        ('2', 'Institution or a Group 2'),
        ('3', 'External')
    )

    user = models.OneToOneField(User, null=True, blank=False, verbose_name="User", on_delete=models.CASCADE)
    nationalid = models.CharField(max_length=11, null=True, blank=False, verbose_name="ID Number")
    phone = models.CharField(max_length=10, null=True, blank=False, verbose_name="Phone number")
    other_phone = models.CharField(max_length=10, null=True, blank=False, verbose_name="Other phone number")
    title =models.CharField(max_length=50,null=True, blank=False, verbose_name="Institution or group",choices=TITLE)
    image = models.ImageField(upload_to=upload_to, verbose_name='Document:', blank=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    course = models.ManyToManyField(Course, blank=True)

    class Meta:
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.get_full_name()

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return None

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

        super(Profile, self).save(*args, **kwargs)