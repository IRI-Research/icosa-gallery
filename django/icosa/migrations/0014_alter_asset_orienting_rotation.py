# Generated by Django 5.0.6 on 2024-06-25 14:49

import icosa.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0013_alter_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='orienting_rotation',
            field=models.JSONField(default=icosa.models.default_orienting_rotation),
        ),
    ]
