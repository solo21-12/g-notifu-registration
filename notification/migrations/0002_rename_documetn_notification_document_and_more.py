# Generated by Django 5.0.4 on 2024-04-19 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='documetn',
            new_name='document',
        ),
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.CharField(default='NT4G6FC9LAHJKE88', max_length=16, primary_key=True, serialize=False),
        ),
    ]