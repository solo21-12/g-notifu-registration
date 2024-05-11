# Generated by Django 5.0.6 on 2024-05-11 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files', '__first__'),
        ('vehicle', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('Third party insurance', 'Third party insurance'), ('Road fund', 'Road Fund'), ('Road Authority', 'Road Authority'), ('Bolo', 'Bolo')], max_length=100)),
                ('renewal_status', models.BooleanField(default=False)),
                ('renewal_date', models.DateField()),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('files', models.ManyToManyField(blank=True, to='files.files')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.vehicel')),
            ],
        ),
    ]
