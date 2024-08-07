# Generated by Django 5.0.2 on 2024-07-26 18:51

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0010_reservation_paid_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payment_id', models.CharField(max_length=255)),
                ('order_id', models.CharField(max_length=255)),
                ('signature', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reservation_id', models.ForeignKey(default='Deleted Reservation', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='reservations_id', to='property.reservation')),
                ('user', models.ForeignKey(default='Deleted User', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='order_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
