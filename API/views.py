from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from API.models import *
from API.more_functions import extract_params, annotate_funcs

# ##################### Store Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def store_view(request: Request, store_id: int = None):

    if(request.method == "GET"):
        return get_store(request=request, store_id=store_id)

    return Response("Nothing")

def get_store(request: Request, store_id: int = None):

    order_by, offset, limit, filter_fields, values, annotations = extract_params(request)

    if store_id is not None:
        return Response({"store": Store.objects.filter(pk=store_id).values(*values).first()})

    stores = Store.objects.filter(**filter_fields).distinct().values(*values)
    if order_by is not None:
        stores = stores.order_by(order_by)

    stores = stores[offset: offset + limit]

    return Response({"stores": stores})

# ##################### Client Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def client_view(request: Request, client_id: int = None):

    if(request.method == "GET"):
        return get_client(request=request, client_id=client_id)

    return Response("Nothing")

def get_client(request: Request, client_id: int = None):

    order_by, offset, limit, filter_fields, values, annotations = extract_params(request)

    if client_id is not None:
        return Response({"client": Client.objects.filter(pk=client_id).values(*values).first()})

    clients = Client.objects.filter(**filter_fields).distinct().values(*values)
    if order_by is not None:
        clients = clients.order_by(order_by)

    clients = clients[offset: offset + limit]

    return Response({"clients": clients})

# ##################### Product Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def product_view(request: Request, product_id: int = None):

    if(request.method == "GET"):
        return get_product(request=request, product_id=product_id)

    return Response("Nothing")

def get_product(request: Request, product_id: int = None):

    order_by, offset, limit, filter_fields, values, annotations = extract_params(request)

    if product_id is not None:
        return Response({"product": Product.objects.filter(pk=product_id).values(*values).first()})

    products = Product.objects.filter(**filter_fields).distinct().values(*values)
    if order_by is not None:
        products = products.order_by(order_by)

    products = products[offset: offset + limit]

    return Response({"products": products})

# ##################### Coupon Views
@api_view(["GET", "POST", "PUT", "DELETE"])
def coupon_view(request: Request, coupon_id: int = None):

    if(request.method == "GET"):
        # return get_coupon(request=request, coupon_id=coupon_id)
        return get_entries(request=request, entry_id=coupon_id, model_name="Coupon")

    return Response("Nothing")

def get_coupon(request: Request, coupon_id: int = None):

    order_by, offset, limit, filter_fields, values, annotations = extract_params(request)

    if coupon_id is not None:
        return Response(
            {
                "coupon": Coupon.objects.filter(pk=coupon_id)
                    .values(*values).annotate(**annotations).first()
            }
        )

    coupons = Coupon.objects.filter(**filter_fields).distinct()
    if order_by is not None:
        coupons = coupons.order_by(order_by)

    coupons = coupons[offset: offset + limit]
    coupons = coupons.values(*values).annotate(**annotations)

    return Response({"coupons": coupons})

# ##################### Order Coupon View
@api_view(["GET", "POST", "PUT", "DELETE"])
def ordercoupon_view(request: Request, ordercoupon_id: int = None):

    if(request.method == "GET"):
        # return get_ordercoupon(request=request, ordercoupon_id=ordercoupon_id)
        return get_entries(request=request, entry_id=ordercoupon_id, model_name="OrderCoupon")

    return Response("Nothing")

def get_ordercoupon(request: Request, ordercoupon_id: int = None):

    order_by, offset, limit, filter_fields, values, annotations = extract_params(request)

    if ordercoupon_id is not None:
        return Response(
            { 
                "ordercoupon": OrderCoupon.objects.filter(pk=ordercoupon_id)
                    .values(*values).annotate(**annotations).first()
            }
        )

    ordercoupons = OrderCoupon.objects.filter(**filter_fields).distinct()
    if order_by is not None:
        ordercoupons = ordercoupons.order_by(order_by)

    ordercoupons = ordercoupons[offset: offset + limit]

    ordercoupons = ordercoupons.values(*values).annotate(**annotations)

    return Response({"ordercoupons": ordercoupons})

# ################ Test
@api_view(["GET", "POST", "PUT", "DELETE"])
def test_view(request: Request):

    print("-"*100)
    print(f"{request.query_params=}")
    print(f"{request.data=}")

    print("-"*100)
    print(request.query_params.get("value", default="default"))
    print(request.query_params.getlist("values"))

    print("-"*100)

    return Response("nothing")

# ##################### Views
def get_entries(request: Request, entry_id: int = None, model_name: str = None):

    model_name = model_name.lower()

    if model_name not in tables:
        return Response("wrong table")

    model = tables.get(model_name)

    order_by, offset, limit, filter_fields, values, annotations = extract_params(request)

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
