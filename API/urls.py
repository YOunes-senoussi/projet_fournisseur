from django.urls import path
from . import views, more_functions

urlpatterns = [
    path("test_view/", views.test_view),

    path("secure_view/", views.secure_view),
    path("get_all_client_credentials/", views.get_all_client_credentials),
    path("get_all_store_credentials/", views.get_all_store_credentials),

    path("client_log_in/", views.client_log_in),
    path("store_log_in/", views.store_log_in),

    path("check_coupon/", more_functions.check_coupon),
    path("create_order/", more_functions.create_order),
    path("delete_order/", more_functions.delete_order),
    path("update_order_state/<int:order_id>/", more_functions.update_order_state),

    path("store_fav_clients/<int:store_id>/", views.StoreFavClientsView.as_view()),
    path("client_fav_stores/<int:client_id>/", views.ClientFavStoresView.as_view()),
    path("group_clients/<int:group_id>/", views.GroupClientsView.as_view()),

    # path("order_coupons/<int:order_id>/", views.OrderCouponsView.as_view()),
    # path("order_products/<int:order_id>/", views.OrderProductsView.as_view()),
    # path("client_products/<int:client_id>/", views.ClientProductsView.as_view()),
    # path("coupon_clients/<int:coupon_id>/", views.CouponClientsView.as_view()),
    # path("coupon_clients/<int:coupon_id>/<int:client_id>/", views.CouponClientsView.as_view()),

    path("get_<str:model_name>/", views.GetView.as_view()),
    path("get_<str:model_name>/<int:item_id>/", views.GetView.as_view()),
    path("create_<str:model_name>/", views.create_item),
    path("update_<str:model_name>/<int:item_id>/", views.update_item),
    path("delete_<str:model_name>/<int:item_id>/", views.delete_item),
]
