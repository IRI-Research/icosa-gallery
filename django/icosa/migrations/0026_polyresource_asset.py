# Generated by Django 5.0.6 on 2024-07-09 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0025_polyresource_is_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='polyresource',
            name='asset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='icosa.asset'),
        ),
    ]
