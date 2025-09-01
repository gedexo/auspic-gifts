from django import forms
from django.forms import inlineformset_factory
from django.utils.safestring import mark_safe
from main.models import District, State
from order.models import GiftCard
from products.models import (
    Brand,
    Category,
    CategoryList,
    Feature,
    FeatureSpec,
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
)
from web.models import Banner


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "image", "slug", "order", "parent", "is_active", "is_list_home", "is_cake", "discount")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category Name"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category Slug"}),
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "order": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Order"}),
            "discount": forms.NumberInput(attrs={"class": "form-control","placeholder": "Enter category-wide discount (%)"}),
            "parent": forms.Select(attrs={"class": "form-select","data-placeholder": "Select Parent Category"}),
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ("name", "category", "slug", "description")
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Sub Category Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "Sub Category Slug", "class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Description", "class": "form-control", "rows": 3}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ("name", "image", "description")
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Brand Name", "class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Description", "class": "form-control", "rows": 3}
            ),
            "image": forms.FileInput(attrs={"class": "file-input"}),
        }


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ("feature_name",)
        widgets = {
            "feature_name": forms.TextInput(
                attrs={"placeholder": "Feature Name", "class": "form-control"}
            ),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("product_name", "brand", "category","cities")
        widgets = {
            "product_name": forms.TextInput(
                attrs={"placeholder": "Product Name", "class": "form-control"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "brand": forms.Select(attrs={"class": "form-select"}),
            "cities": forms.SelectMultiple(
                attrs={"class": "form-select custom-multiple-select", "multiple": "multiple"}
            ),
        }


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        exclude = ("product_code",)
        widgets = {
            "product": forms.Select(attrs={"class": "form-select"}),
            "varient_name": forms.TextInput(
                attrs={"placeholder": "Product Variant Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "Product Variant Slug", "class": "form-control"}
            ),
            "tag": forms.Select(attrs={"class": "form-select"}),
            "selling_price": forms.TextInput(
                attrs={
                    "placeholder": "Sale Price ",
                    "class": "required form-control",
                    "type": "number",
                    "required": True,
                }
            ),
            "actual_price": forms.TextInput(
                attrs={
                    "placeholder": "Regular Price (MRP) ",
                    "class": "required form-control",
                    "type": "number",
                }
            ),
            "product_code": forms.TextInput(
                attrs={"placeholder": "Product Code", "class": "form-control"}
            ),
            "details": forms.Textarea(
                attrs={"cols": "30", "rows": "4", "class": "required form-control"}
            ),
            "meta_title": forms.TextInput(
                attrs={"placeholder": "Title", "class": "form-control"}
            ),
            "meta_description": forms.Textarea(
                attrs={"placeholder": "Description", "class": "form-control", "rows": 3}
            ),
            "thumbnail_image": forms.FileInput(attrs={"class": "file-input"}),
            "stock": forms.TextInput(
                attrs={
                    "placeholder": "Stock Quantity",
                    "class": "form-control",
                    "type": "number",
                }
            ),
            "generic_name": forms.TextInput(
                attrs={"placeholder": "Product Generic Name", "class": "form-control"}
            ),
            "first_available_date": forms.TextInput(
                attrs={
                    "placeholder": "First Available Date",
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ("image",)
        widgets = {
            "image": forms.FileInput(
                attrs={"class": "file-input", "type": "file"}
            ),
        }


class FeatureSpecForm(forms.ModelForm):
    class Meta:
        model = FeatureSpec
        fields = ("feature", "specification_value", "specification_name")
        widgets = {
            "feature": forms.Select(attrs={"class": "form-select"}),
            "specification_name": forms.TextInput(
                attrs={"placeholder": "Specification Title", "class": "form-control"}
            ),
            "specification_value": forms.TextInput(
                attrs={"placeholder": " Specification Value", "class": "form-control"}
            ),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = (
            "name",
            "background_color",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Tag Name", "class": "form-control"}
            ),
            "background_color": forms.Select(attrs={"class": "form-select"}),
        }


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = (
            "name",
            "slug",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "State Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "State Slug", "class": "form-control"}
            ),
        }


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = (
            "name",
            "slug",
            "state",
            "delivery_charge",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Enter District Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "District Slug", "class": "form-control"}
            ),
            "state": forms.Select(attrs={"class": "form-select"}),
            "delivery_charge": forms.TextInput(
                attrs={
                    "placeholder": "Delivery Charge ",
                    "class": "form-control",
                    "type": "number",
                }
            ),
        }


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = (
            "date",
            "voucher_number",
            "description",
        )
        widgets = {
            "date": forms.TextInput(
                attrs={
                    "placeholder": "Purchase date",
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "voucher_number": forms.TextInput(
                attrs={
                    "placeholder": "voucher number",
                    "class": "form-control",
                    "type": "number",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Purchase Description ",
                    "class": "form-control",
                    "rows": "4",
                }
            ),
        }


class PurchaseProductForm(forms.ModelForm):
    class Meta:
        model = PurchaseProduct
        fields = ("product_varient", "quantity")
        widgets = {
            "product_varient": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.TextInput(
                attrs={
                    "placeholder": "Quantity",
                    "class": "form-control",
                    "type": "number",
                }
            ),
        }


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, "1 - Poor"),
        (2, "2 - Below Average"),
        (3, "3 - Average"),
        (4, "4 - Good"),
        (5, "5 - Excellent"),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Review
        exclude = ("created_at",)
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "fullname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Full Name"}
            ),
            "headline": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "What’s most important to know",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "What did you like or dislike? What did you use this product for?",
                }
            ),
        }


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ("position", "banner_image", "category", "is_active")
        widgets = {
            "position": forms.Select(attrs={"class": "form-control"}),
            "banner_image": forms.FileInput(attrs={"class": "file-input"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "type": "checkbox",
                    "role": "switch",
                }
            ),
        }


class CategoryListForm(forms.ModelForm):
    class Meta:
        model = CategoryList
        fields = (
            "title",
            "category",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Category Name", "class": "form-control"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
        }



class GiftCardForm(forms.ModelForm):
    class Meta:
        model = GiftCard
        fields = (
            "code",
            "balance",
        )
        widgets = {
            "code": forms.TextInput(
                attrs={"placeholder": "Gift Card Name", "class": "form-control"}
            ),
            "balance": forms.NumberInput(
                attrs={"placeholder": "Amount", "class": "form-control"}
            ),
        }


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "City Name", "class": "form-control"})
        }


class PincodeForm(forms.ModelForm):
    class Meta:
        model = Pincode
        fields = ["city","code"]
        widgets = {
            "code": forms.TextInput(attrs={"placeholder": "Pincode", "class": "form-control"}),
            "city": forms.Select(attrs={"class": "form-select"})
        }

PincodeFormSet = inlineformset_factory(City, Pincode, form=PincodeForm, extra=1)