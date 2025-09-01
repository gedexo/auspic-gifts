import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import date, timedelta
from accounts.models import User

from web.base import BaseModel


def generate_order_id():
    timestamp = timezone.now().strftime("%y%m%d")
    unique_id = uuid.uuid4().hex[:6]  # Generate a random 8-character string
    return f"{timestamp}{unique_id.upper()}"


class Order(BaseModel):
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    created = models.DateTimeField(db_index=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payable = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_id = models.CharField(max_length=255, default=generate_order_id)
    is_ordered = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    payment_method = models.CharField(
        max_length=20,
        choices=(("COD", "Cash On Delivery"), ("OP", "Online Payment")),
        default="COD",
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address_line_1 = models.CharField("Complete Address", max_length=100)
    address_line_2 = models.CharField("Landmark", max_length=100)
    state = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100)
    pin_code = models.IntegerField()
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField()

    gift_code = models.CharField(max_length=20, blank=True, null=True)
    gift_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,blank=True, null=True)
    delivery_date = models.DateField(null=True, blank=True)
    time_slot = models.CharField(
        max_length=10,
        choices=[("9-12", "9:00 AM - 12:00 PM"), ("12-6", "12:00 PM - 6:00 PM")],
        default="9-12"
    )

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Placed", "Order Placed"),
            ("Shipped", "Order Shipped"),
            ("InTransit", "In Transit"),
            ("Delivered", "Order Delivered"),
            ("Cancelled", "Order Cancelled"),
        ),
    )
    payment_status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Failed", "Failed"),
            ("Success", "Success"),
            ("Cancelled", "Cancelled"),
        ),
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ("-id",)

    def get_items(self):
        return OrderItem.objects.filter(order=self)

    def order_total(self):
        return float(sum([item.subtotal for item in self.get_items()]))

    def get_user_absolute_url(self):
        return reverse("accounts:order_detail", kwargs={"order_id": self.order_id})

    def __str__(self):
        return f"{self.order_id}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(
        "products.ProductVariant", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cakemessage = models.CharField(max_length=25, blank=True, null=True)
    size = models.CharField(max_length=25, blank=True, null=True)

    

    def __str__(self):
        return f"{self.product_variant} - {self.quantity}"

    def subtotal(self):
        return self.amount * self.quantity


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_varients = models.ForeignKey(
        "products.ProductVariant", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} - {self.product_varients}"


class City(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ("order",)
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class DestinationPlace(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Tracking(models.Model):
    tracking_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="Tracking ID"
    )
    mobile_number = models.CharField(max_length=100, null=True, blank=True)
    TRACKING_CHOICES = [
        ("Departed", "Departed From Shop"),
        ("Dispatch", "Dispatch"),
        ("Destination", "At Destination"),
        ("Deliverd", "Deliverd"),
        ("Pending", "Pending"),
    ]
    procedure = models.CharField(
        "status", max_length=100, choices=TRACKING_CHOICES, default="Departed"
    )
    destination_place = models.ForeignKey(
        DestinationPlace,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Pickup Location",
    )
    destination_city = models.ForeignKey(
        "order.City", on_delete=models.CASCADE, blank=True, null=True
    )

    destination_address = models.CharField(max_length=100, blank=True, null=True)

    PENDING_CHOICES = [
        ("As per guest request", "As per guest request"),
        ("Guest unreachable on phone", "Guest unreachable on phone"),
        ("Transiting", "Transiting"),
    ]
    pending_reason = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=PENDING_CHOICES,
        help_text="if status is pending",
    )

    link = models.CharField(
        max_length=1000,
        unique=True,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.link = f"https://auspic.geany.website/en//tracking/?tracking_id={self.tracking_id}"

        super().save(*args, **kwargs)

        def sms():
            print(self.mobile_number)
            print("this is ur tracking id")
            print(self.link)

        sms()

    def __str__(self):
        return f"{self.tracking_id} - {self.procedure}"


class AdditionalInfo(models.Model):
    tracking = models.ForeignKey(Tracking, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title



class GiftCard(models.Model):
    code = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        return self.is_active and (self.expires_at is None or self.expires_at > now())

    def __str__(self):
        return f"{self.code} - ₹{self.balance}"