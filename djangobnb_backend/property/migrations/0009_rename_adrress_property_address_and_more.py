# Generated by Django 5.0.2 on 2024-07-18 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_property_adrress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='adrress',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='licence',
            new_name='license',
        ),
    ]
