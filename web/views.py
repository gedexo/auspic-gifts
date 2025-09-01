from decimal import Decimal

# PHONEPAY
import razorpay
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Min
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from decimal import Decimal, InvalidOperation
from datetime import date

# model
# form
from order.forms import OrderForm, TrackingForm
from order.models import AdditionalInfo, Order, OrderItem, Tracking, Wishlist
from products.forms import ReviewForm
from products.models import Brand, Category, CategoryList, ProductVariant, SubCategory,Product
from web.forms import ContactForm
from web.models import Banner

from .cart import Cart
from django.template.loader import render_to_string

client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY, settings.RAZOR_PAY_SECRET))


class IndexView(TemplateView):
    template_name = "web/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "")
        print(query)

        category_products = CategoryList.objects.all()[:4]
        context["category_products"] = category_products
        pincode = self.request.GET.get("pincode", None)

        context["categories"] = Category.objects.filter(is_list_home=True).order_by('order')
        products = ProductVariant.objects.filter(is_active=True)

        # ✅ Corrected: Only apply the filter if pincode is provided
        if pincode:
            pincode_obj = Pincode.objects.filter(code=pincode).first()
            if pincode_obj:
                city = pincode_obj.city
                products = products.filter(product__cities=city)  # ✅ Apply filter directly to 'products'

        if query:
            products = products.filter(product__product_name__icontains=query)

        context["brands"] = Brand.objects.filter(is_active=True)
        context["popular_products"] = products.filter(is_popular=True)
        context["trending_products"] = products.filter(is_trend=True)
        context["best_seller_products"] = products.filter(is_best_seller=True)
        context["new_arrival_products"] = products.filter(is_new_arrival=True)
        context["is_offer"] = products.filter(is_offer=True)
        context["main_banners"] = Banner.objects.filter(is_active=True, position="main")
        context["query"] = query
        context["main_banners_mobile"] = Banner.objects.filter(
            is_active=True, position="main_mobile"
        )
        context["popular_product_block_banners"] = Banner.objects.filter(
            is_active=True, position="popular_product_block"
        )
        context["best_selling_block_banners"] = Banner.objects.filter(
            is_active=True, position="best_selling_block"
        )
        context["new_arrival_block_banners"] = Banner.objects.filter(
            is_active=True, position="new_arrival_block"
        )
        context["new_arrival_block_left_image"] = Banner.objects.filter(
            is_active=True, position="new_arrival_block_left_image"
        ).last()
        context["curated_gifts"] = Banner.objects.filter(
            is_active=True, position="curated_gifts"
        )[:7]

        cart = Cart(self.request)
        cart_items = []

        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(ProductVariant, id=item_id)
            quantity = item_data["quantity"]
            total_price = Decimal(item_data["selling_price"]) * quantity
            cart_items.append(
                {
                    "variant": variant,
                    "quantity": quantity,
                    "total_price": total_price,
                }
            )

        context["cart_items"] = cart_items
        context["cart_total"] = sum(
            Decimal(item[1]["quantity"]) * Decimal(item[1]["selling_price"])
            for item in cart.get_cart()
        )

        return context


class ShopView(FilterView, ListView):
    model = ProductVariant
    template_name = "web/shop.html"
    context_object_name = "products"
    filterset_fields = {"product__category": ["exact"]}
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        category_slug = self.request.GET.get("category", None)
        selected_brands = self.request.GET.getlist("product__brand", [])
        price_range = self.request.GET.get("selling_price__range", None)
        sort_by = self.request.GET.get("sort_by", None)
        pincode = self.request.GET.get("pincode", None)
        category_title = None

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            
            all_categories = category.get_descendants(include_self=True)
            queryset = queryset.filter(product__category__in=all_categories)
            category_title = category.name

        

        if selected_brands:
            selected_brands = [brand_id for brand_id in selected_brands if brand_id]
            queryset = queryset.filter(product__brand__id__in=selected_brands)

        if price_range:
            amount = price_range.replace("QAR", "")
            min_amount, max_amount = map(int, amount.split("-"))
            queryset = queryset.filter(selling_price__gte=min_amount, selling_price__lte=max_amount).distinct()

        if pincode:
            pincode_obj = Pincode.objects.filter(code=pincode).first()
            if pincode_obj:
                queryset = queryset.filter(product__cities=pincode_obj.city)

        if sort_by:
            if sort_by == "low_to_high":
                queryset = queryset.order_by("selling_price")
            elif sort_by == "high_to_low":
                queryset = queryset.order_by("-selling_price")
            elif sort_by == "rating":
                queryset = queryset.annotate(min_rating=Min("reviews__rating")).order_by("-min_rating")
            else:
                queryset = queryset.order_by("-id")

        self.category_title = category_title
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "")

        # Filtering products based on search query
        products = ProductVariant.objects.filter(is_active=True)
        if query:
            products = products.filter(product__product_name__icontains=query)

        context["brands"] = Brand.objects.filter(is_active=True)
        context["selected_brands"] = self.request.GET.getlist("product__brand")
        context["query"] = query
        context["category_title"] = self.category_title
        context["categories"] = Category.objects.filter(is_list_home=True)

        # Handling Cart Items
        cart = Cart(self.request)
        cart_items = []
        cart_total = Decimal(0)

        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(ProductVariant, id=item_id)
            quantity = item_data["quantity"]
            total_price = Decimal(item_data["selling_price"]) * quantity
            cart_total += total_price
            cart_items.append({"variant": variant, "quantity": quantity, "total_price": total_price})

        context["cart_items"] = cart_items
        context["cart_total"] = cart_total

        return context


class ProductDetailView(DetailView):
    model = ProductVariant
    template_name = "web/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_product = self.get_object()
        product_ratings = [
            {"value": 5, "percentage": int(current_product.five_rating())},
            {"value": 4, "percentage": int(current_product.four_rating())},
            {"value": 3, "percentage": int(current_product.three_rating())},
            {"value": 2, "percentage": int(current_product.two_rating())},
            {"value": 1, "percentage": int(current_product.one_rating())},
        ]
        context["reviews"] = current_product.reviews.filter(approval=True)
        context["review_form"] = ReviewForm()
        context["product_ratings"] = product_ratings
        context["is_product_detail"] = True

        cart = Cart(self.request)
        cart_items = []

        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(ProductVariant, id=item_id)
            quantity = item_data["quantity"]
            total_price = Decimal(item_data["selling_price"]) * quantity
            cart_items.append(
                {
                    "variant": variant,
                    "quantity": quantity,
                    "total_price": total_price,
                }
            )

        context["cart_items"] = cart_items
        context["cart_total"] = sum(
            Decimal(item[1]["quantity"]) * Decimal(item[1]["selling_price"])
            for item in cart.get_cart()
        )
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.instance.product = product
            form.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Message successfully Submitted",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
                "message": form.errors,
            }
        return JsonResponse(response_data)


class CheckoutView(LoginRequiredMixin, View):
    template_name = "web/shop-checkout.html"

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        form = OrderForm()

        user = request.user

        context = {
            "cart_items": cart_items,
            "cart_total": sum(
                Decimal(item["total_price"]) for item in cart_items
            ),
            "form": form,
            "user_details": {
                "full_name": user.get_username() or user.username,
                "phone_number": user.mobile_number or "Not Provided",
                "email": user.email,
        },
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)

        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user  # Assign the logged-in user
            data.delivery_date = form.cleaned_data["selected_date"]
            data.delivery_date = date.today() 

            print(data.delivery_date == "select_date", data.delivery_date)

            try:
                data.subtotal = Decimal(request.POST.get("payable") or 0)
                data.service_fee = Decimal(request.POST.get("service_fee") or 0)
                data.shipping_fee = Decimal(request.POST.get("shipping_fee") or 0)
                data.gift_code = request.POST.get("gift_code", "").strip()
                data.gift_discount = Decimal(request.POST.get("gift_discount") or 0)

                # Ensure payable is never below ₹1
                calculated_payable = data.subtotal + data.service_fee + data.shipping_fee - data.gift_discount
                data.payable = max(calculated_payable, Decimal("1.00"))
            
            except InvalidOperation:
                context = {
                    "cart_items": cart_items,
                    "cart_total": sum(item["total_price"] for item in cart_items),
                    "form": form,
                    "error": "Invalid number format. Please check your inputs."
                }
                return render(request, self.template_name, context)

            data.save()  # Save the order with the user

            # **Create Order Items**
            for item in cart.get_cart():
                item_id = item[0]  # Get product variant ID
                item_data = item[1]

                variant = get_object_or_404(ProductVariant, id=item_id)
                quantity = int(item_data["quantity"])
                amount = Decimal(item_data["selling_price"])
                message = item_data.get("cakemessage", "")
                size = item_data.get("size", "")


                OrderItem.objects.create(
                    order=data,
                    product_variant=variant,
                    quantity=quantity,
                    amount=amount,
                    cakemessage=message,
                    size=size
                )

            # Clear the cart after order placement
            cart.clear()

            payment_option = request.POST.get("payment_option")
            if payment_option == "COD":
                return redirect("web:complete_order", pk=data.pk)


            return redirect("web:order_list",pk=data.pk)

        context = {
            "cart_items": cart_items,
            "cart_total": sum(item["total_price"] for item in cart_items),
            "form": form,
            "error": "There was an issue with your order. Please check all fields."
        }
        return render(request, self.template_name, context)

    def get_cart_items(self, cart):
        cart_items = []
        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(ProductVariant, id=item_id)
            quantity = item_data["quantity"]
            total_price = Decimal(item_data["selling_price"]) * quantity
            message = item_data.get("cakemessage", "")
            cart_items.append(
                {
                    "variant": variant,
                    "quantity": quantity,
                    "total_price": total_price,
                    "cakemessage": message,
                    "size": item_data.get("size", ""),
                }
            )
        return cart_items


class OrderSummaryView(DetailView):
    model = Order
    template_name = "web/order_summary.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()

        context["order_items"] = order.get_items()  # Get items in this order
        context["razorpay_key"] = settings.RAZOR_PAY_KEY  # Pass Razorpay Key for Payment
        context["user_details"] = self.request.user  # Add logged-in user details

        return context


    
class PaymentView(DetailView):
    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)

        # Ensure payable amount is valid
        if order.payable is None or order.payable < Decimal("1.00"):
            return render(request, "web/payment_error.html", {"error": "Minimum payment amount must be ₹1."})

        currency = "INR"
        amount = float(order.payable) * 100  # Convert to paise

        try:
            razorpay_order = client.order.create(
                {"amount": amount, "currency": currency, "payment_capture": "1"}
            )
            razorpay_order_id = razorpay_order["id"]
            order.razorpay_order_id = razorpay_order_id
            order.save()
        except razorpay.errors.BadRequestError as e:
            return render(request, "web/payment_error.html", {"error": str(e)})

        context = {
            "object": order,
            "amount": amount,
            "razorpay_key": settings.RAZOR_PAY_KEY,
            "razorpay_order_id": razorpay_order_id,
            "callback_url": f"{settings.DOMAIN}/callback/{order.pk}/",
        }
        return render(request, "web/payment.html", context=context)
    

@csrf_exempt
def callback(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        response_data = {
            "razorpay_order_id": provider_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature_id,
        }

        order = Order.objects.get(razorpay_order_id=provider_order_id)
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature_id
        client = razorpay.Client(
            auth=(settings.RAZOR_PAY_KEY, settings.RAZOR_PAY_SECRET)
        )
        result = client.utility.verify_payment_signature(response_data)

        if result is not None:
            print("Signature verification successful")
            order.is_ordered = True
            order.order_status = "Placed"
            order.payment_status = "Success"
            order.save()

            products = ""
            total = 0
            counter = 1
            for item in order.get_items():
                products += f"{counter}.{item.product_variant} ({item.quantity}x{item.amount}) QAR {item.subtotal()} \n ----------------------- \n"
                total += item.subtotal()
                counter += 1

            message = (
                f"============================\n"
                f"Order Confirmed\n"
                f"============================\n\n"
                f"Order ID: {order.order_id}\n"
                f"Order Date: {order.created}\n"
                f"Order Status: Placed\n"
                f"Payment Method: Online Payment\n"
                f"Payment Status: Success\n"
                f"----------------------------\n\n"
                f"Products:\n\n"
                f"{products}\n\n"
                f"----------------------------\n\n"
                f"Order Summary:\n\n"
                f"Subtotal: {order.subtotal} \n"
                f"service fee: {order.service_fee} \n"
                f"shipping fee: {order.shipping_fee} \n\n"
                f"Total Payble: {order.payable} \n\n"
                f"----------------------------\n\n"
                f"Shipping Address:\n\n"
                f"Name: {order.full_name}\n"
                f"Address: {order.address_line_1}\n"
                f"Landmark: {order.address_line_2}\n"
                f"State: {order.state}\n"
                f"District: {order.district}\n"
                f"City: {order.city}\n"
                f"Pincode: {order.pin_code}\n"
                f"Mobile: {order.mobile_no}\n"
                f"Email: {order.email}\n\n"
                f"Thank you for placing your order with auspic. Your order has been confirmed.\n\n"
            )

            email = order.email
            subject = "Order Confirmation - auspic"
            message = message
            send_mail(
                subject,
                message,
                "contact@auspicgifts.com",
                [email, "contact@auspicgifts.com"],
                fail_silently=False,
            )

            print("email sent successfully")
            cart = Cart(request)
            cart.clear()

        else:
            print("Signature verification failed, please check the secret key")
            order.payment_status = "Failed"
            order.save()
        return render(request, "web/callback.html", {"object": order})
    else:
        print("Razorpay payment failed")
        return redirect("web:payment", pk=order.pk)


class CompleteOrderView(DetailView):
    model = Order
    template_name = "web/complete-order.html"

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        order.is_ordered = True
        order.order_status = "Placed"
        order.save()
        products = ""
        total = 0
        counter = 1
        for item in order.get_items():
            products += f"{counter}.{item.product_variant} ({item.quantity}x{item.amount}) QAR {item.subtotal()} \n ----------------------- \n"
            total += item.subtotal()
            counter += 1

        message = (
            f"============================\n"
            f"Order Confirmed\n"
            f"============================\n\n"
            f"Order ID: {order.order_id}\n"
            f"Order Date: {order.created}\n"
            f"Order Status: Placed\n"
            f"Payment Method: Cash On Delivery\n"
            f"Payment Status: Pending\n"
            f"----------------------------\n"
            f"Products:\n\n"
            f"{products}\n"
            f"----------------------------\n"
            f"Order Summary:\n\n"
            f"Subtotal: {order.subtotal} \n"
            f"service fee: {order.service_fee} \n"
            f"shipping fee: {order.shipping_fee} \n\n"
            f"Total Payble: {order.payable} \n\n"
            f"----------------------------\n"
            f"Shipping Address:\n\n"
            f"Name: {order.full_name}\n"
            f"Address: {order.address_line_1}\n"
            f"Landmark: {order.address_line_2}\n"
            f"State: {order.state}\n"
            f"District: {order.district}\n"
            f"City: {order.city}\n"
            f"Pincode: {order.pin_code}\n"
            f"Mobile: {order.mobile_no}\n"
            f"Email: {order.email}\n\n"
            f"Thank you for placing your order with auspic. Your order has been confirmed.\n\n"
        )

        email = order.email
        subject = "Order Confirmation - auspic"
        message = message
        send_mail(
            subject,
            message,
            "contact@auspicgifts.com",
            [email, "contact@auspicgifts.com"],
            fail_silently=False,
        )

        cart = Cart(request)
        cart.clear()
        context = {
            "object": order,
        }
        return render(request, self.template_name, context)


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        context = {
            "is_contact": True,
            "form": form,
        }
        return render(request, "web/contact.html", context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Message successfully Submitted",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
            }
        return JsonResponse(response_data)


def cart_view(request):
    cart = Cart(request)
    cart_items = []

    for item_id, item_data in cart.get_cart():
        variant = get_object_or_404(ProductVariant, id=item_id)
        quantity = item_data["quantity"]
        cakemessage = item_data.get("cakemessage", "")  
        size = item_data.get("size", "")
        total_price = Decimal(item_data["selling_price"]) * quantity
        cart_items.append(
            {
                "variant": variant,
                "quantity": quantity,
                "total_price": total_price,
                "cakemessage": cakemessage, 
                "size": size,
            }
        )
    context = {
        "cart_items": cart_items,
        "cart_total": sum(
            Decimal(item[1]["quantity"]) * Decimal(item[1]["selling_price"])
            for item in cart.get_cart()
        ),
    }

    return render(request, "web/cart.html", context)


# def cart_add(request):
#     cart = Cart(request)
#     cart_instance = cart.cart
#     quantity = request.GET.get("quantity", 1)
#     product_id = request.GET.get("product_id", "")
#     variant = get_object_or_404(ProductVariant, pk=product_id)
#     cart.add(variant, quantity=int(quantity))

#       # Prepare cart items for rendering
#     cart_items = [
#         {
#             "quantity": item["quantity"],
#             "sale_price": item["selling_price"],
#         }
#         for item in cart_instance.values()
#     ]

#     # Render updated modal HTML
#     cart_modal_html = render_to_string(
#         "web/partials/cart-modal.html", {"cart_items": cart_items}
#     )

#     wishlist_count = 0
#     if request.user.is_authenticated:
#         if Wishlist.objects.filter(user=request.user).exists():
#             wishlist_count = Wishlist.objects.filter(user=request.user).count()
#     return JsonResponse(
#         {
#             "quantity": cart.get_product_quantity(variant),
#             "total_price": cart.get_total_price(
#                 cart_instance[product_id]
#             ),  # Pass the specific item to get_total_price
#             "cart_total": cart.cart_total(),
#             "cart_count": len(cart_instance),
#             "wishlist_count": wishlist_count,

#             "quantity": cart.get_product_quantity(variant),
#             "total_price": cart.get_total_price(cart_instance[product_id]),
#             "cart_modal_html": cart_modal_html,

#         }
#     )

import json
def cart_add(request):
    cart = Cart(request)
    cart_instance = cart.cart
    quantity = request.GET.get("quantity", 1)
    product_id = request.GET.get("product_id", "")
    message = request.GET.get("message", "")
    size = request.GET.get("size", "")
    variant = get_object_or_404(ProductVariant, pk=product_id)
    cart.add(variant, quantity=int(quantity),cakemessage=message,size=size)

    
    cart_items = [
        {
            "quantity": item["quantity"],
            "sale_price": float(item["selling_price"]), 
        }
        for item in cart_instance.values()
    ]
    

    # return redirect(f"{request.META['HTTP_REFERER']}?show_modal=true")
    return redirect(f"{request.META['HTTP_REFERER']}&show_modal=true" if "?" in request.META['HTTP_REFERER'] else f"{request.META['HTTP_REFERER']}?show_modal=true")

def clear_cart_item(request, item_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=item_id)
    cart.remove(variant)
    return redirect(reverse("web:cart"))


def minus_to_cart(request):
    cart = Cart(request)
    cart_instance = cart.cart
    item_id = request.GET.get("item_id")
    variant = get_object_or_404(ProductVariant, id=item_id)
    cart.decrease_quantity(variant)
    return JsonResponse(
        {
            "quantity": cart.get_product_quantity(variant),
            "total_price": cart.get_total_price(
                cart_instance[item_id]
            ),  # Pass the specific item to get_total_price
            "cart_total": cart.cart_total(),
        }
    )
def cart_plus(request):
    
    cart = Cart(request)
    cart_instance = cart.cart
    item_id = request.GET.get("item_id")
    quantity = request.GET.get("quantity", 1)
    variant = get_object_or_404(ProductVariant, id=item_id)
    cart.add(variant, quantity=int(quantity))
    return JsonResponse(
        {
            "quantity": cart.get_product_quantity(variant),
            "total_price": cart.get_total_price(
                cart_instance[item_id]
            ),  # Pass the specific item to get_total_price
            "cart_total": cart.cart_total(),
        }
    )

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect(reverse("web:shop"))


def tracking(request):
    if request.method == "GET":
        form = TrackingForm(request.GET)
        if form.is_valid():
            order_id = form.cleaned_data["tracking_id"]  # This is the Order's ID now
            try:
                order = Order.objects.get(order_id=order_id)
                tracking_object = Tracking.objects.get(
                    tracking_id=order
                )  # Matching the order ID
                procedure = tracking_object.procedure
                additional = AdditionalInfo.objects.filter(tracking=tracking_object)

                return render(
                    request,
                    "web/tracking.html",
                    {
                        "tracking_id": order_id,
                        "procedure": procedure,
                        "button": "Track another order",
                        "is_tracking": True,
                        "tracking_object": tracking_object,
                        "additional": additional,
                    },
                )
            except (Tracking.DoesNotExist, Order.DoesNotExist):
                error_message = "Tracking ID not found."
                return render(
                    request,
                    "web/tracking.html",
                    {
                        "form": form,
                        "error_message": error_message,
                        "button": "Tracking",
                        "is_tracking": True,
                    },
                )
    else:
        form = TrackingForm()

    context = {
        "form": form,
        "is_tracking": True,
        "button": "Tracking",
    }

    return render(request, "web/tracking.html", context)

def cart_remove(request):
    cart = Cart(request)
    cart_instance = cart.cart
    product_id = request.GET.get("product_id", "")
    variant = get_object_or_404(ProductVariant, pk=product_id)
    
    # Remove the variant from the cart.
    # Depending on your implementation, this might reduce the quantity
    # or remove the item if quantity becomes 0.
    cart.decrease_quantity(variant)

    # Optionally, update cart items info if needed
    cart_items = [
        {
            "quantity": item["quantity"],
            "sale_price": float(item["selling_price"]),
        }
        for item in cart_instance.values()
    ]
    
    # Redirect back to the referring page with the show_modal flag
    referrer = request.META.get("HTTP_REFERER", "/")
    if "?" in referrer:
        return redirect(f"{referrer}&show_modal=true")
    else:
        return redirect(f"{referrer}?show_modal=true")
    


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from order.models import GiftCard

@csrf_exempt
def apply_gift_card(request):
    if request.method == "POST":
        data = json.loads(request.body)
        gift_code = data.get("gift_code", "").strip()

        try:
            gift_card = GiftCard.objects.get(code=gift_code, is_active=True)
            if gift_card.is_valid():
                discount = float(gift_card.balance)
                subtotal = float(request.session.get("cart_total", 0.00))
                new_total = max(subtotal - discount, 0.00)

                return JsonResponse({"success": True, "discount": discount, "new_total": new_total})
            else:
                return JsonResponse({"success": False, "message": "Gift card is expired or invalid."})
        except GiftCard.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid gift code."})

    return JsonResponse({"success": False, "message": "Invalid request."})



import requests
from django.http import JsonResponse
from products.models import City, Pincode

def fetch_pincode_details(pincode):
    """Fetch city from India Post API and save to database."""
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    response = requests.get(url)
    data = response.json()
    
    if data[0]['Status'] == "Success":
        city_name = data[0]['PostOffice'][0]['District']
        city, _ = City.objects.get_or_create(name=city_name)
        Pincode.objects.get_or_create(city=city, code=pincode)
        return city_name
    return None

def check_pincode_ajax(request):
    if request.method == "POST":
        pincode = request.POST.get("pincode", "").strip()
        
        pincode_obj = Pincode.objects.filter(code=pincode).first()
        if pincode_obj:
            city = pincode_obj.city
            products = Product.objects.filter(cities=city).values("product_name")

            return JsonResponse({
                "status": "success",
                "city": city.name,
                "products": list(products),
            })
        else:
            return JsonResponse({"status": "error", "message": "Pincode not found."})

    return JsonResponse({"status": "error", "message": "Invalid request."})


def handler404(request, exception):
    return render(request, "web/404.html", status=404)

class CollectionView(ListView):
    template_name = "web/shop.html"
    context_object_name = "products"
    paginate_by =10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        context['page_name'] = 'Shop'
        if slug == 'bestseller':
            context['page_name'] = 'Best Seller'
        elif slug == 'new':
            context['page_name'] = 'New Collection'
        elif slug:
            context['page_name'] = str(Category.objects.get(slug=slug))
        return context

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        slug = self.kwargs.get('slug')
        filter_param = self.request.GET.get('filter')  # Retrieve filter value from query params

        # Filter by slug (category/bestseller/new)
        if slug:
            if slug.lower() == 'bestseller':
                queryset = queryset.filter(is_best_seller=True)
            elif slug.lower() == 'new':
                queryset = queryset.filter(is_new_arrival=True)
            else:
                category = get_object_or_404(Category, slug=slug)
                descendants = category.get_descendants(include_self=True)
                queryset = queryset.filter(category__in=descendants)

        # Apply additional filters
        if filter_param:
            if filter_param == 'sort_by_popularity':
                queryset = queryset.filter(is_popular=True)
            elif filter_param == 'latest':
                queryset = queryset.order_by('-id')
            
            elif filter_param == 'low-to-high':
                queryset = queryset.annotate(min_price=Min('variants__selling_price')).order_by('min_price')
            elif filter_param == 'high-to-low':
                queryset = queryset.annotate(max_price=Max('variants__selling_price')).order_by('-max_price')
              
            elif filter_param == 'most-reviews':
                queryset = queryset.order_by('-review_count')

        return queryset
