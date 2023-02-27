from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from API.models import *
from API.more_functions import extract_params

import json

# ##################### Store Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def store_view(request: Request, store_id: int = None):

    if (request.method == "GET"):
        return get_store(request=request, store_id=store_id)

    return Response("Nothing")


def get_store(request: Request, store_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if store_id is not None:
        stores = Store.objects.filter(pk=store_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"store": stores.first(), **stores.aggregate(**aggregations)})
        
        return Response({"store": stores.first()})

    stores = (
        Store.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    stores = stores[offset: offset + limit]

    if aggregations:
        return Response({"stores": stores, **stores.aggregate(**aggregations)})
    
    return Response({"stores": stores})

# ##################### Client Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def client_view(request: Request, client_id: int = None):

    if (request.method == "GET"):
        return get_client(request=request, client_id=client_id)

    return Response("Nothing")


def get_client(request: Request, client_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if client_id is not None:
        clients = Client.objects.filter(pk=client_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"client": clients.first(), **clients.aggregate(**aggregations)})
        
        return Response({"client": clients.first()})

    clients = (
        Client.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    clients = clients[offset: offset + limit]

    if aggregations:
        return Response({"clients": clients, **clients.aggregate(**aggregations)})
    
    return Response({"clients": clients})

# ##################### Product Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def product_view(request: Request, product_id: int = None):

    if (request.method == "GET"):
        return get_product(request=request, product_id=product_id)

    return Response("Nothing")


def get_product(request: Request, product_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if product_id is not None:
        products = Product.objects.filter(pk=product_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"product": products.first(), **products.aggregate(**aggregations)})
        
        return Response({"product": products.first()})

    products = (
        Product.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    products = products[offset: offset + limit]

    if aggregations:
        return Response({"products": products, **products.aggregate(**aggregations)})
    
    return Response({"products": products})

# ##################### Coupon Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def coupon_view(request: Request, coupon_id: int = None):

    if (request.method == "GET"):
        return get_coupon(request=request, coupon_id=coupon_id)

    return Response("Nothing")


def get_coupon(request: Request, coupon_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if coupon_id is not None:
        coupons = Coupon.objects.filter(pk=coupon_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"coupon": coupons.first(), **coupons.aggregate(**aggregations)})
        
        return Response({"coupon": coupons.first()})

    coupons = (
        Coupon.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    coupons = coupons[offset: offset + limit]

    if aggregations:
        return Response({"coupons": coupons, **coupons.aggregate(**aggregations)})
    
    return Response({"coupons": coupons})

# ##################### Order View
@api_view(["GET", "POST", "PUT", "DELETE"])
def order_view(request: Request, order_id: int = None):

    if (request.method == "GET"):
        return get_order(request=request, order_id=order_id)

    return Response("Nothing")


def get_order(request: Request, order_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if order_id is not None:
        orders = Order.objects.filter(pk=order_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"order": orders.first(), **orders.aggregate(**aggregations)})
        
        return Response({"order": orders.first()})

    orders = (
        Order.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    orders = orders[offset: offset + limit]

    if aggregations:
        return Response({"orders": orders, **orders.aggregate(**aggregations)})
    
    return Response({"orders": orders})

# ##################### OrderCoupon View
@api_view(["GET", "POST", "PUT", "DELETE"])
def ordercoupon_view(request: Request, ordercoupon_id: int = None):

    if (request.method == "GET"):
        return get_ordercoupon(request=request, ordercoupon_id=ordercoupon_id)
        # return get_entries(request=request, entry_id=ordercoupon_id, model_name="OrderCoupon")

    return Response("Nothing")


def get_ordercoupon(request: Request, ordercoupon_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if ordercoupon_id is not None:
        ordercoupons = OrderCoupon.objects.filter(pk=ordercoupon_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"ordercoupon": ordercoupons.first(), **ordercoupons.aggregate(**aggregations)})
        
        return Response({"ordercoupon": ordercoupons.first()})

    ordercoupons = (
        OrderCoupon.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    ordercoupons = ordercoupons[offset: offset + limit]

    if aggregations:
        return Response({"ordercoupons": ordercoupons, **ordercoupons.aggregate(**aggregations)})
    
    return Response({"ordercoupons": ordercoupons})

# ##################### OrderItem View
@api_view(["GET", "POST", "PUT", "DELETE"])
def orderitem_view(request: Request, orderitem_id: int = None):

    if (request.method == "GET"):
        return get_orderitem(request=request, orderitem_id=orderitem_id)

    return Response("Nothing")


def get_orderitem(request: Request, orderitem_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if orderitem_id is not None:
        orderitems = OrderItem.objects.filter(pk=orderitem_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"orderitem": orderitems.first(), **orderitems.aggregate(**aggregations)})
        
        return Response({"orderitem": orderitems.first()})

    orderitems = (
        OrderItem.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    orderitems = orderitems[offset: offset + limit]

    if aggregations:
        return Response({"orderitems": orderitems, **orderitems.aggregate(**aggregations)})
    
    return Response({"orderitems": orderitems})

# ##################### Group Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def group_view(request: Request, group_id: int = None):

    if (request.method == "GET"):
        return get_group(request=request, group_id=group_id)

    return Response("Nothing")


def get_group(request: Request, group_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if group_id is not None:
        groups = Group.objects.filter(pk=group_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"group": groups.first(), **groups.aggregate(**aggregations)})
        
        return Response({"group": groups.first()})

    groups = (
        Group.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    groups = groups[offset: offset + limit]

    if aggregations:
        return Response({"groups": groups, **groups.aggregate(**aggregations)})
    
    return Response({"groups": groups})

# ##################### Category Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def category_view(request: Request, category_id: int = None):

    if (request.method == "GET"):
        return get_category(request=request, category_id=category_id)

    return Response("Nothing")


def get_category(request: Request, category_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if category_id is not None:
        categorys = Category.objects.filter(pk=category_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"category": categorys.first(), **categorys.aggregate(**aggregations)})
        
        return Response({"category": categorys.first()})

    categorys = (
        Category.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    categorys = categorys[offset: offset + limit]

    if aggregations:
        return Response({"categorys": categorys, **categorys.aggregate(**aggregations)})
    
    return Response({"categorys": categorys})

# ##################### PackType Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def packtype_view(request: Request, packtype_id: int = None):

    if (request.method == "GET"):
        return get_packtype(request=request, packtype_id=packtype_id)

    return Response("Nothing")


def get_packtype(request: Request, packtype_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if packtype_id is not None:
        packtypes = PackType.objects.filter(pk=packtype_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"packtype": packtypes.first(), **packtypes.aggregate(**aggregations)})
        
        return Response({"packtype": packtypes.first()})

    packtypes = (
        PackType.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    packtypes = packtypes[offset: offset + limit]

    if aggregations:
        return Response({"packtypes": packtypes, **packtypes.aggregate(**aggregations)})
    
    return Response({"packtypes": packtypes})

# ##################### CouponCount Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def couponcount_view(request: Request, couponcount_id: int = None):

    if (request.method == "GET"):
        return get_couponcount(request=request, couponcount_id=couponcount_id)

    return Response("Nothing")


def get_couponcount(request: Request, couponcount_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if couponcount_id is not None:
        couponcounts = CouponCount.objects.filter(pk=couponcount_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"couponcount": couponcounts.first(), **couponcounts.aggregate(**aggregations)})
        
        return Response({"couponcount": couponcounts.first()})

    couponcounts = (
        CouponCount.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    couponcounts = couponcounts[offset: offset + limit]

    if aggregations:
        return Response({"couponcounts": couponcounts, **couponcounts.aggregate(**aggregations)})
    
    return Response({"couponcounts": couponcounts})

# ##################### OrderState Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def orderstate_view(request: Request, orderstate_id: int = None):

    if (request.method == "GET"):
        return get_orderstate(request=request, orderstate_id=orderstate_id)

    return Response("Nothing")


def get_orderstate(request: Request, orderstate_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if orderstate_id is not None:
        orderstates = OrderState.objects.filter(pk=orderstate_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"orderstate": orderstates.first(), **orderstates.aggregate(**aggregations)})
        
        return Response({"orderstate": orderstates.first()})

    orderstates = (
        OrderState.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    orderstates = orderstates[offset: offset + limit]

    if aggregations:
        return Response({"orderstates": orderstates, **orderstates.aggregate(**aggregations)})
    
    return Response({"orderstates": orderstates})

# ##################### Cart Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def cart_view(request: Request, cart_id: int = None):

    if (request.method == "GET"):
        return get_cart(request=request, cart_id=cart_id)

    return Response("Nothing")


def get_cart(request: Request, cart_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if cart_id is not None:
        carts = Cart.objects.filter(pk=cart_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"cart": carts.first(), **carts.aggregate(**aggregations)})
        
        return Response({"cart": carts.first()})

    carts = (
        Cart.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    carts = carts[offset: offset + limit]

    if aggregations:
        return Response({"carts": carts, **carts.aggregate(**aggregations)})
    
    return Response({"carts": carts})

# ##################### CartItem Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def cartitem_view(request: Request, cartitem_id: int = None):

    if (request.method == "GET"):
        return get_cartitem(request=request, cartitem_id=cartitem_id)

    return Response("Nothing")


def get_cartitem(request: Request, cartitem_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if cartitem_id is not None:
        cartitems = CartItem.objects.filter(pk=cartitem_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"cartitem": cartitems.first(), **cartitems.aggregate(**aggregations)})
        
        return Response({"cartitem": cartitems.first()})

    cartitems = (
        CartItem.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    cartitems = cartitems[offset: offset + limit]

    if aggregations:
        return Response({"cartitems": cartitems, **cartitems.aggregate(**aggregations)})
    
    return Response({"cartitems": cartitems})

# ##################### Notification Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def notification_view(request: Request, notification_id: int = None):

    if (request.method == "GET"):
        return get_notification(request=request, notification_id=notification_id)

    return Response("Nothing")


def get_notification(request: Request, notification_id: int = None):

    order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

    if notification_id is not None:
        notifications = OrderNotification.objects.filter(pk=notification_id).values(*values).annotate(**annotations)

        if aggregations:
            return Response({"notification": notifications.first(), **notifications.aggregate(**aggregations)})
        
        return Response({"notification": notifications.first()})

    notifications = (
        OrderNotification.objects
            .filter(**filters).distinct()
            .values(*values).annotate(**annotations)
            .order_by(order_by)
    )
    notifications = notifications[offset: offset + limit]

    if aggregations:
        return Response({"notifications": notifications, **notifications.aggregate(**aggregations)})
    
    return Response({"notifications": notifications})

# ################ Test
@api_view(["GET", "POST", "PUT", "DELETE"])
def test_view(request: Request):

    print("-"*100)
    print(f"{request.query_params=}")
    # print(f"{request.data=}")
    # print("-"*100)
    # param = request.query_params.get("json")
    # param = json.loads(param)
    # print(json.dumps(param, indent=0))
    # print("-"*100)
    # print(request.query_params.getlist("filter"))
    # print(dict(list(map(lambda el: el.split("="), request.query_params.getlist("filter")))))
    # print("-"*100)

    return Response("nothing")

# ##################### Generic GET View (not used yet)
def get_entries(request: Request, entry_id: int = None, model_name: str = None):

    model_name = model_name.lower()

    if model_name not in tables:
        return Response("wrong table")

    model = tables.get(model_name)

    order_by, offset, limit, filter_fields, values, annotations, aggregations = extract_params(
        request)

    if entry_id is not None:
        return Response(
            {
                model_name: model.objects.filter(pk=entry_id)
                .values(*values).annotate(**annotations).first()
            }
        )

    entries = model.objects.filter(**filter_fields).distinct()
    if order_by is not None:
        entries = entries.order_by(order_by)

    entries = entries[offset: offset + limit]
    entries = entries.values(*values).annotate(**annotations)

    return Response({f"{model_name}s": entries})


# ################ Models
tables = {
    "store": Store,
    "client": Client,
    "product": Product,
    "coupon": Coupon,
    "order": Order,
    "ordercoupon": OrderCoupon,
    "orderitem": OrderItem,
    "group": Group,
    "category": Category,
    "packtype": PackType,
}
