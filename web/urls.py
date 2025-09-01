from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "web"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", TemplateView.as_view(template_name="web/about.html"), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    # policy
    path(
        "privacy-policy/",
        TemplateView.as_view(template_name="web/privacy_policy.html"),
        name="privacy_policy",
    ),
    path(
        "terms-conditions/",
        TemplateView.as_view(template_name="web/terms_conditions.html"),
        name="terms_conditions",
    ),
    path(
        "refund-policy/",
        TemplateView.as_view(template_name="web/refund_policy.html"),
        name="refund_policy",
    ),
    path(
        "shipping-policy/",
        TemplateView.as_view(template_name="web/shipping_policy.html"),
        name="shipping_policy",
    ),
    path(
        "contact-policy/",
        TemplateView.as_view(template_name="web/contact_policy.html"),
        name="contact_policy",
    ),
    # cart
    path("shop/cart/", views.cart_view, name="cart"),
    path("shop/cart/add/", views.cart_add, name="add_cart"),
    path("shop/cart/plus/", views.cart_plus, name="cart_plus"),
    path(
        "shop/cart-item-clear/<str:item_id>/",
        views.clear_cart_item,
        name="clear_cart_item",
    ),
    path("shop/cart-minus/", views.minus_to_cart, name="minus_to_cart"),
    path("shop/cart-clear/", views.clear_cart, name="clear_cart"),
    # shop
    path("shop/", views.ShopView.as_view(), name="shop"),
    path("shop/<slug:category_slug>/", views.ShopView.as_view(), name="shop_by_category"),

    path(
        "product-detail/<slug:slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
        path("apply-gift-card/", views.apply_gift_card, name="apply_gift_card"),

    # payment
    path("payment/<str:pk>/", views.PaymentView.as_view(), name="payment"),
    path("callback/<str:pk>/", views.callback, name="callback"),
    path(
        "complete-order/<str:pk>/",
        views.CompleteOrderView.as_view(),
        name="complete_order",
    ),
    path("tracking/", views.tracking, name="tracking"),
    path("tracking/<str:tracking_id>/", views.tracking, name="tracking_view"),
    path('remove_cart',views.cart_remove,name='remove_cart'),
    path("check-pincode/", views.check_pincode_ajax, name="check_pincode_ajax"),

        path(
        "test/",
        TemplateView.as_view(template_name="web/test.html"),
        name="test",
    ),
      path("order_list/<str:pk>/", views.OrderSummaryView.as_view(), name="order_list"),

]
