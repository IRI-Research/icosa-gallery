# Generated by Django 5.0.6 on 2024-09-03 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0050_alter_polyresource_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='is_valid',
            new_name='is_viewer_compatible',
        ),
    ]
