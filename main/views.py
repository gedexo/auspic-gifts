from datetime import datetime, timedelta

from django import forms

# models
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.forms.formsets import formset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from django.views import View

# view
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

# forms
from main.forms import (
    BannerForm,
    BrandForm,
    CategoryForm,
    CategoryListForm,
    DistrictForm,
    FeatureForm,
    FeatureSpecForm,
    ProductForm,
    ProductImageForm,
    ProductVariantForm,
    PurchaseForm,
    PurchaseProductForm,
    ReviewForm,
    StateForm,
    SubCategoryForm,
    TagForm,
    GiftCardForm,
    PincodeForm,
    CityForm,
    PincodeFormSet
)
from main.mixins import SuperAdminLoginRequiredMixin
from main.models import District, State
from order.models import Order,GiftCard,OrderItem
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
    Pincode
    
)
from web.models import Banner
from django.contrib.auth import get_user_model
User=get_user_model()

class IndexView(SuperAdminLoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"
    extra_context = {"is_dashbord": True}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        two_weeks_ago = datetime.now() - timedelta(weeks=2)
        context["last_two_week_orders_count"] = Order.objects.filter(
            created__gte=two_weeks_ago
        ).count()
        context["last_two_week_reviews_count"] = Review.objects.filter(
            created_at__gte=two_weeks_ago
        ).count()
        context["last_two_week_customers_count"] = User.objects.filter(
            date_joined__gte=two_weeks_ago
        ).count()
        context["orders"] = Order.objects.order_by("-id")[:100]
        context["customers"] = User.objects.order_by("-id")[:100]
        context["reviews"] = Review.objects.order_by("-id")[:100]
        return context


# order
class OrderView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/order/list.html"
    model = Order
    extra_context = {"is_order": True}


class OrderDetailView(SuperAdminLoginRequiredMixin, DetailView):
    model = Order
    template_name = "dashboard/order/single.html"
    context_object_name = "order"
    slug_field = "order_id"
    slug_url_kwarg = "order_id"
    extra_context = {"is_order": True}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_items"] = OrderItem.objects.filter(order=self.object)
        return context


class OrderUpdateView(SuperAdminLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Retrieve parameters from the GET request
        status = request.GET.get("status")
        pk = request.GET.get("pk")

        # Update the order status
        order = get_object_or_404(Order, pk=pk)
        order.status = status
        order.save()

        # Prepare the response data
        message = "Order status updated successfully"
        response_data = {
            "status": "true",
            "title": "Successfully Updated",
            "message": str(message),
            "reload": "true",
        }

        return JsonResponse(response_data)


# State
class StateListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/state/list.html"
    model = State
    extra_context = {"is_state": True}


class StateCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = State
    template_name = "dashboard/state/entry.html"
    form_class = StateForm
    success_url = reverse_lazy("main:states")
    extra_context = {"is_state": True, "title": "Add New State"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "State Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class StateUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = State
    template_name = "dashboard/state/entry.html"
    form_class = StateForm
    success_url = reverse_lazy("main:states")
    extra_context = {"is_state": True, "title": "State Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "State Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class StateDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = State
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:states")
    extra_context = {"is_state": True}


# District
class DistrictListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/district/list.html"
    model = District
    extra_context = {"is_district": True}


class DistrictCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = District
    template_name = "dashboard/district/entry.html"
    form_class = DistrictForm
    success_url = reverse_lazy("main:districts")
    extra_context = {"is_district": True, "title": "Add New District"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "District Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class DistrictUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = District
    template_name = "dashboard/district/entry.html"
    form_class = DistrictForm
    success_url = reverse_lazy("main:districts")
    extra_context = {"is_district": True, "title": "District Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "District Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class DistrictDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = District
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:districts")


# tag
class TagListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/tag/list.html"
    model = Tag
    extra_context = {"is_tag": True}

    def get_queryset(self):
        return Tag.objects.filter(is_active=True)


class TagCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Tag
    template_name = "dashboard/tag/entry.html"
    form_class = TagForm
    success_url = reverse_lazy("main:tags")
    extra_context = {"is_tag": True, "title": "Add New Tag"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Tag Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class TagUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Tag
    template_name = "dashboard/tag/entry.html"
    form_class = TagForm
    success_url = reverse_lazy("main:tags")
    extra_context = {"is_tag": True, "title": "Edit Tag"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Tag Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class TagDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Tag
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:tags")


# brand
class BrandListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/brand/list.html"
    model = Brand
    extra_context = {"is_brand": True}

    def get_queryset(self):
        return Brand.objects.filter(is_active=True)


class BrandCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Brand
    template_name = "dashboard/brand/entry.html"
    form_class = BrandForm
    success_url = reverse_lazy("main:brands")
    extra_context = {"is_brand": True, "title": "Add New Brand"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Brand Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class BrandUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Brand
    template_name = "dashboard/brand/entry.html"
    form_class = BrandForm
    success_url = reverse_lazy("main:brands")
    extra_context = {"is_brand": True, "title": "Edit Brand"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "brand Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class BrandDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Brand
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:brands")


# feature
class FeatureListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/feature/list.html"
    model = Feature
    extra_context = {"is_feature": True}

    def get_queryset(self):
        return Feature.objects.filter(is_active=True)


class FeatureCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Feature
    template_name = "dashboard/feature/entry.html"
    form_class = FeatureForm
    success_url = reverse_lazy("main:features")
    extra_context = {"is_feature": True, "title": "Add New Product Feature"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Product Feature Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class FeatureUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Feature
    template_name = "dashboard/feature/entry.html"
    form_class = FeatureForm
    success_url = reverse_lazy("main:features")
    extra_context = {"is_feature": True, "title": "Edit Product Feature"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Feature Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class FeatureDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Feature
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:features")


# category
class CategoryListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/category/list.html"
    model = Category
    extra_context = {"is_category": True, "is_category_list": True}

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


class CategoryCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Category
    template_name = "dashboard/category/entry.html"
    form_class = CategoryForm
    success_url = reverse_lazy("main:categories")
    extra_context = {
        "is_category": True,
        "is_category_list": True,
        "title": "Add New Category",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Category Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class CategoryUpdate(SuperAdminLoginRequiredMixin, UpdateView):
    model = Category
    template_name = "dashboard/category/entry.html"
    form_class = CategoryForm
    success_url = reverse_lazy("main:categories")
    extra_context = {
        "is_category": True,
        "is_category_list": True,
        "is_edit": True,
        "title": "Edit Category",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Category Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class CategoryDelete(SuperAdminLoginRequiredMixin, DeleteView):
    model = Category
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:categories")
    extra_context = {"is_category": True, "is_category_list": True}


# subcategory
class SubCategoryListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/subcategory/list.html"
    model = SubCategory
    context_object_name = "category_list"
    extra_context = {"is_category": True, "is_subcategory_list": True}

    def get_queryset(self):
        return SubCategory.objects.filter(is_active=True)


class SubCategoryCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = SubCategory
    template_name = "dashboard/subcategory/entry.html"
    form_class = SubCategoryForm
    success_url = reverse_lazy("main:subcategories")
    extra_context = {
        "is_category": True,
        "is_subcategory_list": True,
        "title": "Add New SubCategory",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Sub Category Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class SubCategoryUpdate(SuperAdminLoginRequiredMixin, UpdateView):
    model = SubCategory
    template_name = "dashboard/subcategory/entry.html"
    form_class = SubCategoryForm
    success_url = reverse_lazy("main:subcategories")
    extra_context = {
        "is_category": True,
        "is_subcategory_list": True,
        "is_edit": True,
        "title": "Edit Sub Category",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Sub Category Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class SubCategoryDelete(SuperAdminLoginRequiredMixin, DeleteView):
    model = SubCategory
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:subcategories")
    extra_context = {"is_category": True, "is_subcategory_list": True}


# product
class ProductListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/product/list.html"
    model = Product
    extra_context = {"is_product": True, "is_product_list": True}

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class CreateProductView(SuperAdminLoginRequiredMixin, CreateView):
    template_name = "dashboard/product/entry.html"
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy("main:product_list")
    extra_context = {
        "is_product": True,
        "is_product_list": True,
        "title": "Add New Product",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Product Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ProductUpdate(SuperAdminLoginRequiredMixin, UpdateView):
    model = Product
    template_name = "dashboard/product/entry.html"
    form_class = ProductForm
    success_url = reverse_lazy("main:product_list")
    extra_context = {
        "is_product": True,
        "is_product_list": True,
        "is_edit": True,
        "title": "Edit Product",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Product Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ProductDelete(SuperAdminLoginRequiredMixin, DeleteView):
    model = Product
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:product_list")
    extra_context = {"is_product": True}


# ProductVariant
class VariantListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/variant/list.html"
    model = ProductVariant
    extra_context = {
        "is_variant": True,
    }

    def get_queryset(self):
        return ProductVariant.objects.filter(is_active=True)


class VariantCreateView(SuperAdminLoginRequiredMixin, View):
    template_name = "dashboard/variant/entry.html"
    form_class = ProductVariantForm
    # feature_spec_formset_class = formset_factory(
    #     FeatureSpecForm, extra=1, can_delete=True
    # )
    product_image_formset_class = formset_factory(
        ProductImageForm, extra=1, can_delete=True
    )

    def get(self, request, *args, **kwargs):
        # feature_spec_formset = self.feature_spec_formset_class(
        #     prefix="feature_spec_formset"
        # )
        product_image_formset = self.product_image_formset_class(
            prefix="product_image_formset"
        )
        product_form = self.form_class()
        context = {
            "is_variant": True,
            "title": "Add New Product Variant",
            # "feature_spec_formset": feature_spec_formset,
            "product_image_formset": product_image_formset,
            "form": product_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        product_image_formset = self.product_image_formset_class(
            request.POST, request.FILES, prefix="product_image_formset"
        )
        # feature_spec_formset = self.feature_spec_formset_class(
        #     request.POST, prefix="feature_spec_formset"
        # )
        product_form = self.form_class(request.POST, request.FILES)

        if (
            # feature_spec_formset.is_valid() and
            product_form.is_valid()
            and product_image_formset.is_valid()
        ):
            product = product_form.save()

            # for variant_form in feature_spec_formset:
            #     variant_data = variant_form.save(commit=False)
            #     variant_data.product_varient = product
            #     variant_data.save()

            for image_form in product_image_formset:
                image_data = image_form.save(commit=False)
                image_data.product_varient = product
                image_data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Product Variant Created successfully.",
            }
            return JsonResponse(response_data)
        else:
            message = ""
            if product_form.errors:
                message += str(product_form.errors)
            # if feature_spec_formset.errors:
            #     message += str(feature_spec_formset.errors)
            if product_image_formset.errors:
                message += str(product_image_formset.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
                "message": message,
            }
            return JsonResponse(response_data)


class VariantUpdateView(SuperAdminLoginRequiredMixin, View):
    template_name = "dashboard/variant/entry.html"

    def get(self, request, pk):
        instance = get_object_or_404(ProductVariant, pk=pk)

        # Move DB queries inside method
        extra = (
            0
            if ProductImage.objects.filter(
                 product_varient=instance, product_varient__is_active=True
            ).exists()
            else 1
        )
        # extra1 = (
        #     0
        #     if FeatureSpec.objects.filter(
        #         product_varient=instance, product_varient__is_active=True
        #     ).exists()
        #     else 1
        # )

        ImageFormSet = inlineformset_factory(
            ProductVariant,
            ProductImage,
            can_delete=True,
            extra=extra,
            min_num=1,
            fields=("image",),
            widgets={
                "image": forms.FileInput(
                    attrs={"class": "file-input required", "type": "file"}
                )
            },
        )

        # FeaturesFormSet = inlineformset_factory(
        #     ProductVariant,
        #     FeatureSpec,
        #     can_delete=True,
        #     extra=extra1,
        #     min_num=1,
        #     fields=("feature", "specification_value", "specification_name"),
        #     widgets={
        #         "feature": forms.Select(attrs={"class": "form-select"}),
        #         "specification_name": forms.TextInput(
        #             attrs={
        #                 "placeholder": "Specification Title",
        #                 "class": "form-control",
        #             }
        #         ),
        #         "specification_value": forms.TextInput(
        #             attrs={
        #                 "placeholder": " Specification Value",
        #                 "class": "form-control",
        #             }
        #         ),
        #     },
        # )

        form = ProductVariantForm(instance=instance)
        product_image_formset = ImageFormSet(
            prefix="product_image_formset", instance=instance
        )
        # feature_spec_formset = FeaturesFormSet(
        #     prefix="feature_spec_formset", instance=instance
        # )

        context = {
            "form": form,
            "title": "Edit Product Variant",
            "product_image_formset": product_image_formset,
            # "feature_spec_formset": feature_spec_formset,
            "is_edit": True,
            "is_variant": True,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        instance = get_object_or_404(ProductVariant, pk=pk)
        form = ProductVariantForm(request.POST, request.FILES, instance=instance)

        # Move DB queries inside method
        extra = (
            0
            if ProductImage.objects.filter(
                product_varient=instance,  product_varient__is_active=True
            ).exists()
            else 1
        )
        # extra1 = (
        #     0
        #     if FeatureSpec.objects.filter(
        #         product_varient=instance,  product_varient__is_active=True
        #     ).exists()
        #     else 1
        # )

        ImageFormSet = inlineformset_factory(
            ProductVariant,
            ProductImage,
            can_delete=True,
            extra=extra,
            min_num=1,
            fields=("image",),
            widgets={
                "image": forms.FileInput(
                    attrs={"class": "file-input required", "type": "file"}
                )
            },
        )

        # FeaturesFormSet = inlineformset_factory(
        #     ProductVariant,
        #     FeatureSpec,
        #     can_delete=True,
        #     extra=extra1,
        #     min_num=1,
        #     fields=("feature", "specification_value", "specification_name"),
        #     widgets={
        #         "feature": forms.Select(attrs={"class": "form-select"}),
        #         "specification_name": forms.TextInput(
        #             attrs={
        #                 "placeholder": "Specification Title",
        #                 "class": "form-control",
        #             }
        #         ),
        #         "specification_value": forms.TextInput(
        #             attrs={
        #                 "placeholder": " Specification Value",
        #                 "class": "form-control",
        #             }
        #         ),
        #     },
        # )

        product_image_formset = ImageFormSet(
            request.POST,
            request.FILES,
            prefix="product_image_formset",
            instance=instance,
        )
        # feature_spec_formset = FeaturesFormSet(
        #     request.POST,
        #     request.FILES,
        #     prefix="feature_spec_formset",
        #     instance=instance,
        # )

        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            # if feature_spec_formset.is_valid():
            #     FeatureSpec.objects.filter( product_varient=data.pk).delete()
            #     for f0 in feature_spec_formset:
            #         data1 = f0.save(commit=False)
            #         data1.product_varient = data
            #         data1.save()
            # else:
            #     print("feature_spec_formset--", feature_spec_formset.errors)

            if product_image_formset.is_valid():
                ProductImage.objects.filter(product_varient=data.pk).delete()
                for f1 in product_image_formset:
                    data2 = f1.save(commit=False)
                    data2.product_varient = data
                    data2.save()

                response_data = {
                    "status": "true",
                    "title": "Successfully Submitted",
                    "message": "Variant Updated successfully.",
                }
                return JsonResponse(response_data)
            else:
                print("product_image_formset--", product_image_formset.errors)

        message = ""
        if form.errors:
            message += str(form.errors)
        if product_image_formset.errors:
            message += str(product_image_formset.errors)
        # if feature_spec_formset.errors:
        #     message += str(feature_spec_formset.errors)

        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": message,
        }
        return JsonResponse(response_data)


class VarianteDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = ProductVariant
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:variants")
    extra_context = {"is_variant": True}


# parchase
class PurchaseListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/purchase/list.html"
    model = Purchase
    extra_context = {"is_purchase_list": True}

    def get_queryset(self):
        return Purchase.objects.filter(is_active=True)


class PurchaseCreateView(SuperAdminLoginRequiredMixin, View):
    template_name = "dashboard/purchase/entry.html"
    form_class = PurchaseForm
    products_formset_class = formset_factory(
        PurchaseProductForm, extra=1, can_delete=True
    )

    def get(self, request, *args, **kwargs):
        products_formset = self.products_formset_class(prefix="products_formset")
        context = {
            "is_purchase_list": True,
            "title": "Add New Purchase",
            "products_formset": products_formset,
            "form": self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        products_formset = self.products_formset_class(
            request.POST, prefix="products_formset"
        )
        purchase_form = self.form_class(request.POST)

        if products_formset.is_valid() and purchase_form.is_valid():
            purchase = purchase_form.save()

            for product_form in products_formset:
                product_data = product_form.save(commit=False)
                product_data.purchase = purchase
                product_data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Purchase Created successfully.",
            }
            return JsonResponse(response_data)
        else:
            message = ""
            if purchase_form.errors:
                message += str(purchase_form.errors)
            if products_formset.errors:
                message += str(products_formset.errors)

            response_data = {
                "status": "false",
                "title": "Form validation error",
                "message": message,
            }
            return JsonResponse(response_data)


class PurchaseUpdateView(SuperAdminLoginRequiredMixin, View):
    template_name = "dashboard/purchase/entry.html"
    PurchaseProductFormSet = inlineformset_factory(
        Purchase,
        PurchaseProduct,
        can_delete=True,
        extra=0,
        fields=("product_varient", "quantity"),
        widgets={
            "product_varient": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.TextInput(
                attrs={
                    "placeholder": "Quantity",
                    "class": "form-control",
                    "type": "number",
                }
            ),
        },
    )

    def get(self, request, pk):
        instance = get_object_or_404(Purchase.objects.filter(pk=pk))
        form = PurchaseForm(instance=instance)
        products_formset = self.PurchaseProductFormSet(
            prefix="products_formset", instance=instance
        )
        context = {
            "form": form,
            "title": "Edit Purchase",
            "is_purchase_list": True,
            "products_formset": products_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        instance = get_object_or_404(Purchase.objects.filter(pk=pk))
        form = PurchaseForm(request.POST, instance=instance)
        products_formset = self.PurchaseProductFormSet(
            request.POST, prefix="products_formset", instance=instance
        )

        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            if products_formset.is_valid():
                PurchaseProduct.objects.filter(purchase=data.pk).delete()
                for f0 in products_formset:
                    data2 = f0.save(commit=False)
                    data2.purchase = data
                    data2.save()

                response_data = {
                    "status": "true",
                    "title": "Successfully Submitted",
                    "message": "Purchase Updated successfully.",
                }
                return JsonResponse(response_data)

        message = ""
        if form.errors:
            message += str(form.errors)
        if products_formset.errors:
            message += str(products_formset.errors)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": message,
        }
        return JsonResponse(response_data)


class PurchaseDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:purchase_list")
    extra_context = {"is_purchase": True}


# customer
class CustomerListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/customer/list.html"
    model = User
    extra_context = {"is_customer": True}


# review
class ReviewListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/review/list.html"
    model = Review
    extra_context = {"is_review": True}


class ReviewCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Review
    template_name = "dashboard/review/entry.html"
    form_class = ReviewForm
    success_url = reverse_lazy("main:review_list")
    extra_context = {"is_review": True, "title": "Add New Review"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Review Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ReviewUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Review
    template_name = "dashboard/review/entry.html"
    form_class = ReviewForm
    success_url = reverse_lazy("main:review_list")
    extra_context = {"is_review": True, "title": "Edit Review"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Review Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ReviewDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Review
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:review_list")


# banner
class BannerListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/banner/list.html"
    model = Banner
    extra_context = {"is_banner": True}
    extra_context = {"is_banner": True, "title": " Banner List"}


class BannerCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Banner
    template_name = "dashboard/banner/entry.html"
    form_class = BannerForm
    success_url = reverse_lazy("main:banners")
    extra_context = {"is_banner": True, "title": "Add New Banner"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Banner Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class BannerUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Banner
    template_name = "dashboard/banner/entry.html"
    form_class = BannerForm
    success_url = reverse_lazy("main:banners")
    extra_context = {"is_Banner": True, "title": "Banner Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Banner Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class BannerDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Banner
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:banners")


# Category List
class CategoryListListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/categorylist/list.html"
    model = CategoryList
    context_object_name = "categorylist_list"
    extra_context = {"is_category": True, "is_categorylist_list": True}

    def get_queryset(self):
        return CategoryList.objects.filter(is_active=True)


class CategoryListCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = CategoryList
    template_name = "dashboard/categorylist/entry.html"
    form_class = CategoryListForm
    success_url = reverse_lazy("main:categorylists")
    extra_context = {
        "is_category": True,
        "is_categorylist_list": True,
        "title": "Add New Category List",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Category List Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class CategoryListUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = CategoryList
    template_name = "dashboard/categorylist/entry.html"
    form_class = CategoryListForm
    success_url = reverse_lazy("main:categorylists")
    extra_context = {
        "is_category": True,
        "is_categorylist_list": True,
        "is_edit": True,
        "title": "Edit Category List",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Category List Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class CategoryListDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = CategoryList
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:categorylists")
    extra_context = {
        "is_category": True,
        "is_categorylist_list": True,
    }


# Gift Card",
class GiftCardListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/giftcard/list.html"
    model = GiftCard
    context_object_name = "giftcard_list"
    extra_context = {"is_giftcard": True, "is_giftcard_list": True}

    def get_queryset(self):
        return GiftCard.objects.filter(is_active=True)


class GiftCardCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = GiftCard
    template_name = "dashboard/giftcard/entry.html"
    form_class = GiftCardForm
    success_url = reverse_lazy("main:giftcards")
    extra_context = {
        "is_giftcard": True,
        "is_giftcard_list": True,
        "title": "Add New Gift Card",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Gift Card Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class GiftCardUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = GiftCard
    template_name = "dashboard/giftcard/entry.html"
    form_class = GiftCardForm
    success_url = reverse_lazy("main:giftcards")
    extra_context = {
        "is_giftcard": True,
        "is_giftcard_list": True,
        "is_edit": True,
        "title": "Edit Gift Card",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Gift Card Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class GiftCardDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = GiftCard
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:giftcards")
    extra_context = {
        "is_giftcard": True,
        "is_giftcard_list": True,
    }


# City CRUD
class CityListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/city/list.html"
    model = City
    context_object_name = "city_list"
    extra_context = {"is_city": True} 

    
class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    template_name = "dashboard/city/entry.html"
    success_url = reverse_lazy("main:cities")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["pincode_formset"] = PincodeFormSet(self.request.POST)
        else:
            context["pincode_formset"] = PincodeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        pincode_formset = context["pincode_formset"]

        if form.is_valid() and pincode_formset.is_valid():
            self.object = form.save()
            pincode_formset.instance = self.object  # ✅ Ensure Pincode links to City
            pincode_formset.save()

            response_data = {
                "status": "true", 
                "title": "Success",
                "message": "City and Pincodes saved successfully!"
            }
            return JsonResponse(response_data)

        return JsonResponse({"status": "error", "message": "Form submission failed."}, status=400)

class CityUpdateView(UpdateView):
    model = City
    form_class = CityForm
    template_name = "dashboard/city/entry.html"
    success_url = reverse_lazy("main:cities")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Define a formset with extra=0 for update view
        PincodeFormSetNoExtra = inlineformset_factory(
            City, Pincode, form=PincodeForm, extra=0
        )

        if self.request.POST:
            context["pincode_formset"] = PincodeFormSetNoExtra(self.request.POST, instance=self.object)
        else:
            context["pincode_formset"] = PincodeFormSetNoExtra(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        pincode_formset = context["pincode_formset"]

        if form.is_valid() and pincode_formset.is_valid():
            self.object = form.save()
            pincode_formset.instance = self.object 
            pincode_formset.save()

            return JsonResponse({
                "status": "true",  # Note: match this to JS expectations
                "title": "Success",
                "message": "City and Pincodes updated successfully!"
            })
        

        # return JsonResponse({
        #     "status": "false",
        #     "title": "Error",
        #     "message": "Form submission failed."
        # }, status=400)

        else:
            print("Form errors:", form.errors)
            print("Formset errors:", pincode_formset.errors)
            print("Management form errors:", pincode_formset.management_form.errors)
            return JsonResponse({
                "status": "false",
                "title": "Error",
                "message": "Form submission failed."
            }, status=400)

class CityDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = City
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:cities")
    extra_context = {"is_city": True}

# Pincode CRUD
class PincodeListView(SuperAdminLoginRequiredMixin, ListView):
    model = Pincode
    template_name = "dashboard/pincode/list.html"
    context_object_name = "pincodes"
    extra_context = {"is_pincode": True}

class PincodeCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Pincode
    template_name = "dashboard/pincode/entry.html"
    form_class = PincodeForm
    success_url = reverse_lazy("main:pincodes")
    extra_context = {"is_pincode": True, "title": "Add Pincode"}

    def form_valid(self, form):
        response = super().form_valid(form)
        return JsonResponse({"status": "true", "message": "Pincode added successfully!"})

    def form_invalid(self, form):
        return JsonResponse({"status": "false", "message": str(form.errors)})

class PincodeUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Pincode
    template_name = "dashboard/pincode/entry.html"
    form_class = PincodeForm
    success_url = reverse_lazy("main:pincodes")
    extra_context = {"is_pincode": True, "title": "Edit Pincode"}

    def form_valid(self, form):
        response = super().form_valid(form)
        return JsonResponse({"status": "true", "message": "Pincode updated successfully!"})

    def form_invalid(self, form):
        return JsonResponse({"status": "false", "message": str(form.errors)})

class PincodeDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Pincode
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:pincodes")
    extra_context = {"is_pincode": True}