# model
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.text import slugify

from main.models import COLOR_CHOICES
from web.base import BaseModel


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )
    image = ThumbnailerImageField(
        "category",
        upload_to="categories/",
        help_text="Recommended size: 120x120 pixels.",
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(blank=True, null=True)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        help_text="Enter discount percentage for all products in this category."
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Category Active?")
    is_list_home = models.BooleanField(default=False,verbose_name="Show on Home Page")
    is_cake = models.BooleanField(default=False,verbose_name="Mark as Cake Category")

    class MPTTMeta:
        order_insertion_by = ["order"]

    class Meta:
        ordering = ["order"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_products(self):
        return Product.objects.filter(category=self)

    def get_product_count(self):
        return Product.objects.filter(category=self).count()

    def get_list_url(self):
        return reverse_lazy("main:categories")
    
    def get_all_products(self):
        descendant_categories = self.get_descendants(include_self=True)
        return Product.objects.filter(category__in=descendant_categories)
    
    def get_absolute_url(self):
        return reverse_lazy("web:shop_by_category", kwargs={'category_slug': self.slug})
    


    def __str__(self):
        return f"{self.name}"
    

class SubCategory(BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, limit_choices_to={"is_active": True}
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = ThumbnailerImageField(
        "subcategory",
        upload_to="subcategories/",
        blank=True,
        null=True,
        help_text="if Image Availible add",
    )
    description = models.TextField(blank=True, null=True)

    def get_list_url(self):
        return reverse_lazy("main:subcategories")

    def get_products(self):
        return Product.objects.filter(sub_category=self)

    def get_sub_products(self):
        return ProductVariant.objects.filter(product__sub_category=self, is_active=True)

    def get_product_count(self):
        return Product.objects.filter(sub_category=self).count()

    def __str__(self):
        return f"{self.category}-{self.name}"

    class Meta:
        verbose_name = _("Sub Category")
        verbose_name_plural = _("Sub Categories")
        ordering = ("category", "name")


class Tag(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    background_color = models.CharField(
        max_length=10, choices=COLOR_CHOICES, default="success"
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ("name",)

    def get_list_url(self):
        return reverse_lazy("main:tags")

    def __str__(self):
        return f"{self.name}"


class Brand(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    image = ThumbnailerImageField(upload_to="brands/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def get_list_url(self):
        return reverse_lazy("main:brands")

    def __str__(self):
        return self.name

    def get_products(self):
        return ProductVariant.objects.filter(product__brand=self, is_active=True)

class City(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        ordering = ("name",)

    def __str__(self):
        return self.name

class Pincode(BaseModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="pincodes")
    code = models.CharField(max_length=6, )

    def __str__(self):
        return f"{self.code} - {self.city.name}"



class Product(BaseModel):
    category = TreeForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        blank=True,
        null=True,
    )
    product_name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    cities = models.ManyToManyField(City, related_name="products", blank=True, )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products"    
        ordering = ("product_name",)

    def get_list_url(self):
        return reverse_lazy("main:product_list")

    def get_update_url(self):
        
        return reverse_lazy("main:product_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:product_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return f" {self.product_name}"


def generate_product_code():
    unique_id = uuid.uuid4()
    hex_str = str(unique_id).replace("-", "")[:8]
    alphanumeric_str = "".join(char for char in hex_str if char.isalnum())
    return alphanumeric_str.upper()


class ProductVariant(BaseModel):
    
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="varients"
    )
    varient_name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_code = models.CharField(max_length=100, default=generate_product_code)
    details = models.TextField()
    thumbnail_image = ThumbnailerImageField(
        upload_to="products/varients/",
        help_text=" The recommended size is 220x220 pixels.",
    )
    generic_name = models.CharField(max_length=200, blank=True, null=True)
    first_available_date = models.DateField(blank=True, null=True)
    is_popular = models.BooleanField(default=False)
    is_trend = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=True)
    is_best_seller = models.BooleanField(default=True)
    is_offer = models.BooleanField(default=False)
    is_stock = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=1)
    # meta
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.product} {self.varient_name}"

    def status(self):
        if self.stock >= 1:
            return "In Stock"
        else:
            return "Out of Stock"

    def get_reviews(self):
        return Review.objects.filter(product=self, approval=True)

    def num_of_reviews(self):
        return self.get_reviews().count()

    def average_rating(self):
        from django.db.models import Avg

        return self.get_reviews().aggregate(Avg("rating"))["rating__avg"]

    def five_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=5).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=5).count()
            else 0
        )

    def four_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=4).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=4).count()
            else 0
        )

    def three_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=3).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=3).count()
            else 0
        )

    def two_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=2).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=2).count()
            else 0
        )

    def one_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=1).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=1).count()
            else 0
        )

    def get_detail_url(self):
        return reverse_lazy("web:product_detail", kwargs={"slug": self.slug})

    def get_detete_url(self):
        return reverse_lazy("main:variant_delete", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("main:variant_update", kwargs={"pk": self.pk})

    def get_list_url(self):
        return reverse_lazy("main:variants")

    def get_product_images(self):
        return ProductImage.objects.filter(product_varient=self)

    def product_price(self):
        offer = OfferSaleProduct.objects.filter(
            product_varient=self,
            is_active=True,
            sale__is_active=True,
            sale__end_date__gte=timezone.now(),
        ).first()
        
        # Base price is selling price
        final_price = self.selling_price

        # Apply Offer Sale Price Deduction
        if offer:
            final_price -= offer.deduction

        # Apply Category Discount if Available
        if self.product.category and self.product.category.discount > 0:
            discount_percentage = self.product.category.discount
            final_price -= (final_price * discount_percentage / 100)

        return round(final_price, 2)

    def calculate_offer_percentage(self):
        """Update to calculate discount based on the new product_price."""
        if self.actual_price and self.actual_price > 0:
            discount_value = self.actual_price - self.product_price()
            offer_percentage = (discount_value / self.actual_price) * 100
            return round(offer_percentage, 2)
        return 0.0

    def offer_percent(self):
        """Ensure it considers both category and special discounts."""
        if self.actual_price and self.actual_price > self.selling_price:
            return round(
                ((self.actual_price - self.product_price()) / self.actual_price) * 100, 2
            )
        return 0

    def get_all_features_with_specs(self):
        features_with_specs = {}
        feature_specs = FeatureSpec.objects.filter(product_varient=self)
        for feature_spec in feature_specs:
            feature_name = feature_spec.feature.feature_name
            if feature_name not in features_with_specs:
                features_with_specs[feature_name] = []

            features_with_specs[feature_name].append(
                {
                    "specification_name": feature_spec.specification_name,
                    "specification_value": feature_spec.specification_value,
                }
            )
        return features_with_specs

    def get_related_products(self):
        return ProductVariant.objects.filter(
            product__sub_category__category=self.product.sub_category.category
        ).exclude(pk=self.pk)[:10]
    

class AvailableSize(models.Model):
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="available_sizes"
    )
    title = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.variant} - {self.title}"


class Feature(BaseModel):
    feature_name = models.CharField(max_length=128,null=True, blank=True)

    def get_list_url(self):
        return reverse_lazy("main:features")

    def __str__(self):
        return self.feature_name


class FeatureSpec(BaseModel):
    product_varient = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    specification_name = models.CharField(max_length=128,null=True, blank=True) 
    specification_value = models.CharField(max_length=128,null=True, blank=True)

    def __str__(self):
        return f"{self.specification_name} - {self.specification_value}"

from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class ProductImage(BaseModel):
    product_varient = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="products/", blank=True, null=True, help_text=" The recommended size is 800x600 pixels."
   )

    class Meta:
        ordering = ("product_varient",)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(ProductImage, self).delete(*args, **kwargs)
        storage.delete(path)

    def compress_image(self):
        """Compress image to target size while maintaining quality"""
        if not self.image:
            return
            
        # Open the image
        img = Image.open(self.image)
        
        # Initial quality
        quality = 90
        max_size = 100 * 1024  # 100KB
        
        # Try reducing quality gradually until reaching target size
        while quality >= 30:  # Don't go below quality 30
            output = BytesIO()
            
            # Convert to RGB if image is RGBA to avoid issues with JPEG
            if img.mode == 'RGBA':
                img = img.convert('RGB')
                
            # Save with current quality setting
            img.save(output, format='JPEG', quality=quality, optimize=True)
            
            # Check if size is below target
            if output.tell() <= max_size:
                # We've reached our target size, save and exit
                output.seek(0)
                self.image.save(
                    self.image.name.split('/')[-1],
                    ContentFile(output.read()),
                    save=False
                )
                break
                
            quality -= 5
            output.close()
        
        # If we couldn't get file below 100KB, try resizing dimensions
        if quality < 30:
            # Start with original image again
            img = Image.open(self.image)
            width, height = img.size
            
            # Try reducing dimensions while keeping aspect ratio
            while width > 300 and height > 300:  # Don't go below 300x300
                # Reduce dimensions by 10%
                width = int(width * 0.9)
                height = int(height * 0.9)
                
                resized_img = img.resize((width, height), Image.LANCZOS)
                output = BytesIO()
                
                if resized_img.mode == 'RGBA':
                    resized_img = resized_img.convert('RGB')
                    
                resized_img.save(output, format='JPEG', quality=85, optimize=True)
                
                if output.tell() <= max_size:
                    output.seek(0)
                    self.image.save(
                        self.image.name.split('/')[-1],
                        ContentFile(output.read()),
                        save=False
                    )
                    break
                
                output.close()


@receiver(pre_save, sender=ProductImage)
def image_compression(sender, instance, **kwargs):
    """Signal to compress image before saving"""
    if instance.image:
        instance.compress_image()



class Review(BaseModel):
    product = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveIntegerField(default=5)
    fullname = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.headline} - {self.fullname}"


class Purchase(BaseModel):
    date = models.DateField()
    voucher_number = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.voucher_number}"

    def get_detete_url(self):
        return reverse_lazy("main:purchase_delete", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("main:purchase_update", kwargs={"pk": self.pk})

    def get_list_url(self):
        return reverse_lazy("main:purchase_list")


class PurchaseProduct(BaseModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product_varient = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("purchase", "product_varient")

    def __str__(self):
        return f"{self.purchase} {self.product_varient}"


class OfferSale(BaseModel):
    title = models.CharField(max_length=128)
    image = ThumbnailerImageField(
        upload_to="sales/",
    )
    end_date = models.DateField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.end_date}"


class OfferSaleProduct(BaseModel):
    sale = models.ForeignKey(OfferSale, on_delete=models.CASCADE)
    product_varient = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    deduction = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.sale} {self.product_varient}"

    class Meta:
        unique_together = ("sale", "product_varient")

    def clean(self):
        # Ensure that a product is associated with only one active sale at a time
        existing_sale_product = (
            OfferSaleProduct.objects.filter(
                product_varient=self.product_varient,
                is_active=True,
                sale__is_active=True,
                sale__end_date__gte=timezone.now(),
            )
            .exclude(pk=self.pk)
            .first()
        )
        if existing_sale_product:
            raise ValidationError(
                {
                    "product_varient": "This product variant is already associated with an active sale."
                }
            )


class CategoryList(BaseModel):
    title = models.CharField(max_length=128)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, limit_choices_to={"is_active": True}
    )

    def __str__(self):
        return self.title

    def get_list_url(self):
        return reverse_lazy("main:categorylists")

    class Meta:
        verbose_name_plural = "Category Lists"
        ordering = ("id",)
