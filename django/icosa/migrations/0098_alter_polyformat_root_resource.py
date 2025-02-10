# Generated by Django 5.0.6 on 2025-02-10 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0097_alter_polyformat_root_resource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polyformat',
            name='root_resource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='root_formats', to='icosa.resource'),
        ),
    ]
