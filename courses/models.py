from django.db import models
from prereg.models import PreRegistration

class Course(models.Model):

    STATUS = (
        (None, 'Seçiniz'),
        ('1', 'Devam ediyor.'),
        ('2', 'Ön kayıtlar açık.'),
        ('3', 'Kesin kayıtlar açık.'),
        ('4', 'Bitti.'),
    )

    CATEGORIES = (
        (None, 'Seçiniz'),
        ('1', 'Senkron'),
        ('2', 'Asenkron')
    )

    name = models.CharField(max_length=250, null=True, blank=False, verbose_name="Kurs:")
    start_at = models.DateTimeField(null=True, blank=False, verbose_name="Başlangıç tarihi:")
    finish_at = models.DateTimeField(null=True, blank=False, verbose_name="Bitiş tarihi:")
    content = models.TextField(max_length=6000, null=True, blank=True, verbose_name="İçerik:")
    status = models.CharField(max_length=45, null=True, blank=False, verbose_name="Kurs Durumu:", choices=STATUS)
    course_code = models.CharField(max_length=5, null=True, blank=True)
    price = models.IntegerField(null=True, blank=False, verbose_name="Fiyat:")
    prereg = models.ManyToManyField(PreRegistration, blank=True, verbose_name="Ön başvuru:")
    registering_extension = models.CharField(max_length=25, null=True, blank=True, editable=True)
    is_registerable = models.BooleanField(default=False, verbose_name="Kesin kaydı aç.")
    category = models.CharField(max_length=45, null=True, blank=False, verbose_name="Kurs Kategori:", choices=CATEGORIES)

    class Meta:
        verbose_name_plural = "Kurslar"

    def __str__(self):
        return self.name

class CourseDiscount(models.Model):
    discount_1 = models.IntegerField(null=True, blank=False,
                                     verbose_name="Ege Üniversitesi personel / öğrenci / mezun indirimi:")
    discount_2  = models.IntegerField(null=True, blank=False,
                                     verbose_name="Gazi / engell / şehit yakını indirimi:")
    bank_info = models.TextField(max_length=500, null=True, blank=True, verbose_name="Banka hesap bilgileri:")

    class  Meta:
        verbose_name_plural = "İndirim"

    def __str__(self):
        return "EgeUni Personel/ogrenci/mezun -> {} Gazi/engelli/sehit yakini 2 -> {}".format(self.discount_1,
                                                                                              self.discount_2)