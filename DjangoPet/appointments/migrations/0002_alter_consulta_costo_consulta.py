# Generated by Django 4.2.20 on 2025-04-04 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consulta",
            name="costo_consulta",
            field=models.DecimalField(decimal_places=2, default=20, max_digits=10),
        ),
    ]
