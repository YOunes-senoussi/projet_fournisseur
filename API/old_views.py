from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.db.models import Case

from API.models import *

# ################ some variables
COUPON_FOUND = 0
PRODUCT_FOUND = 1

STORE_NOT_FOUND = -1
CLIENT_NOT_FOUND = -2

COUPON_NOT_FOUND = -3
COUPON_NOT_ACTIVE = -5
COUPON_USAGE_LIMIT = -7
COUPON_WRONG_STORE = -9

PRODUCT_NOT_FOUND = -2
PRODUCT_WRONG_STORE = -4
PRODUCT_NOT_AVAILABLE = -6
PRODUCT_WRONG_PRICE = -8

# ##################### Check Function
def check_coupon(c_string: str, store_id: int, client_id: int):

    coupon = Coupon.objects.filter(string=c_string).first()

    if not coupon:
        return {
            "status": "fail",
            "string": c_string,
            "code": COUPON_NOT_FOUND,
            "code_text": "COUPON_NOT_FOUND",
        }
    
    if coupon.store_id != store_id:
        return {
            "status": "fail",
            "string": c_string,
            "code": PRODUCT_WRONG_STORE,
            "code_text": "WRONG_STORE",
        }

    if not coupon.is_active:
        return {
            "status": "fail",
            "string": c_string,
            "code": COUPON_NOT_ACTIVE,
            "code_text": "COUPON_NOT_ACTIVE",
        }
    
    # this doesn't work anymore
    if coupon.ordercoupons.filter(order__client__id=client_id).count() >= coupon.max_nbr_uses:
        return {
            "status": "fail",
            "string": c_string,
            "code": COUPON_USAGE_LIMIT,
            "code_text": "COUPON_USAGE_LIMIT",
        }
    
    return {
        "status": "success",
        "string": c_string,
        "code": COUPON_FOUND,
        "code_text": "COUPON_FOUND",
        **Coupon.objects.filter(pk=coupon.id).values().first()
    }

@api_view(["POST"])
def check_coupons(request: Request):

    coupons = request.data["coupons"]
    store_id = request.data["store_id"]
    client_id = request.data["client_id"]

    if not Client.objects.filter(pk=client_id).first():
        return Response(
            {
                "status": "fail",
                "code": CLIENT_NOT_FOUND,
                "code_text": "CLIENT_NOT_FOUND",
                "coupons": [],
            }
        )
    
    if not Store.objects.filter(pk=store_id).first():
        return Response(
            {
                "status": "fail",
                "code": STORE_NOT_FOUND,
                "code_text": "STORE_NOT_FOUND",
                "coupons": [],
            }
        )
    
    coupons = [check_coupon(c_string=coupon, store_id=store_id, client_id=client_id) for coupon in coupons]

    return Response(
        {
            "status": "fail" if any(map(lambda c:c["status"]=="fail", coupons)) else "success",
            "coupons": coupons
        }
    )

# ########
def check_product(product_id: int, quantity: int, store_id: int):

    product = Product.objects.filter(pk=product_id).first()

    if not product:
        return {
            "status": "fail",
            "id": product_id,
            "code": PRODUCT_NOT_FOUND,
            "code_text": "PRODUCT_NOT_FOUND",
        }
    
    if product.store_id != store_id:
        return {
            "status": "fail",
            "id": product_id,
            "code": PRODUCT_WRONG_STORE,
            "code_text": "WRONG_STORE",
        }

    if product.is_available is False:
        return {
            "status": "fail",
            "id": product_id,
            "code": PRODUCT_NOT_AVAILABLE,
            "code_text": "PRODUCT_NOT_AVAILABLE",
        }
    
    return {
        "status": "success",
        "id": product_id,
        "quantity": quantity,
        "code": PRODUCT_FOUND,
        "code_text": "PRODUCT_FOUND",
        **Product.objects.filter(pk=product.id).values().annotate(
            category_name=Case(default="category__name")
        ).first()
    }

@api_view(["POST"])
def check_products(request: Request):

    products = request.data["products"]
    store_id = request.data["store_id"]

    if not Store.objects.filter(pk=store_id).first():
        return Response(
            {
                "status": "fail",
                "code": STORE_NOT_FOUND,
                "code_text": "STORE_NOT_FOUND",
                "products": [],
            }
        )

    products = [check_product(product_id=p["id"], store_id=store_id) for p in products]

    return Response(
        {
            "status": "fail" if any(map(lambda p:p["status"]=="fail", products)) else "success",
            "products": products
        }
    )

# #####################
@api_view(["POST"])
def create_order(request: Request):

    store_id = request.data["store_id"]
    client_id = request.data["client_id"]
    products = request.data["products"]
    coupons = request.data["coupons"]

    if not Client.objects.filter(pk=client_id).exists():
        return Response(
            {
                "status": "fail",
                "code": CLIENT_NOT_FOUND,
                "code_text": "CLIENT_NOT_FOUND",
                "coupons": [],
                "products": [],
            }
        )

    if not Store.objects.filter(pk=store_id).exists():
        return Response(
            {
                "status": "fail",
                "code": STORE_NOT_FOUND,
                "code_text": "STORE_NOT_FOUND",
                "coupons": [],
                "products": [],
            }
        )
    
    coupons = [
        check_coupon(c_string=coupon, store_id=store_id, client_id=client_id) 
        for coupon in coupons
    ]

    products = [
        check_product(product_id=p["id"], quantity=p["quantity"], store_id=store_id) 
        for p in products
    ]

    if (any(map(lambda c:c["status"]=="fail", coupons)) or 
        any(map(lambda p:p["status"]=="fail", products))):

        return Response(
            {
                "status": "fail",
                "products": products,
                "coupons": coupons,
            }
        )
    
    for coupon in coupons:
        if coupon["coupon_type"] == "All":

            for product in products:
                product["discount"] += coupon["discount"]

        elif coupon["coupon_type"] == "Category":

            for product in list(filter(lambda p:p["category_id"]==coupon["target_id"], products)):
                product["discount"] += coupon["discount"]

        elif coupon["coupon_type"] == "Product":

            for product in list(filter(lambda p:p["id"]==coupon["target_id"], products)):
                product["discount"] += coupon["discount"]

    total_price = 0
    for product in products:
        product["new_price"] = round(
            (product["price"] * (1 - (product["discount"]/100))) * product["quantity"], 2
        )
        total_price += product["price"]

    new_ordre = Order.objects.create(
        store_id = store_id,
        client_id = client_id,
        total_price = round(total_price, 2),
    )

    for product in products:
        OrderProduct.objects.create(
            order_id=new_ordre.id,
            product_id=product["id"],

            discount=product["discount"],
            quantity=product["quantity"],
            original_price=product["price"],
            new_price=product["new_price"],
        )

    for coupon in coupons:
        OrderCoupon.objects.create(
            coupon_id=coupon["id"],
            order_id=new_ordre.id,
        )

    return Response(
        {
            "status": "success",
            "products": products,
            "coupons": coupons,
            "total_price": total_price,
        }
    )

