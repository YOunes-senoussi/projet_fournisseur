from django.urls import path
from . import views, more_functions

urlpatterns = [
    path("test_view/", views.test_view),

    path("store/", views.StoreView.as_view()),
    path("store/<int:store_id>/", views.StoreView.as_view()),

    path("client/", views.ClientView.as_view()),
    path("client/<int:client_id>/", views.ClientView.as_view()),

    path("group/", views.GroupView.as_view()),
    path("group/<int:group_id>/", views.GroupView.as_view()),

    path("product/", views.ProductView.as_view()),
    path("product/<int:product_id>/", views.ProductView.as_view()),
    
    path("category/", views.CategoryView.as_view()),
    path("category/<int:category_id>/", views.CategoryView.as_view()),

    path("packtype/", views.PackTypeView.as_view()),
    path("packtype/<int:packtype_id>/", views.PackTypeView.as_view()),

    path("coupon/", views.CouponView.as_view()),
    path("coupon/<int:coupon_id>/", views.CouponView.as_view()),

    path("couponcount/", views.CouponCountView.as_view()),
    path("couponcount/<int:couponcount_id>/", views.CouponCountView.as_view()),

    path("order/", views.OrderView.as_view()),
    path("order/<int:order_id>/", views.OrderView.as_view()),
    
    path("orderstate/", views.OrderStateView.as_view()),
    path("orderstate/<int:orderstate_id>/", views.OrderStateView.as_view()),
    
    path("ordercoupon/", views.OrderCouponView.as_view()),
    path("ordercoupon/<int:ordercoupon_id>/", views.OrderCouponView.as_view()),
    
    path("orderitem/", views.OrderItemView.as_view()),
    path("orderitem/<int:orderitem_id>/", views.OrderItemView.as_view()),
    
    path("cart/", views.CartView.as_view()),
    path("cart/<int:cart_id>/", views.CartView.as_view()),
    
    path("cartitem/", views.CartItemView.as_view()),
    path("cartitem/<int:cartitem_id>/", views.CartItemView.as_view()),
    
    path("notification/", views.NotificationView.as_view()),
    path("notification/<int:notification_id>/", views.NotificationView.as_view()),
    
    path("get_stores/", views.get_stores),
    path("get_client/", views.get_clients),
    path("get_groups/", views.get_groups),
    path("get_products/", views.get_products),
    path("get_categories/", views.get_categories),
    path("get_packtypes/", views.get_packtypes),
    path("get_coupons/", views.get_coupons),
    path("get_couponcounts/", views.get_couponcounts),
    path("get_orders/", views.get_orders),
    path("get_orderstates/", views.get_orderstates),
    path("get_ordercoupons/", views.get_ordercoupons),
    path("get_orderitems/", views.get_orderitems),
    path("get_carts/", views.get_carts),
    path("get_cartitems/", views.get_cartitems),
    path("get_notifications/", views.get_notifications),
    
    # path("check_coupons/", more_functions.check_coupons),
    # path("check_products/", more_functions.check_products),
    # path("create_order/", more_functions.create_order),
]
