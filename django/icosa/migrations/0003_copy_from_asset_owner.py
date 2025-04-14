# Generated by Django 5.0.6 on 2025-03-15 00:43

from django.db import migrations

def copy_likes(apps, schema_editor):
    OwnerAssetLike = apps.get_model("icosa", "OwnerAssetLike")
    UserLike = apps.get_model("icosa", "UserLike")
    for asset_owner_like in OwnerAssetLike.objects.all():
        UserLike.objects.create(
            date_liked=asset_owner_like.date_liked,
            asset=asset_owner_like.asset,
            user=asset_owner_like.user.django_user,
        )
        
def copy_displayname(apps, schema_editor):
    AssetOwner = apps.get_model("icosa", "AssetOwner")
    for asset_owner in AssetOwner.objects.all():
        if asset_owner.django_user:
            asset_owner.django_user.displayname = asset_owner.displayname
            asset_owner.django_user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0002_alter_user_options_user_displayname_alter_user_table_and_more'),
    ]


    operations = [
        migrations.RunPython(copy_likes),
        migrations.RunPython(copy_displayname),
    ]

        