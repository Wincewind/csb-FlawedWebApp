# Generated by Django 4.2.6 on 2023-10-24 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("super_secret", models.CharField(max_length=2000)),
                (
                    "pw_recovery_q",
                    models.CharField(
                        default="What is my favourite color?", max_length=200
                    ),
                ),
                ("pw_recovery_a", models.CharField(max_length=200)),
                ("ssn", models.CharField(max_length=128)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
