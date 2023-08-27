# Generated by Django 4.2.4 on 2023-08-27 05:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_alter_booking_booking_number_alter_payment_booking"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="status",
            field=models.CharField(
                choices=[("completed", "Completed"), ("refunded", "Refunded")],
                default="completed",
                max_length=55,
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="booking_number",
            field=models.CharField(default=68673289, max_length=8),
        ),
    ]