# Generated by Django 5.0.4 on 2024-04-19 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_rename_documetn_notification_document_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
