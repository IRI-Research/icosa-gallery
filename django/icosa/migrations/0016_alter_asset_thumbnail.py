# Generated by Django 5.0.6 on 2024-06-26 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0015_auto_20240626_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
