from functools import reduce
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.db.models import F, Case, Value, When, Q, Avg, Max, Min, Count, Sum
from django.db.models.query import QuerySet
import base64, io, pathlib
from PIL import Image

from API.models import *
# ################ 
calcul_classes = {
    "avg": Avg,
    "max": Max,
    "min": Min,
    "count": Count,
    "sum": Sum,
    "value": Value,
    "append": F,
}
# ################ 

# Create your views here.
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

    if not Client.objects.filter(pk=client_id).first():
        return Response(
            {
                "status": "fail",
                "code": CLIENT_NOT_FOUND,
                "code_text": "CLIENT_NOT_FOUND",
                "coupons": [],
                "products": [],
            }
        )

    if not Store.objects.filter(pk=store_id).first():
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
        OrderItem.objects.create(
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

# #####################
def extract_params(request: Request):

    params = request.query_params
    values = params.getlist("value", [])

    annotations = get_annotations(params.getlist("annotate", []))
    aggregations = get_annotations(params.getlist("aggregate", []))

    filters = dict(list(map(
        lambda el:(el.split(":")[0], eval(f'"{el.split(":")[1]}"')
                   ), params.getlist("filter", []))))

    order_by = params.get("order_by", "pk")
    offset = int(params.get("offset", 0))
    limit = int(params.get("limit", 1_000_000))

    return order_by, offset, limit, filters, values, annotations, aggregations

def get_annotations(annot_list: list):

    annotations = {}
    for an in annot_list:
        
        split = an.lower().split(",")

        if len(split) == 3:
            class_name, field, field_name = split
        elif len(split) == 2:
            class_name, field = split
            field_name = f"{field}__{class_name}"
        else:
            continue

        class_name = class_name.strip()
        field = field.strip()
        field_name = field_name.strip()

        cls = calcul_classes[class_name]
        annotations[field_name] = cls(field)
    
    return annotations

# #####################
def decode_image(encoded_image: str):

    decoded_image = base64.b64decode(bytes(encoded_image, encoding="utf-8"))
    return Image.open(io.BytesIO(decoded_image))

def copy_image(source_path: str, destination_path):

    if not pathlib.Path(destination_path).suffix:
        destination_path += pathlib.Path(source_path).suffix

    with open(source_path, mode="rb") as file_1:
        with open(destination_path, mode="wb") as file_2:
            file_2.write(file_1.read())

# #####################
def filter_set(items: QuerySet, args: dict, aggregations: dict = None):

    q = create_filter(conditions=args.get("conditions", []), aggregations=aggregations)

    if args.get("distinct", False):
        return items.filter(q).distinct()
    else:
        return items.filter(q)

def exclude_set(items: QuerySet, args: dict, aggregations: dict = None):

    q = create_filter(conditions=args.get("conditions", []), aggregations=aggregations)

    if args.get("distinct", False):
        return items.exclude(q).distinct()
    else:
        return items.exclude(q)

def annotate_set(items: QuerySet, args: dict, aggregations: dict = None):

    func = args.get("function")
    field = args.get("field")
    output = args.get("output")

    if func.lower() == "max":
        value = Max(field, filter=create_filter(args.get("conditions", []), aggregations))

    elif func.lower() == "min":
        value = Min(field, filter=create_filter(args.get("conditions", []), aggregations))

    elif func.lower() == "value":
        value = Value(field, filter=create_filter(args.get("conditions", []), aggregations))

    elif func.lower() == "avg":
        value = Avg(field, filter=create_filter(args.get("conditions", []), aggregations))

    elif func.lower() == "sum":
        value = Sum(field, filter=create_filter(args.get("conditions", []), aggregations))

    elif func.lower() == "count":
        value = Count(field, distinct=args.get("distinct", False), 
            filter=create_filter(args.get("conditions", []), aggregations)
        )
    elif func.lower() == "append":
        value = F(field)
        output = args.get("output", field)

    return items.annotate(**{output: value}) if output else items.annotate(value)

def aggregate_set(items: QuerySet, args: dict, aggregations: dict = None):

    func = args.get("function")
    field = args.get("field")
    output = args.get("output")

    if func.lower() == "max":
        value = Max(field, filter=create_filter(args.get("conditions", []), aggregations))

    elif func.lower() == "min":
        value = Min(field, filter=create_filter(args.get("conditions", []), aggregations))

    elif func.lower() == "value":
        value = Value(field, filter=create_filter(args.get("conditions", []), aggregations))

    elif func.lower() == "avg":
        value = Avg(field, filter=create_filter(args.get("conditions", []), aggregations))

    elif func.lower() == "sum":
        value = Sum(field, filter=create_filter(args.get("conditions", []), aggregations))
        
    elif func.lower() == "count":
        value = Count(field, distinct=args.get("distinct", False), 
            filter=create_filter(args.get("conditions", []), aggregations)
        )
    elif func.lower() == "append":
        value = F(field)
        output = args.get("output", field)

    return items.aggregate(**{output: value}) if output else items.aggregate(value)

def order_set(items: QuerySet, args: dict):

    fields = args.get("fields", [])

    if isinstance(fields, list):
        return items.order_by(*fields)
    
    elif isinstance(fields, str):
        return items.order_by(fields)
    
    return items

def slice_set(items: QuerySet, args: dict):

    return items[args.get("offset", 0): args.get("offset", 0) + args.get("limit", 1_000_000)]

def output_values(items: QuerySet, args: dict):

    values = args.get("values", [])
    values_args = list(filter(lambda el:isinstance(el, str), values))
    values_kwargs = list(filter(lambda el:isinstance(el, dict), values))
    values_kwargs = reduce(lambda d, el: {**d, **el}, values_kwargs, {})
    values_kwargs = {key: F(value) for key, value in values_kwargs.items()}

    return items.values(*values_args, **values_kwargs)

def create_filter(conditions: list, aggregations: dict = None):

    if aggregations is None:
        aggregations = {}

    q = Q()
    for filter in conditions:
        conditions = {}
        for expression, value in filter.items():

            if isinstance(value, dict):
                if "aggregation" in value:
                    conditions[expression] = aggregations.get(value["aggregation"])
                elif "field" in value:
                    conditions[expression] = F(value["field"])

            elif isinstance(value, list):
                conditions[expression] = list(map(
                        lambda el:
                        aggregations[el["aggregation"]] if (isinstance(el, dict) and "aggregation" in el)
                        else F(el["field"]) if (isinstance(el, dict) and "field" in el) 
                        else el
                        , value
                    )
                )

            else:
                conditions[expression] = value

        q |= Q(**conditions)

    return q

# #####################
# 1 - unchecked
# 2 - checked:
#     not accepted (reponse : message d'err)
#     accepted:
#       dilivery
#         false (waiting)
#         true -> lahget(cloturé) / lala(in the way)

# 3 - cancel // 

# status : [mzal machafhach, 
# B3atha w ray f trig, 
# b3atha w lahget, 
# lcommande fiha mouchkil(message err), 
# y'anuliha]
