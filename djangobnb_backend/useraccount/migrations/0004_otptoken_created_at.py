# Generated by Django 5.0.2 on 2024-07-19 18:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0003_otptoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='otptoken',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
