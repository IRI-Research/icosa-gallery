# Generated by Django 5.0.6 on 2024-12-11 16:08

import django.db.models.deletion
import icosa.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0085_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='MastheadSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=1024, null=True, upload_to=icosa.models.thumbnail_upload_path)),
                ('url', models.CharField(blank=True, help_text="URL to link to in place of an asset's viewer page.", max_length=1024, null=True)),
                ('headline_text', models.CharField(blank=True, help_text="Text displayed in place of an asset's name.", max_length=1024, null=True)),
                ('sub_text', models.CharField(blank=True, help_text="Text displayed in place of an asset's owner's name.", max_length=1024, null=True)),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='icosa.asset')),
            ],
        ),
    ]
