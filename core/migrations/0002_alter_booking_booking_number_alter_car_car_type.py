# Generated by Django 4.0.2 on 2023-08-01 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_number',
            field=models.CharField(default=86471982, max_length=8),
        ),
        migrations.AlterField(
            model_name='car',
            name='car_type',
            field=models.CharField(choices=[('sedan', 'Sedan'), ('suv', 'SUV'), ('minivan', 'MiniVan'), ('sport', 'Sport')], max_length=10),
        ),
    ]
