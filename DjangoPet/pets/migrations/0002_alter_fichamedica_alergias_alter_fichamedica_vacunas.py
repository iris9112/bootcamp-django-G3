# Generated by Django 4.2.20 on 2025-04-04 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pets", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fichamedica",
            name="alergias",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="fichamedica",
            name="vacunas",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
