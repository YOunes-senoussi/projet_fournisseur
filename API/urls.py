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

# Query Params: (all are optional)
#   
#   single value:
#       1) order_by:(str) name of field to sort the list by
#       
#       2) offset: (int) nbr of elements to ignore in the beginning
# 
#       3) limit: (int) max nbr of elements to return
#   
#   multiple values:
#       values: (str) fields to include when returning, 
#           ex: (table: Product):
#               "values=id & values=name & values=store__store_name"
#                   ===> {
#                	        "id": 1,
#                	        "name": "Beets",
#                	        "store__store_name": "Photobean"
#                         }
# 
#       annotations: (str) apply some calculation function on some field of every item in the list
#                   
#           ex: (table: Store):
#               "values=id & values=store_name & annotations=count, product__id, nbr_product"
#                   ===> {
#                	        "id": 1,
#                	        "store_name": "Photobean",
#                           "nbr_product": 5,
#                         }
# 
#       filters: (str) every other param is considered a filter,
#           ex: (table: Product):
#               "id__lt=10 & category__id=1 & values=id & values=name & values category__name"
#               
#                 {
#                     "products": [
#                         {
#                             "id": 3,
#                             "name": "Cup - 4oz Translucent",
#                             "category__name": "category_1"
#                         },
#                         {
#                             "id": 4,
#                             "name": "Sauce - Vodka Blush",
#                             "category__name": "category_1"
#                         }
#                     ]
#                 }
#           
#                   ==> get products that their id is less than 10 & their category id is 1
#                       and return only id, name, and category__name
