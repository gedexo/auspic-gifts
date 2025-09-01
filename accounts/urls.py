from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("user/address/add/", views.AddAddress.as_view(), name="address_create"),
    path("user/address/get/", views.get_address_data, name="address_get"),
    path(
        "user/address/<int:pk>/edit/",
        views.customer_address_edit,
        name="address_update",
    ),
    path("user/address/<int:pk>/delete/", views.delete_address, name="address_delete"),
    path("user/address/", views.AddressListView.as_view(), name="address_list"),
    # order
    path("user/orders/", views.UserOrderListView.as_view(), name="orders"),
    path(
        "user/order/<str:order_id>/detail/",
        views.UserOrderDetailView.as_view(),
        name="order_detail",
    ),
    # setting
    path("user/setting/", views.SettingView.as_view(), name="setting"),

    path('user/register/', views.CustomRegistrationView.as_view(), name='registration_register'),
    
    path("", views.UserListView.as_view(), name="user_list"),
    path("user/<str:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("new/user/", views.UserCreateView.as_view(), name="user_create"),
    path("user/<str:pk>/update/", views.UserUpdateView.as_view(), name="user_update"),
    path("user/<str:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
]
