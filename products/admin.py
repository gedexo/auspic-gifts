from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export import resources

from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin
from mptt.forms import TreeNodeChoiceField

from web.base import BaseAdmin

from .models import (
    Brand,
    Category,
    CategoryList,
    Feature,
    FeatureSpec,
    OfferSale,
    OfferSaleProduct,
    Product,
    ProductImage,
    ProductVariant,
    Purchase,
    PurchaseProduct,
    Review,
    SubCategory,
    Tag,
    City,
    Pincode,
    AvailableSize
)


class OfferSaleProductInline(admin.TabularInline):
    model = OfferSaleProduct
    extra = 1
    autocomplete_fields = ("product_varient",)


@admin.register(OfferSale)
class OfferSaleAdmin(BaseAdmin, ImportExportModelAdmin):
    list_display = ("title", "end_date", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("title",)
    inlines = (OfferSaleProductInline,)


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    fields = ('name', 'slug','order', 'is_active','is_list_home','is_cake')
    fk_name = 'parent'
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin, ImportExportModelAdmin):
    list_display = ('name','order', 'slug', 'parent', 'is_active','is_list_home','is_cake')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['is_active','is_list_home','is_cake',]
    inlines = [CategoryInline]
    autocomplete_fields = ("parent",)
    fieldsets = (
        ("Category Details", {'fields': ('name', 'slug', 'parent','order', 'is_active','is_list_home','is_cake','image', 'discount')}),
    )
    list_editable = ('order','is_active','is_cake','is_list_home',)


@admin.register(Tag)
class TagAdmin(BaseAdmin, ImportExportModelAdmin):
    list_display = ("name", "background_color")
    search_fields = ("name",)
    list_display_links = ("name", "background_color")


@admin.register(Feature)
class FeatureAdmin(BaseAdmin, ImportExportModelAdmin):
    list_display = ("feature_name",)
    search_fields = ("feature_name",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class PincodeInline(admin.TabularInline):
    model = Pincode
    extra = 1  # Number of empty forms displayed (optional)
    fields = ("code", "is_active")  # Show only relevant fields


@admin.register(City)
class CityAdmin(BaseAdmin, ImportExportModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "is_active")
    inlines = [PincodeInline]  # Attach the inline here

@admin.register(Pincode)
class PincodeAdmin(BaseAdmin, ImportExportModelAdmin):  # No need for BaseAdmin
    list_display = ("city", "code",)
    search_fields = ("code",)


@admin.register(Product)
class ProductAdmin(BaseAdmin, ImportExportModelAdmin):
    list_display = ("product_name",)
    exclude = ("creator",)
    list_filter = ("brand","cities","category")
    search_fields = ("product_name",)
    autocomplete_fields = ("cities",)


class FeatureSpecInline(admin.TabularInline):  # or admin.StackedInline
    model = FeatureSpec
    autocomplete_fields = ("feature",)
    extra = 1

class AvailableSizeInline(admin.TabularInline):
    model = AvailableSize
    extra = 1


@admin.register(ProductVariant)
class ProductVariantAdmin(BaseAdmin, ImportExportModelAdmin):  # Correct order
    list_display = ("product", "varient_name", "is_active")
    list_filter = ("product", "product__brand", "is_active")
    list_display_links = ("product", "varient_name")
    prepopulated_fields = {"slug": ("varient_name",)}
    search_fields = ("varient_name",)
    autocomplete_fields = ("product", "tag")
    list_editable = ("is_active",)
    inlines = [FeatureSpecInline, ProductImageInline, AvailableSizeInline]


@admin.register(Brand)
class BrandAdmin(BaseAdmin, ImportExportModelAdmin):
    list_display = ("name",)


@admin.register(Review)
class ReviewAdmin(BaseAdmin, ImportExportModelAdmin):
    list_display = ["product", "rating", "headline", "approval", "created_at"]
    list_filter = ["approval", "created_at"]
    search_fields = ["headline", "content", "user__username", "product__varient_name"]
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"


@admin.register(CategoryList)
class CategoryListAdmin(BaseAdmin, ImportExportModelAdmin):
    list_display = ("title",)
