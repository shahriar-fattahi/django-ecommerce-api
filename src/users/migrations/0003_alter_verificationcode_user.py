# Generated by Django 4.2.7 on 2023-11-25 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_is_active_alter_user_profile_picture_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="verificationcode",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="code",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
