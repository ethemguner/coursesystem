# Generated by Django 2.2.5 on 2019-10-11 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0003_auto_20191005_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='price',
        ),
    ]
