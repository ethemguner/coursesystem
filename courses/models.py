from django.db import models
from prereg.models import PreRegistration

class Course(models.Model):

    STATUS = (
        (None, 'Choose'),
        ('1', 'Continuing.'),
        ('2', 'Pre-registration is open.'),
        ('3', 'Certain registration is open.'),
        ('4', 'Finished.'),
    )

    CATEGORIES = (
        (None, 'Choose'),
        ('1', 'Senkron'),
        ('2', 'Asenkron')
    )

    name = models.CharField(max_length=250, null=True, blank=False, verbose_name="Course:")
    start_at = models.DateTimeField(null=True, blank=False, verbose_name="Start at:")
    finish_at = models.DateTimeField(null=True, blank=False, verbose_name="Finish at:")
    content = models.TextField(max_length=6000, null=True, blank=True, verbose_name="Content:")
    status = models.CharField(max_length=45, null=True, blank=False, verbose_name="Status:", choices=STATUS)
    course_code = models.CharField(max_length=5, null=True, blank=True)
    price = models.IntegerField(null=True, blank=False, verbose_name="Price:")
    prereg = models.ManyToManyField(PreRegistration, blank=True, verbose_name="Pre-registration:")
    registering_extension = models.CharField(max_length=25, null=True, blank=True, editable=True)
    is_registerable = models.BooleanField(default=False, verbose_name="Open certain registrations.")
    category = models.CharField(max_length=45, null=True, blank=False, verbose_name="Course category:", choices=CATEGORIES)

    class Meta:
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name

class CourseDiscount(models.Model):
    discount_1 = models.IntegerField(null=True, blank=False,
                                     verbose_name="Special discount for a group/person etc. 1")
    discount_2  = models.IntegerField(null=True, blank=False,
                                     verbose_name="Special discount for a group/person etc. 2")
    bank_info = models.TextField(max_length=500, null=True, blank=True, verbose_name="Bank account information:")

    class  Meta:
        verbose_name_plural = "Discount"

    def __str__(self):
        return "Discount 1 -> {} Discount 2 -> {}".format(self.discount_1, self.discount_2)