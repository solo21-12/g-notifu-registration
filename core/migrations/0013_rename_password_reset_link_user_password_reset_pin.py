# Generated by Django 5.0.3 on 2024-04-01 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_user_password_reset_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='password_reset_link',
            new_name='password_reset_pin',
        ),
    ]