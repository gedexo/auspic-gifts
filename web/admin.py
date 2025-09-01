from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .base import BaseAdmin
from .models import Banner, Contact

admin.site.unregister(Group)


@admin.register(Banner)
class BannerAdmin(BaseAdmin):
    list_display = ("position", "category", "image_preview", "is_active")
    list_filter = ("position",)

    def image_preview(self, obj):
        if obj.banner_image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.banner_image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"


@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    list_display = ("full_name", "email", "phone", "place")
    ordering = ("timestamp",)
    search_fields = (
        "first_name",
        "last_name",
    )
