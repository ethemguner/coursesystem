# Generated by Django 2.2.5 on 2019-10-15 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_auto_20191011_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[(None, 'Seçiniz'), ('1', 'Devam ediyor.'), ('2', 'Ön kayıtlar açık.'), ('3', 'Kesin kayıtlar açık.'), ('4', 'Bitti.')], max_length=45, null=True, verbose_name='Kurs Durumu:'),
        ),
    ]
