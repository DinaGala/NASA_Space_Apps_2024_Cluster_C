# Generated by Django 5.1.1 on 2024-10-03 11:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_back', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='App_back',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='telefono',
        ),
        migrations.AddField(
            model_name='usuario',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
