# Generated by Django 4.0.4 on 2022-12-16 15:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calculate", "0002_remove_material_steel_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="material",
            name="hardness",
            field=models.FloatField(help_text="HB"),
        ),
        migrations.AlterField(
            model_name="material",
            name="yield_strenght",
            field=models.FloatField(help_text="МПа"),
        ),
    ]
