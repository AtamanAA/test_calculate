# Generated by Django 4.0.4 on 2022-12-16 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='steel_type',
        ),
    ]
