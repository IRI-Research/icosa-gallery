# Generated by Django 5.0.6 on 2025-02-11 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0100_asset_assets_likes_df6e36_idx'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='asset',
            index=models.Index(fields=['owner'], name='assets_owner_i_b9eeda_idx'),
        ),
    ]
