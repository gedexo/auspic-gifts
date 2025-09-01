from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    AdditionalInfo,
    City,
    DestinationPlace,
    Order,
    OrderItem,
    Tracking,
    Wishlist,
    GiftCard,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_id",
        # "user",
        "is_ordered",
        "payable",
        "order_status",
        "created",
    ]
    list_filter = ["order_status", "created", "updated"]
    search_fields = ["order_id", "user__username"]
    inlines = (OrderItemInline,)


@admin.register(GiftCard)
class GiftCardAdmin(ImportExportModelAdmin):
    list_display = ("code", "balance", "is_active",)
    list_filter = ("is_active",)
    search_fields = ("code",)

# @admin.register(Wishlist)
# class WishlistAdmin(ImportExportModelAdmin):
#     list_display = ("user",)
#     search_fields = ("user__username",)


# class TrackInline(admin.TabularInline):
#     model = AdditionalInfo
#     extra = 1
#     fields = (
#         "date",
#         "title",
#     )


# @admin.register(Tracking)
# class TrackingAdmin(admin.ModelAdmin):
#     list_display = ("tracking_id", "procedure", "link")
#     list_filter = ("procedure",)
#     search_fields = ("tracking_id",)
#     readonly_fields = ("link",)
#     autocomplete_fields = ("destination_city",)
#     inlines = [TrackInline]


# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
#     list_display = ("name", "order")
#     list_filter = ("order",)
#     search_fields = ("name",)


# @admin.register(DestinationPlace)
# class DestinationPlaceAdmin(admin.ModelAdmin):
#     list_display = ("name", "code")
