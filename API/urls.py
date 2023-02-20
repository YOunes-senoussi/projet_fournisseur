from django.urls import path
from . import views, more_functions

urlpatterns = [
    path("test_get/", views.test_view),

    path("coupon/", views.coupon_view),
    path("coupon/<int:coupon_id>/", views.coupon_view),

    path("ordercoupon/", views.ordercoupon_view),
    path("ordercoupon/<int:ordercoupon_id>/", views.ordercoupon_view),
    
    path("product/", views.product_view),
    path("product/<int:product_id>/", views.product_view),

    # path("check_coupons/", more_functions.check_coupons),
    # path("check_products/", more_functions.check_products),

    # path("create_order/", more_functions.create_order),
    # path("create_product/", retrieve_views.create_product),
]
