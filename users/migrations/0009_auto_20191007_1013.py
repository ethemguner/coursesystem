# Generated by Django 2.2.5 on 2019-10-07 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20191007_0959'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='national_id',
            new_name='nationalid',
        ),
    ]
