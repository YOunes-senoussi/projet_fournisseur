from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from django.conf import settings
from django.db.models import F, Case, Value, When, Q, Avg, Max, Min, Count, Sum
from django.db.models.query import QuerySet
from django.db.models.functions.math import Abs, Power, Round, Sqrt, Mod
from django.db.models.functions.text import Reverse, Concat, Lower, Upper, Length
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from functools import reduce
from django.core.handlers.wsgi import WSGIRequest

from API.models import *
from API.some_functions import *
# ################ 

# ##################### query params for GET requests
def extract_params(request: Request):

    params = request.query_params

    values = params.getlist("output", [])
    values = list(map(lambda el: el.split(":") if ":" in el else el, values))
    values_args = list(filter(lambda el:isinstance(el, str), values))

    values_kwargs = list(filter(lambda el:isinstance(el, list), values))
    values_kwargs = dict(values_kwargs)
    values_kwargs = {key.strip(): F(value.strip()) for key, value in values_kwargs.items()}

    values = {"args": values_args, "kwargs": values_kwargs}

    annotations = get_annotations(params.getlist("annotate", []))
    aggregations = get_annotations(params.getlist("aggregate", []))

    filters = dict(list(map(lambda el:el.split(":"), params.getlist("filter", []))))
    exclusions = dict(list(map(lambda el:el.split(":"), params.getlist("exclude", []))))

    order = params.getlist("order", ["pk"])
    offset = int(params.get("offset", 0))
    limit = int(params.get("limit", 1_000_000))

    return order, offset, limit, filters, exclusions, values, annotations, aggregations


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
class RequestHandler:

    def __init__(self, items: QuerySet, operations: list) -> None:
        self.items = items
        self.operations = operations
        self.aggregations = {}

    def filter_set(self, kwargs: dict):

        if kwargs.get("distinct", False):
            return self.items.filter(self.create_filter(kwargs.get("conditions", []))).distinct()
        else:
            return self.items.filter(self.create_filter(kwargs.get("conditions", [])))
        
    def exclude_set(self, kwargs: dict):

        if kwargs.get("distinct", False):
            return self.items.exclude(self.create_filter(kwargs.get("conditions", []))).distinct()
        else:
            return self.items.exclude(self.create_filter(kwargs.get("conditions", [])))

    def order_set(self, kwargs: dict):

        fields = kwargs.get("fields", [])

        if isinstance(fields, list):
            return self.items.order_by(*fields)
        
        return self.items.order_by(fields)
    
    def output_values(self, kwargs: dict):

        values = kwargs.get("values", [])
        values_args = list(filter(lambda el:isinstance(el, str), values))
        values_kwargs = list(filter(lambda el:isinstance(el, dict), values))
        values_kwargs = reduce(lambda d, el: {**d, **el}, values_kwargs, {})
        values_kwargs = {key: F(value) for key, value in values_kwargs.items()}

        return self.items.values(*values_args, **values_kwargs)

    def slice_set(self, kwargs: dict):

        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 1_000_000)
        return self.items[offset: offset + limit]

    def annotate_set(self, kwargs: dict):

        output = kwargs.get("output")

        if output is not None:
            return self.items.annotate(**{output: self.get_annot_func(kwargs)})
        else:
            return self.items.annotate(self.get_annot_func(kwargs))

    def aggregate_set(self, kwargs: dict):

        output = kwargs.get("output")

        if output is not None:
            return self.items.aggregate(**{output: self.get_annot_func(kwargs)})
        else:
            return self.items.aggregate(self.get_annot_func(kwargs))

    # #####################
    def apply_operations(self):

        for operation in self.operations:
            op_name = operation.get("operation")
            args = operation.get("args")

            self.apply_op(op_name=op_name, args=args)

        return self.items, self.aggregations

    def apply_op(self, op_name: str, args: dict):

        if op_name and args:
            if op_name == "aggregate":
                self.aggregations.update(**self.aggregate_set(args))

            elif op_name == "annotate":
                self.items = self.annotate_set(args)

            elif op_name == "exclude":
                self.items = self.exclude_set(args)

            elif op_name == "filter":
                self.items = self.filter_set(args)

            elif op_name == "order":
                self.items = self.order_set(args)

            elif op_name == "output":
                self.items = self.output_values(args)

            elif op_name == "slice":
                self.items = self.slice_set(args)

    # ##################### Unused
    def Q_object(self, conditions):

        if isinstance(conditions, list):
            return reduce(lambda init_q, clause: init_q | self.Q_object(clause), conditions, Q())

        elif isinstance(conditions, dict):
            q = Q()
            for key, value in conditions.items():

                if key.startswith("-"):
                    key = key[1:]
                    q &= ~Q(**{key: self.get_expression(value, False)})
                else:
                    q &= Q(**{key: self.get_expression(value, False)})

            # return Q(**{key: self.get_expression(value, False) for key, value in conditions.items()})

        return q

    def get_expression(self, kwargs, str_is_field: bool = True):
        # sourcery skip: low-code-quality

        if isinstance(kwargs, dict):

            if "value" in kwargs:
                return Value(kwargs["value"])
            
            elif "field" in kwargs:
                return F(kwargs["field"])
            
            elif "aggregation" in kwargs:
                return Value(self.aggregations[kwargs["aggregation"]])

            func_name = kwargs["function"].lower()
            args = kwargs["args"]
            
            if func_name=="value": 
                return Value(args)
            
            elif func_name=="field": 
                return F(args)
            
            elif func_name=="aggregation":
                return Value(self.aggregations[args])
            

            elif func_name=="max": 
                return Max(self.get_expression(args["f"], True), filter=self.Q_object(args.get("conditions", [])))
            
            elif func_name=="min": 
                return Min(self.get_expression(args["f"], True), filter=self.Q_object(args.get("conditions", [])))
            
            elif func_name=="avg": 
                return Avg(self.get_expression(args["f"], True), filter=self.Q_object(args.get("conditions", [])))
            
            elif func_name=="sum": 
                return Sum(self.get_expression(args["f"], True), filter=self.Q_object(args.get("conditions", [])))
            
            elif func_name=="count": 
                return Count(self.get_expression(args["f"], True), filter=self.Q_object(args.get("conditions", [])), 
                            distinct=args.get("distinct", False))
            

            elif func_name=="abs": 
                return Abs(self.get_expression(args["n"], True))
            
            elif func_name=="power": 
                return Power(self.get_expression(args["x"], True), self.get_expression(args["y"], True))
            
            elif func_name=="round": 
                return Round(self.get_expression(args["n"], True), self.get_expression(args.get("r", 0), True))
            
            elif func_name=="sqrt": 
                return Sqrt(self.get_expression(args["n"], True))
            
            elif func_name=="mod": 
                return Mod(self.get_expression(args["x"], True), self.get_expression(args["y"], True))
            

            elif func_name=="reverse": 
                return Reverse(self.get_expression(args["s"], True))
            
            elif func_name=="concat": 

                strings = args["s"]
                if not isinstance(strings, list):
                    strings = [strings]

                strings = list(map(lambda el: self.get_expression(el, True), strings))
                return Concat(*strings)
            
            elif func_name=="lower": 
                return Lower(self.get_expression(args["s"], True))
            
            elif func_name=="upper": 
                return Upper(self.get_expression(args["s"], True))
            
            elif func_name=="length": 
                return Length(self.get_expression(args["s"], True))
            

        elif isinstance(kwargs, list):
            return list(map(lambda el: self.get_expression(el, str_is_field), kwargs))
        
        elif isinstance(kwargs, str):
            return F(kwargs) if str_is_field else Value(kwargs)

        return Value(kwargs)

    # #####################
    def get_annot_func(self, kwargs: dict):  
        # sourcery skip: low-code-quality
        
        func_name = kwargs["function"].lower()
        if func_name=="append": 
            return self.get_value(kwargs["f"])
        
        elif func_name=="max": 
            return Max(self.get_value(kwargs["f"]), filter=self.create_filter(kwargs.get("conditions", [])))

        elif func_name=="min": 
            return Min(self.get_value(kwargs["f"]), filter=self.create_filter(kwargs.get("conditions", [])))
        
        elif func_name=="avg": 
            return Avg(self.get_value(kwargs["f"]), filter=self.create_filter(kwargs.get("conditions", [])))
        
        elif func_name=="sum": 
            return Sum(self.get_value(kwargs["f"]), filter=self.create_filter(kwargs.get("conditions", [])))
        
        elif func_name=="count": 
            return Count(self.get_value(kwargs["f"]), filter=self.create_filter(kwargs.get("conditions", [])), 
                        distinct=kwargs.get("distinct", False))
        

        elif func_name=="abs": 
            return Abs(self.get_value(kwargs["n"]))
        
        elif func_name=="power": 
            return Power(self.get_value(kwargs["x"]), self.get_value(kwargs["y"]))
        
        elif func_name=="round": 
            return Round(self.get_value(kwargs["n"]), self.get_value(kwargs["r"]))
        
        elif func_name=="sqrt": 
            return Sqrt(self.get_value(kwargs["n"]))
        
        elif func_name=="mod": 
            return Mod(self.get_value(kwargs["x"]), self.get_value(kwargs["y"]))
        

        elif func_name=="reverse": 
            return Reverse(self.get_value(kwargs["s"]))
        
        elif func_name=="concat": 

            strings = kwargs["s"]
            if not isinstance(strings, list):
                strings = [strings]

            strings = list(map(lambda el: self.get_value(el), strings))
            return Concat(*strings)
        
        elif func_name=="lower": 
            return Lower(self.get_value(kwargs["s"]))
        
        elif func_name=="upper": 
            return Upper(self.get_value(kwargs["s"]))
        
        elif func_name=="length": 
            return Length(self.get_value(kwargs["s"]))
        
    def get_value(self, arg, str_is_field: bool = True):

        if isinstance(arg, str):
            return F(arg) if str_is_field else Value(arg)
        
        elif isinstance(arg, dict):
            if "field" in arg: return F(arg["field"])
            if "value" in arg: return Value(arg["value"])
            if "aggregate" in arg: return self.aggregations[arg["aggregate"]]

        elif isinstance(arg, list):
            return list(map(lambda el: self.get_value(el, str_is_field), arg))
        
        return Value(arg)

    def create_filter(self, conditions):

        if isinstance(conditions, list):
            return reduce(lambda init_q, clause: init_q | self.create_filter(clause), conditions, Q())

        elif isinstance(conditions, dict):
            q = Q()
            for key, value in conditions.items():

                if key.startswith("-"):
                    key = key[1:]
                    q &= ~Q(**{key: self.get_value(value, str_is_field=False)})
                else:
                    q &= Q(**{key: self.get_value(value, str_is_field=False)})

        return q


# ##################### Signals
@receiver(post_delete, sender=Store, dispatch_uid="not unique string")
@receiver(post_delete, sender=Client, dispatch_uid="not unique string")
@receiver(post_delete, sender=Product, dispatch_uid="not unique string")
@receiver(post_delete, sender=Category, dispatch_uid="not unique string")
@receiver(post_delete, sender=Advertisement, dispatch_uid="not unique string")
@receiver(post_delete, sender=AdImage, dispatch_uid="not unique string")
def post_delete_func(sender, instance=None, **kwargs):

    if sender == Store:
        delete_dir(instance.dir_path)
        User.objects.filter(pk=instance.account_id).delete()

    elif sender == Client:
        delete_dir(instance.dir_path)
        User.objects.filter(pk=instance.account_id).delete()

    elif sender == Product:
        delete_dir(instance.dir_path)

    elif sender == Category:
        delete_dir(instance.dir_path)

    elif sender == Advertisement:
        delete_dir(instance.dir_path)
    
    elif sender == AdImage:
        delete_img(instance.url)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# ##################### MiddleWare
def simple_middleware(get_response):

    def middleware(request: WSGIRequest):

        # token = request.headers.get("Authorization")
        # if token is None:
        #     return Response("no token was provided", status=400)
        
        # token = token.lstrip("Token ")
        # print(f"{token=}")
        # print(f"{request.path=}")
        
        response = get_response(request)

        return response

    return middleware

# #####################
def decrement_coupon_count(id: int = None, coupon_id: int = None, client_id: int = None):

    if id is not None:
        coupon_client = CouponClient.objects.filter(id=id).first()
    else:
        coupon_client = CouponClient.objects.filter(coupon_id=coupon_id, client_id=client_id).first()

    if coupon_client is None:
        return False
    
    if coupon_client.count <= 1:
        coupon_client.delete()
    else:
        coupon_client.count -= 1
        coupon_client.save()

    return True

def increment_coupon_count(id: int = None, coupon_id: int = None, client_id: int = None):

    if id is not None:
        coupon_client = CouponClient.objects.filter(id=id).first()
        if coupon_client is None:
            return False
        
        coupon_client.count += 1
        coupon_client.save()
    else:
        coupon_client, created = CouponClient.objects.get_or_create(coupon_id=coupon_id, client_id=client_id)

        if not created:
            coupon_client.count += 1
            coupon_client.save()
        
    return True

# ##################### Specific Order Views
# ################ some variables
SUCCESS = 100
FAIL = -100

COUPON_FOUND = 0
PRODUCT_FOUND = 1

STORE_NOT_FOUND = -1
CLIENT_NOT_FOUND = -2

COUPON_NOT_FOUND = -3
COUPON_NOT_ACTIVE = -5
COUPON_USAGE_LIMIT = -7
COUPON_WRONG_STORE = -9
COUPON_NO_PRODUCTS = -11

PRODUCT_NOT_FOUND = -2
PRODUCT_WRONG_STORE = -4
PRODUCT_NOT_AVAILABLE = -6
PRODUCT_WRONG_PRICE = -8

@api_view(["POST", "PUT"])
def create_order(request: Request):

    store_id = request.data.get("store_id", None)
    client_id = request.data.get("client_id", None)
    products_qtes = request.data.get("products", [])
    coupons_ids = request.data.get("coupons", [])
    description = request.data.get("description", "")

    if not Client.objects.filter(pk=client_id).exists():
        return Response(f"Client ({client_id}) doesn't exist", status=400)

    if not Store.objects.filter(pk=store_id).exists():
        return Response(f"Store ({store_id}) doesn't exist", status=400)

    products_ids = list(map(lambda p:p["product_id"], products_qtes))
    products_qtes = dict(list(map(lambda p:(p["product_id"], p["quantity"]), products_qtes)))
    products = Product.objects.filter(store_id=store_id, id__in=products_ids).values()
    list(map(lambda product: product.update({"quantity": products_qtes[product["id"]]}), products))

    coupons = Coupon.objects.filter(store_id=store_id, id__in=coupons_ids).values()

    for coupon_id in coupons:
        for product in products:
            if ((coupon_id["coupon_type"]=="all") or 
                (coupon_id["coupon_type"]=="category" and product["category_id"]==coupon_id["target_id"]) or 
                (coupon_id["coupon_type"]=="product" and product["id"]==coupon_id["target_id"])):
                product["discount"] += coupon_id["discount"]

    total_price = 0
    for product in products:
        product["new_price"] = round(product["price"]*product["quantity"]*(1-(product["discount"]/100)), 2)
        total_price += product["new_price"]

    order = Order.create(store_id=store_id, client_id=client_id, total_price=round(total_price, 2))

    for product in products:
        OrderProduct.create(
            order_id=order.id,
            product_id=product["id"],
            discount=product["discount"],
            quantity=product["quantity"],
            original_price=product["price"],
            new_price=product["new_price"],
        )

    for coupon_id in coupons_ids:
        OrderCoupon.create(order_id=order.id, coupon_id=coupon_id)
        increment_coupon_count(coupon_id=coupon_id, client_id=client_id)

    order.current_state = OrderState.create(
        order_id=order.id, 
        state="Created", 
        description=description, 
        updated_by_store=False,
    )
    order.save()

    StoreNotification.create(
        store_id=store_id,
        action="Create",
        message=f"Client({client_id}) created an Order({order.id})"
    )

    return Response(order.to_dict())


@api_view(["POST", "PUT"])
def update_order_state(request: Request, order_id: int):

    order = Order.objects.filter(pk=order_id).first()
    if order is None:
        return Response({"error": f"order: {order_id} does not exist"}, status=400)

    kwargs = request.data
    state = kwargs["state"]
    description = kwargs["description"]
    updated_by_store = kwargs.get("updated_by_store", True)

    order.current_state = OrderState.objects.create(
        order_id=order_id, 
        state=state, 
        description=description, 
        updated_by_store=updated_by_store,
    )
    order.save()

    # creating a notification

    action = order.current_state.state
    
    if updated_by_store:
        StoreNotification.create(
            store_id=order.store_id,
            action=order.current_state.state,
            message=f"Store({order.store_id}) {action} Order({order.id})"
        )
    else:
        ClientNotification.create(
            client_id=order.client_id,
            action=order.current_state.state,
            message=f"Client({order.client_id}) {action} Order({order.id})"
        )

    return Response(order.to_dict())


@api_view(["DELETE"])
def delete_order(request: Request, order_id: int):
    return Response(Order.objects.filter(pk=order_id).delete())


@api_view(["POST"])
def check_coupon(request: Request):

    store_id = request.data.get("store_id", None)
    client_id = request.data.get("client_id", None)
    coupon = request.data.get("coupon", None)
    products_ids = request.data.get("products", [])

    if not Client.objects.filter(pk=client_id).exists():
        return Response(
            {
                "valide": False,
                "coupon": None,
                "code": CLIENT_NOT_FOUND,
                "code_text": "CLIENT_NOT_FOUND",
                "products": [],
            },
            status=400
        )

    if not Store.objects.filter(pk=store_id).exists():
        return Response(
            {
                "valide": False,
                "coupon": None,
                "code": STORE_NOT_FOUND,
                "code_text": "STORE_NOT_FOUND",
                "products": [],
            },
            status=400
        )

    coupon = Coupon.objects.filter(string=coupon, store_id=store_id).first()

    if not coupon:

        return Response(
            {
                "valide": False,
                "coupon": None,
                "code": COUPON_NOT_FOUND,
                "code_text": "COUPON_NOT_FOUND",
                "products": [],
            },
            status=400
        )

    if not coupon.is_active:
        return Response(
            {
            "valide": False,
            "coupon": None,
            "code": COUPON_NOT_ACTIVE,
            "code_text": "COUPON_NOT_ACTIVE",
            "products": [],
            },
            status=400
        )

    coupon_client = CouponClient.objects.filter(client_id=client_id, coupon_id=coupon.id).first()

    if coupon_client is not None and coupon_client.count >= coupon.max_nbr_uses:
        return Response(
            {
                "valide": False,
                "coupon": None,
                "code": COUPON_USAGE_LIMIT,
                "code_text": "COUPON_USAGE_LIMIT",
                "products": [],
            },
            status=400
        )

    products = Product.objects.filter(id__in=products_ids)
    products = list(filter(lambda p:coupon_on_product(coupon, p), products))
    products = list(map(lambda p:p.id, products))

    if products:
        return Response(
                {
                    "valide": True,
                    "coupon": coupon.to_dict(),
                    "code": COUPON_FOUND,
                    "code_text": "COUPON_FOUND",
                    "products": products,
                }
            )
    else: 
        return Response(
            {
                "valide": False,
                "coupon": None,
                "code": COUPON_NO_PRODUCTS,
                "code_text": "COUPON_NO_PRODUCTS",
                "products": [],
            },
            status=400,
        )
    

def coupon_on_product(coupon: Coupon, product: Product):

    if coupon.coupon_type=="All":
        return True
    elif coupon.coupon_type=="Category" and coupon.target_id==product.category_id:
        return True
    elif coupon.coupon_type=="Product" and coupon.target_id==product.id:
        return True
    
    return False

# #####################

################ Temporary

import json

def pop_tab(file_name: str):

    with open(f"more data/old_data/{file_name}.json", mode="r", encoding="utf8") as file:
        json_data = json.load(fp=file)
        model = get_model(file_name)
        if model is None:
            print(f"{file_name} is None")
            return
        
        for el in json_data:
            model.create(**el)

def get_model(name: str):

    if name=="store": return Store
    elif name=="client": return Client
    elif name=="group": return Group
    elif name=="groupclient": return GroupClient
    elif name=="storefavclient": return StoreFavClient
    elif name=="clientfavstore": return ClientFavStore

    elif name=="product": return Product
    elif name=="category": return Category
    elif name=="packtype": return PackType
    elif name=="clientproduct": return ClientProduct

    elif name=="coupon": return Coupon
    elif name=="couponclient": return CouponClient

    elif name=="order": return Order
    elif name=="orderstate": return OrderState
    elif name=="ordercoupon": return OrderCoupon
    elif name=="orderproduct": return OrderProduct

    elif name=="advertisement": return Advertisement
    elif name=="adimage": return AdImage

    elif name=="storenotification": return StoreNotification
    elif name=="clientnotification": return ClientNotification


def read_json(file_name: str):

    with open(f"{file_name}.json", mode="r", encoding="utf8") as file:
        json_data = json.load(fp=file)
    return json_data

def write_json(json_data, file_name: str):

    with open(f"{file_name}.json", mode="w", encoding="utf8") as file:
        json.dump(json_data, fp=file, ensure_ascii=False, indent=2)

