# Generated by Django 4.2.7 on 2023-11-24 15:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("checkouts", "0002_remove_checkout_total_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="payment_status",
            field=models.CharField(
                choices=[("f", "failed"), ("s", "success")], default="f", max_length=1
            ),
        ),
    ]