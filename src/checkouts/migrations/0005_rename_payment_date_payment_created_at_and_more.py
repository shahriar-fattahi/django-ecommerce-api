# Generated by Django 4.2.7 on 2023-11-25 13:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("checkouts", "0004_alter_payment_checkout"),
    ]

    operations = [
        migrations.RenameField(
            model_name="payment",
            old_name="payment_date",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="payment",
            old_name="payment_method",
            new_name="method",
        ),
        migrations.RenameField(
            model_name="payment",
            old_name="payment_status",
            new_name="status",
        ),
    ]