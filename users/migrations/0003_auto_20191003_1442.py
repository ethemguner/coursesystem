# Generated by Django 2.2.5 on 2019-10-03 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('users', '0002_profile_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='course',
        ),
        migrations.AddField(
            model_name='profile',
            name='course',
            field=models.ManyToManyField(blank=True, null=True, to='courses.Course'),
        ),
    ]
