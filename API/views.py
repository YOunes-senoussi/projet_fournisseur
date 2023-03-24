from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from API.models import *
from API.more_functions import extract_params, RequestHandler, simple_Q

# ##################### Generic Views
class GetView(APIView):

    def get(self, request: Request, model_name: str, item_id: int = None):
        
        model = tables.get(model_name)
        if model is None:
            return Response(f"table {model_name} doesn't exist.", status=400)
        
        order, offset, limit, filters, exclusions, values, annotations, aggregations = extract_params(request)

        items = (
            model.objects
                .values(*values["args"], **values["kwargs"]).annotate(**annotations)
                .filter(simple_Q(filters if item_id is None else {"pk": item_id})).distinct()
                .exclude(simple_Q(exclusions if item_id is None else {})).distinct()
                .order_by(*order)[offset: offset + limit]
        )

        return Response({
            "aggregations": {**items.aggregate(**aggregations)} if aggregations else {},
            "items": items, 
            })

    def post(self, request: Request, model_name: str, item_id: int = None):

        if not request.data:
            return Response(data={"error": "No/Empty Body"}, status=400)

        model = tables.get(model_name)
        if model is None:
            return Response(f"table {model_name} doesn't exist.", status=400)
        
        operations = request.data
        if item_id is None:
            items = model.objects.all().values()
        else: 
            items = model.objects.filter(pk=item_id).values()
            ops = ["filter", "exclude", "order", "slice"]
            operations = list(filter(lambda op: op["operation"] not in ops, operations))

        items, aggregations = RequestHandler(items=items, operations=operations).apply_operations()

        return Response({"aggregations": aggregations, "items": items})

    def put(self, request: Request, model_name: str, item_id: int = None):
        return Response("nothing")

    def delete(self, request: Request, model_name: str, item_id: int = None):
        return Response("nothing")

# ################ Generic retrieve using POST
@api_view(["POST"])
def get_items(request: Request, model_name: str, item_id: int = None):

    model = tables.get(model_name)
    if model is None:
        return Response(f"table {model_name} doesn't exist.", status=400)
    
    operations = request.data
    if item_id is None:
        items = model.objects.all().values()
    else: 
        items = model.objects.filter(pk=item_id).values()
        ops = ["filter", "exclude", "order", "slice"]
        operations = list(filter(lambda op: op["operation"] not in ops, operations))

    items, aggregations = RequestHandler(items=items, operations=operations).apply_operations()

    return Response({"aggregations": aggregations, "items": items})


@api_view(["POST", "PUT"])
def create_item(request: Request, model_name: str):

    if not request.data:
        return Response(data={"error": "No/Empty Body"}, status=400)

    model = tables.get(model_name)
    if model is None:
        return Response(f"table {model_name} doesn't exist.", status=400)
    
    try:
        return Response(model.create(**request.data).to_dict())

    except Exception as e:
        return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)


@api_view(["POST", "PUT"])
def update_item(request: Request, model_name: str, item_id: int):

    if not request.data:
        return Response(data={"error": "No/Empty Body"}, status=400)
    
    model = tables.get(model_name)
    if model is None:
        return Response(f"table {model_name} doesn't exist.", status=400)
    
    try:
        return Response(model.objects.get(pk=item_id).update(**request.data).to_dict())
    
    except Exception as e:
        return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)
    

@api_view(["DELETE"])
def delete_item(request: Request, model_name: str, item_id: int):

    model = tables.get(model_name)
    if model is None:
        return Response(f"table {model_name} doesn't exist.", status=400)
    
    try:
        return Response(model.objects.get(pk=item_id).delete())
    
    except Exception as e:
        return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)
    
# Many To Many Relationships:
# ##################### Client Fav Stores Views
class ClientFavStoresView(APIView):

    def get(self, request: Request, client_id: int = None):

        try:
            return Response(Client.objects.get(pk=client_id).clientfavstores.values())
        except Exception as e:
            return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)

    def post(self, request: Request, client_id: int = None):

        try:
            client = Client.objects.get(pk=client_id)
            operation = request.data.get("operation")
            stores = request.data.get("stores", [])
            stores_ids = list(map(lambda el:el["store_id"], stores))

            if operation=="add":
                client.fav_stores.add(*Store.objects.filter(id__in=stores_ids))

            elif operation=="set":
                client.fav_stores.set(Store.objects.filter(id__in=stores_ids))

            elif operation=="remove":
                client.fav_stores.remove(*Store.objects.filter(id__in=stores_ids))

            elif operation=="clear":
                client.fav_stores.clear()
            
            return Response(client.clientfavstores.values())
            
        except Exception as e:
            return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)
    
    def put(self, request: Request, client_id: int = None):
        return Response("nothing")

    def delete(self, request: Request, client_id: int = None):
        return Response("nothing")

# ##################### Store Fav Clients Views
class StoreFavClientsView(APIView):

    def get(self, request: Request, store_id: int = None):

        try:
            return Response(Store.objects.get(pk=store_id).storefavclients.values())
        except Exception as e:
            return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)

    def post(self, request: Request, store_id: int = None):

        try:
            store = Store.objects.get(pk=store_id)
            operation = request.data.get("operation")
            clients = request.data.get("clients", [])
            clients_ids = list(map(lambda el:el["client_id"], clients))

            if operation=="add":
                store.fav_clients.add(*Client.objects.filter(id__in=clients_ids))

            elif operation=="set":
                store.fav_clients.set(Client.objects.filter(id__in=clients_ids))

            elif operation=="remove":
                store.fav_clients.remove(*Client.objects.filter(id__in=clients_ids))

            elif operation=="clear":
                store.fav_clients.clear()
            
            return Response(store.storefavclients.values())
            
        except Exception as e:
            return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)

    def put(self, request: Request, store_id: int = None):
        return Response("nothing")

    def delete(self, request: Request, store_id: int = None):
        return Response("nothing")

# ##################### Group Clients Views
class GroupClientsView(APIView):

    def get(self, request: Request, group_id: int):

        try:
            return Response(Group.objects.get(pk=group_id).groupclients.values())
        except Exception as e:
            return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)

    def post(self, request: Request, group_id: int = None):

        try:
            group = Group.objects.get(pk=group_id)
            operation = request.data.get("operation")
            clients = request.data.get("clients", [])
            clients_ids = list(map(lambda el:el["client_id"], clients))

            if operation=="add":
                group.clients.add(*Client.objects.filter(id__in=clients_ids))

            elif operation=="set":
                group.clients.set(Client.objects.filter(id__in=clients_ids))

            elif operation=="remove":
                group.clients.remove(*Client.objects.filter(id__in=clients_ids))

            elif operation=="clear":
                group.clients.clear()

            return Response(group.groupclients.values())
        
        except Exception as e:
            return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)

    def put(self, request: Request, group_id: int = None):
        return Response("nothing")

    def delete(self, request: Request, group_id: int = None):
        return Response("nothing")

# ##################### Cart Products Views
class CartProductsView(APIView):

    def get(self, request: Request, cart_id: int):

        try:
            return Response(Cart.objects.get(pk=cart_id).cartproducts.values())
        except Exception as e:
            return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)

    def post(self, request: Request, cart_id: int = None):
        return Response("nothing")

    def put(self, request: Request, cart_id: int = None):
        return Response("nothing")

    def delete(self, request: Request, cart_id: int = None):
        return Response("nothing")

# ##################### Order Products Views
class OrderProductsView(APIView):

    def get(self, request: Request, order_id: int):

        try:
            return Response(Order.objects.get(pk=order_id).orderproducts.values())
        except Exception as e:
            return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)

    def post(self, request: Request, order_id: int = None):
        return Response("nothing")
        
    def put(self, request: Request, order_id: int = None):
        return Response("nothing")

    def delete(self, request: Request, order_id: int = None):
        return Response("nothing")

# ##################### Order Coupons Views
class OrderCouponsView(APIView):

    def get(self, request: Request, order_id: int):

        try:
            return Response(Order.objects.get(pk=order_id).ordercoupons.values())
        except Exception as e:
            return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)

    def post(self, request: Request, order_id: int = None):
        return Response("nothing")

    def put(self, request: Request, order_id: int = None):
        return Response("nothing")

    def delete(self, request: Request, order_id: int = None):
        return Response("nothing")

# ##################### Coupon Clients Views
class CouponClientsView(APIView):

    def get(self, request: Request, coupon_id: int, client_id: int = None):

        try:
            if client_id is not None:
                return Response(CouponClient.objects.filter(coupon_id=coupon_id, client_id=client_id).values())
            else:
                return Response(CouponClient.objects.filter(coupon_id=coupon_id).values())
        except Exception as e:
            return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)

    def post(self, request: Request, coupon_id: int, client_id: int):
        return Response("nothing")

    def put(self, request: Request, coupon_id: int, client_id: int = None):
        return Response("nothing")

    def delete(self, request: Request, coupon_id: int, client_id: int = None):
        return Response("nothing")

# ################ Models
tables = {
    "store": Store,
    "client": Client,
    "group": Group,
    "product": Product,
    "category": Category,
    "packtype": PackType,
    "coupon": Coupon,
    "order": Order,
    "orderstate": OrderState,
    "cart": Cart,
    "notification": Notification,
    "ad": Advertisement,
    "adimage": AdImage,

    "cartproduct": CartProduct,
    "ordercoupon": OrderCoupon,
    "orderproduct": OrderProduct,
    "groupclient": GroupClient,
    "storefavclient": StoreFavClient,
    "clientfavstore": ClientFavStore,
    "couponclient": CouponClient,
}

# ################ Test
@api_view(["GET", "POST", "PUT", "DELETE"])
def test_view(request: Request):

    try:
        return Response("nothing")
    
    except Exception as e:
        return Response(data={"error": e.__class__.__name__, "args": e.args}, status=400)

# ################ 

# Delete: 
#   instance: method + signals
#   in bulk : signals
#   CASCADE : signals
# 
# Save (create or update): 
#   instance: method + signals
#   in bulk : nothing
# 
# 
# 