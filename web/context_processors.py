from django.conf import settings
from decimal import Decimal
from order.models import Wishlist
from products.models import Brand, Category,ProductVariant
from django.shortcuts import get_object_or_404
from .cart import Cart
from django.contrib.auth import get_user_model
User=get_user_model()

def main_context(request):
    all_categories = Category.objects.filter(parent__isnull=True, is_active=True).order_by('order')
    all_brands = Brand.objects.filter(is_active=True)

    cart_count = 0
    wishlist_count = 0
    current_user = None

    cart_instance = Cart(request)
    cart = cart_instance.cart
    cart_count = len(cart)

    cart_items = []
    cart_total = Decimal(0)

    # Calculate cart items and total
    for item_id, item_data in cart.items():
        variant = get_object_or_404(ProductVariant, id=item_id)
        quantity = item_data["quantity"]
        total_price = Decimal(item_data["selling_price"]) * quantity
        cart_items.append(
            {
                "product": variant,
                "quantity": quantity,
                "total_price": total_price,
            }
        )
        cart_total += total_price

    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return {
        "all_categories": all_categories,
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
        "current_user": current_user,
        "all_brands": all_brands,
        "RAZOR_PAY_KEY": settings.RAZOR_PAY_KEY,
        "RAZOR_PAY_SECRET": settings.RAZOR_PAY_SECRET,
        "cart_items": cart_items,
    }
