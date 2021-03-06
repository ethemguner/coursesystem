# Generated by Django 2.2.5 on 2019-10-09 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course_requests', '0004_auto_20191007_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseGiven',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_title', models.CharField(max_length=250, null=True)),
                ('request_content', models.TextField(max_length=1000, null=True)),
                ('limit_min', models.IntegerField(null=True)),
                ('limit_max', models.IntegerField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kursun vermek isteyen:')),
            ],
            options={
                'verbose_name_plural': 'Kurs Verme Talepleri',
            },
        ),
        migrations.CreateModel(
            name='CourseTaken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_title', models.CharField(max_length=250, null=True)),
                ('request_content', models.TextField(max_length=1000, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kurs talebinde bulunan:')),
            ],
            options={
                'verbose_name_plural': 'Kurs Alma Talepleri',
            },
        ),
        migrations.DeleteModel(
            name='CourseRequest',
        ),
    ]
