# Generated by Django 4.2.3 on 2023-08-24 04:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_alter_booking_booking_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="booking_number",
            field=models.CharField(default=52853382, max_length=8),
        ),
    ]