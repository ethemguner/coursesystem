# Generated by Django 2.2.5 on 2019-10-11 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20191011_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursediscount',
            name='bank_info',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Banka hesap bilgileri:'),
        ),
    ]
