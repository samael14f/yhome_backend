# Generated by Django 5.0.2 on 2024-07-07 05:47

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffMembers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=255)),
                ('country_code', models.CharField(max_length=10)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
