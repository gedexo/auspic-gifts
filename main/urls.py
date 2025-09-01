from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("dashboard/", views.IndexView.as_view(), name="index"),
    path("orders/", views.OrderView.as_view(), name="orders"),
    path(
        "order/<str:order_id>/detail/",
        views.OrderDetailView.as_view(),
        name="order_detail",
    ),
    path("order/update/", views.OrderUpdateView.as_view(), name="order_update"),
    # catgory
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path(
        "category/create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "category/<str:pk>/update/",
        views.CategoryUpdate.as_view(),
        name="category_update",
    ),
    path(
        "category/<str:pk>/delete/",
        views.CategoryDelete.as_view(),
        name="category_delete",
    ),
    # subcatgory
    path("subcategories/", views.SubCategoryListView.as_view(), name="subcategories"),
    path(
        "subcategory/create/",
        views.SubCategoryCreateView.as_view(),
        name="subcategory_create",
    ),
    path(
        "subcategory/<str:pk>/update/",
        views.SubCategoryUpdate.as_view(),
        name="subcategory_update",
    ),
    path(
        "subcategory/<str:pk>/delete/",
        views.SubCategoryDelete.as_view(),
        name="subcategory_delete",
    ),
    # tag
    path("tags/", views.TagListView.as_view(), name="tags"),
    path("tag/create/", views.TagCreateView.as_view(), name="tag_create"),
    path("tag/<str:pk>/update/", views.TagUpdateView.as_view(), name="tag_update"),
    path("tag/<str:pk>/delete/", views.TagDeleteView.as_view(), name="tag_delete"),
    # brand
    path("brands/", views.BrandListView.as_view(), name="brands"),
    path("brand/create/", views.BrandCreateView.as_view(), name="brand_create"),
    path(
        "brand/<str:pk>/update/", views.BrandUpdateView.as_view(), name="brand_update"
    ),
    path(
        "brand/<str:pk>/delete/", views.BrandDeleteView.as_view(), name="brand_delete"
    ),
    # fearture
    path("features/", views.FeatureListView.as_view(), name="features"),
    path("feature/create/", views.FeatureCreateView.as_view(), name="feature_create"),
    path(
        "feature/<str:pk>/update/",
        views.FeatureUpdateView.as_view(),
        name="feature_update",
    ),
    path(
        "feature/<str:pk>/delete/",
        views.FeatureDeleteView.as_view(),
        name="feature_delete",
    ),
    # product
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("product/create/", views.CreateProductView.as_view(), name="product_create"),
    path("product/<pk>/edit/", views.ProductUpdate.as_view(), name="product_update"),
    path(
        "product/<str:pk>/delete/", views.ProductDelete.as_view(), name="product_delete"
    ),
    # variant
    path("variants/", views.VariantListView.as_view(), name="variants"),
    path("variant/create/", views.VariantCreateView.as_view(), name="variant_create"),
    path(
         "variant/<str:pk>/update/",
          views.VariantUpdateView.as_view(),
         name="variant_update",
    ),
    path(
        "variant/<str:pk>/delete/",
        views.VarianteDeleteView.as_view(),
        name="variant_delete",
    ),
    # reviews
    path("reviews/", views.ReviewListView.as_view(), name="review_list"),
    path("review/create/", views.ReviewCreateView.as_view(), name="review_create"),
    path("review/<pk>/edit/", views.ReviewUpdateView.as_view(), name="review_update"),
    path(
        "review/<str:pk>/delete/",
        views.ReviewDeleteView.as_view(),
        name="review_delete",
    ),
    # Purchase
    path("purchases/", views.PurchaseListView.as_view(), name="purchase_list"),
    path(
        "purchase/create/", views.PurchaseCreateView.as_view(), name="purchase_create"
    ),
    path(
        "purchase/<str:pk>/update/",
        views.PurchaseUpdateView.as_view(),
        name="purchase_update",
    ),
    path(
        "purchase/<str:pk>/delete/",
        views.PurchaseDeleteView.as_view(),
        name="purchase_delete",
    ),
    # state
    path("states/", views.StateListView.as_view(), name="states"),
    path("state/create/", views.StateCreateView.as_view(), name="state_create"),
    path(
        "state/<str:pk>/update/", views.StateUpdateView.as_view(), name="state_update"
    ),
    path(
        "state/<str:pk>/delete/", views.StateDeleteView.as_view(), name="state_delete"
    ),
    # district
    path("districts/", views.DistrictListView.as_view(), name="districts"),
    path(
        "district/create/", views.DistrictCreateView.as_view(), name="district_create"
    ),
    path(
        "district/<str:pk>/update/",
        views.DistrictUpdateView.as_view(),
        name="district_update",
    ),
    path(
        "district/<str:pk>/delete/",
        views.DistrictDeleteView.as_view(),
        name="district_delete",
    ),
    # Banner
    path("banners/", views.BannerListView.as_view(), name="banners"),
    path("banner/create/", views.BannerCreateView.as_view(), name="banner_create"),
    path(
        "banner/<str:pk>/update/",
        views.BannerUpdateView.as_view(),
        name="banner_update",
    ),
    path(
        "banner/<str:pk>/delete/",
        views.BannerDeleteView.as_view(),
        name="banner_delete",
    ),
    # customer
    path("customers/", views.CustomerListView.as_view(), name="customers"),
    # Category List
    path("categorylist/", views.CategoryListListView.as_view(), name="categorylists"),
    path(
        "categorylist/create/",
        views.CategoryListCreateView.as_view(),
        name="categorylist_create",
    ),
    path(
        "categorylist/<str:pk>/update/",
        views.CategoryListUpdateView.as_view(),
        name="categorylist_update",
    ),
    path(
        "categorylist/<str:pk>/delete/",
        views.CategoryListDeleteView.as_view(),
        name="categorylist_delete",
    ),
    # Gift Card
    path("giftcards/", views.GiftCardListView.as_view(), name="giftcards"),
    path("giftcard/create/", views.GiftCardCreateView.as_view(), name="giftcard_create"),
    path(
        "giftcard/<str:pk>/update/",
        views.GiftCardUpdateView.as_view(),
        name="giftcard_update",
    ),
    path(
        "giftcard/<str:pk>/delete/",
        views.GiftCardDeleteView.as_view(),
        name="giftcard_delete",
    ),

    path("cities/", views.CityListView.as_view(), name="cities"),
    path("city/create/", views.CityCreateView.as_view(), name="city_create"),
    path("city/<int:pk>/update/", views.CityUpdateView.as_view(), name="city_update"),
    path("city/<int:pk>/delete/", views.CityDeleteView.as_view(), name="city_delete"),

    # Pincode URLs
    path("pincodes/", views.PincodeListView.as_view(), name="pincodes"),
    path("pincode/create/", views.PincodeCreateView.as_view(), name="pincode_create"),
    path("pincode/<int:pk>/update/", views.PincodeUpdateView.as_view(), name="pincode_update"),
    path("pincode/<int:pk>/delete/", views.PincodeDeleteView.as_view(), name="pincode_delete"),
]
