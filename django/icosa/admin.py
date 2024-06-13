from icosa.models import (
    Asset,
    DeviceCode,
    Oauth2Client,
    Oauth2Code,
    Oauth2Token,
    User,
)

from django.contrib import admin


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url",
        "owner",
        "description",
        "_formats",
        "visibility",
        "curated",
        "polyid",
        "polydata",
        "thumbnail",
    )
    search_fields = (
        "name",
        "url",
    )
    list_filter = (
        "visibility",
        "curated",
    )

    @admin.display(description="Formats")
    def _formats(self, obj):
        return (
            f"{', '.join([x['format'] for x in obj.formats if 'format' in x])}"
        )

    search_fields = (
        "name",
        "url",
        "owner__displayname",
    )


@admin.register(DeviceCode)
class DeviceCodeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "devicecode",
        "expiry",
    )

    date_hierarchy = "expiry"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "displayname",
        "email",
        "url",
    )

    search_fields = (
        "displayname",
        "email",
        "url",
        "id",
    )
    filter_horizontal = ("likes",)


@admin.register(Oauth2Client)
class Oauth2ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Oauth2Code)
class Oauth2CodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Oauth2Token)
class Oauth2TokenAdmin(admin.ModelAdmin):
    pass
