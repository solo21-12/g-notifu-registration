# Generated by Django 5.0.6 on 2024-05-15 18:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0002_alter_vehicel_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicel',
            name='plate_number',
            field=models.CharField(default=django.utils.timezone.now, max_length=32, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehicel',
            name='id',
            field=models.CharField(default='d8d10d86611a4f7c', max_length=16, primary_key=True, serialize=False),
        ),
    ]
