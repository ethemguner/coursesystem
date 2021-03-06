# Generated by Django 2.2.5 on 2019-10-16 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0018_auto_20191015_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.FileField(blank=True, null=True, upload_to='.', verbose_name='Sertifika:')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('is_downloadable', models.BooleanField(blank=True, default=False, null=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='Kurs:')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı:')),
            ],
            options={
                'verbose_name_plural': 'Yüklenen Sertifikalar',
            },
        ),
    ]
