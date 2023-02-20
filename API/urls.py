from django.urls import path
from . import views, more_functions

urlpatterns = [
    path("test_view/", views.test_view),

    path("store/", views.store_view),
    path("store/<int:store_id>/", views.store_view),

    path("client/", views.client_view),
    path("client/<int:client_id>/", views.client_view),

    path("product/", views.product_view),
    path("product/<int:product_id>/", views.product_view),

    path("coupon/", views.coupon_view),
    path("coupon/<int:coupon_id>/", views.coupon_view),

    path("order/", views.order_view),
    path("order/<int:order_id>/", views.order_view),
    
    path("ordercoupon/", views.ordercoupon_view),
    path("ordercoupon/<int:ordercoupon_id>/", views.ordercoupon_view),
    
    path("orderitem/", views.orderitem_view),
    path("orderitem/<int:orderitem_id>/", views.orderitem_view),
    
    path("group/", views.group_view),
    path("group/<int:group_id>/", views.group_view),
    
    path("category/", views.category_view),
    path("category/<int:category_id>/", views.category_view),
    
    path("packtype/", views.packtype_view),
    path("packtype/<int:packtype_id>/", views.packtype_view),
    
    # path("check_coupons/", more_functions.check_coupons),
    # path("check_products/", more_functions.check_products),
    # path("create_order/", more_functions.create_order),
]
