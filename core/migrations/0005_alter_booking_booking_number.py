# Generated by Django 4.0.2 on 2023-08-01 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_booking_booking_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_number',
            field=models.CharField(default=40512111, max_length=8),
        ),
    ]
