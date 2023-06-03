# Generated by Django 4.0.4 on 2022-12-16 14:42

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Material",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=40)),
                ("steel_type", models.CharField(max_length=40)),
                ("type", models.CharField(max_length=40)),
                ("condition", models.CharField(blank=True, max_length=40)),
                ("hardness", models.FloatField()),
                ("yield_strenght", models.FloatField()),
            ],
        ),
    ]
