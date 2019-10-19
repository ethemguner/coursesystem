# Generated by Django 2.2.5 on 2019-10-04 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prereg', '0002_remove_preregistration_course'),
        ('courses', '0004_auto_20191004_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='prereg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prereg.PreRegistration', verbose_name='Ön başvuru:'),
        ),
    ]
