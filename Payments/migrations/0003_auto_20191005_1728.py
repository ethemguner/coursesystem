# Generated by Django 2.2.5 on 2019-10-05 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0002_payment_payment_receipt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payment_receipt',
            new_name='image',
        ),
    ]
