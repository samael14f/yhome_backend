# Generated by Django 5.0.2 on 2024-07-15 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_propertyverification_is_canceled_complaints_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
    ]
