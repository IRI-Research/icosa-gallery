# Generated by Django 5.0.6 on 2025-03-06 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0111_alter_bulksavelog_finish_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WaitlistEntry',
        ),
    ]
