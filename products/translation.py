from modeltranslation.translator import TranslationOptions, register

from .models import (
    Brand,
    Category,
    CategoryList,
    Feature,
    FeatureSpec,
    OfferSale,
    Product,
    ProductVariant,
    Purchase,
    SubCategory,
    Tag,
)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ("feature_name",)


@register(FeatureSpec)
class FeatureSpecTranslationOptions(TranslationOptions):
    fields = ("specification_name", "specification_value")


@register(Purchase)
class PurchaseTranslationOptions(TranslationOptions):
    fields = ("description",)


@register(OfferSale)
class OfferSaleTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(CategoryList)
class CategoryListTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("product_name",)


@register(ProductVariant)
class ProductVariantTranslationOptions(TranslationOptions):
    fields = (
        "varient_name",
        "details",
        "generic_name",
        "meta_title",
        "meta_description",
    )
