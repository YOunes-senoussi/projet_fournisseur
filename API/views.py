from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from projet_fournisseur.settings import (
    DEFAULT_STORE_IMG, DEFAULT_CLIENT_IMG, 
    DEFAULT_PRODUCT_IMG, DEFAULT_CATEGORY_IMG
)
from API.models import *
from API.more_functions import (
    extract_params, aggregate_set, annotate_set, filter_set, 
    exclude_set, order_set, slice_set, output_values, decode_image, copy_image)

from django.db.models import F, Case, Value, When, Q, Avg, Max, Min, Count, Sum
import pathlib, base64

# ##################### Store Views
class StoreView(APIView):

    def get(self, request: Request, store_id: int = None):

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

    def post(self, request: Request, store_id: int = None):

        kwargs = request.data
        encoded_img = kwargs.pop("encoded_img", None)
        new_store = Store(**kwargs)
        # new_store.save()
        img_path = f"static/stores/store_{new_store.id}/store_{new_store.id}"
        
        parent_folder = pathlib.Path(img_path).parent
        parent_folder.mkdir(exist_ok=True)

        if encoded_img:
            encoded_img = encoded_img.split(",")[-1]
            try:
                image = decode_image(encoded_img)
                img_path = f"{img_path}.{image.format}"
                image.save(img_path)
                return Response(img_path)

            except Exception as e:
                return Response(data=e.args, status=400)
        
        else:
            copy_image(source_path=DEFAULT_STORE_IMG, destination_path=img_path)
        
        new_store.image_url = img_path
        # new_store.save()

        return Response({"id", new_store.id})
    
    def put(self, request: Request, store_id: int = None):

        kwargs = request.data
        encoded_img = kwargs.pop("encoded_img", None)
        Store.objects.filter(pk=store_id).update(**request.data)
        store = Store.objects.filter(pk=store_id).first()
        store.fav_clients_list

        img_path = f"static/stores/store_{store.id}/store_{store.id}"
        
        parent_folder = pathlib.Path(img_path).parent
        parent_folder.mkdir(exist_ok=True)

        if encoded_img:
            encoded_img = encoded_img.split(",")[-1]
            try:
                image = decode_image(encoded_img)
                img_path = f"{img_path}.{image.format}"
                image.save(img_path)
                return Response(img_path)

            except Exception as e:
                return Response(data=e.args, status=400)
        else:
            copy_image(source_path=DEFAULT_STORE_IMG, destination_path=img_path)
        
        return Response("success")

    def delete(self, request: Request, store_id: int = None):

        return Response(Store.objects.get(pk=store_id).delete())

# ##################### Client Views
class ClientView(APIView):

    def get(self, request: Request, client_id: int = None):

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

    def post(self, request: Request, client_id: int = None):

        new_client = Client.objects.create(**request.data)

        return Response(new_client.id)
    
    def put(self, request: Request, client_id: int = None):

        Client.objects.filter(pk=client_id).update(**request.data)

        return Response("success")
    
    def delete(self, request: Request, client_id: int = None):
        
        return Response(Client.objects.get(pk=client_id).delete())

# ##################### Product Views
class ProductView(APIView):

    def get(self, request: Request, product_id: int = None):

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

    def post(self, request: Request, product_id: int = None):

        new_product = Product.objects.create(**request.data)

        return Response(new_product.id)
    
    def put(self, request: Request, product_id: int = None):

        Product.objects.filter(pk=product_id).update(**request.data)

        return Response("success")
    
    def delete(self, request: Request, product_id: int = None):
        
        return Response(Product.objects.get(pk=product_id).delete())

# ##################### Coupon Views
class CouponView(APIView):

    def get(self, request: Request, coupon_id: int = None):

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

    def post(self, request: Request, coupon_id: int = None):

        new_coupon = Coupon.objects.create(**request.data)

        return Response(new_coupon.id)
    
    def put(self, request: Request, coupon_id: int = None):
        
        Coupon.objects.filter(pk=coupon_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, coupon_id: int = None):
        
        return Response(Coupon.objects.get(pk=coupon_id).delete())

# ##################### Order Views
class OrderView(APIView):

    def get(self, request: Request, order_id: int = None):

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

    def post(self, request: Request, order_id: int = None):

        new_order = Order.objects.create(**request.data)

        return Response(new_order.id)
    
    def put(self, request: Request, order_id: int = None):
        
        Order.objects.filter(pk=order_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, order_id: int = None):
        
        return Response(Order.objects.get(pk=order_id).delete())

# ##################### OrderCoupon Views
class OrderCouponView(APIView):

    def get(self, request: Request, ordercoupon_id: int = None):

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

    def post(self, request: Request, ordercoupon_id: int = None):

        new_ordercoupon = OrderCoupon.objects.create(**request.data)

        return Response(new_ordercoupon.id)
    
    def put(self, request: Request, ordercoupon_id: int = None):
        
        OrderCoupon.objects.filter(pk=ordercoupon_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, ordercoupon_id: int = None):
        
        return Response(OrderCoupon.objects.get(pk=ordercoupon_id).delete())

# ##################### OrderItem Views
class OrderItemView(APIView):

    def get(self, request: Request, orderitem_id: int = None):

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

    def post(self, request: Request, orderitem_id: int = None):

        new_orderitem = OrderItem.objects.create(**request.data)

        return Response(new_orderitem.id)
    
    def put(self, request: Request, orderitem_id: int = None):
        
        OrderItem.objects.filter(pk=orderitem_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, orderitem_id: int = None):
        
        return Response(OrderItem.objects.get(pk=orderitem_id).delete())

# ##################### Group Views
class GroupView(APIView):

    def get(self, request: Request, group_id: int = None):

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

    def post(self, request: Request, group_id: int = None):

        new_group = Group.objects.create(**request.data)

        return Response(new_group.id)
    
    def put(self, request: Request, group_id: int = None):
        
        Group.objects.filter(pk=group_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, group_id: int = None):
        
        return Response(Group.objects.get(pk=group_id).delete())

# ##################### Category Views
class CategoryView(APIView):

    def get(self, request: Request, category_id: int = None):

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

    def post(self, request: Request, category_id: int = None):

        new_category = Category.objects.create(**request.data)

        return Response(new_category.id)
    
    def put(self, request: Request, category_id: int = None):
        
        Category.objects.filter(pk=category_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, category_id: int = None):
        
        return Response(Category.objects.get(pk=category_id).delete())

# ##################### PackType Views
class PackTypeView(APIView):

    def get(self, request: Request, packtype_id: int = None):

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

    def post(self, request: Request, packtype_id: int = None):

        new_packtype = PackType.objects.create(**request.data)

        return Response(new_packtype.id)
    
    def put(self, request: Request, packtype_id: int = None):
        
        PackType.objects.filter(pk=packtype_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, packtype_id: int = None):
        
        return Response(PackType.objects.get(pk=packtype_id).delete())

# ##################### CouponCount Views
class CouponCountView(APIView):

    def get(self, request: Request, couponcount_id: int = None):

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

    def post(self, request: Request, couponcount_id: int = None):

        new_couponcount = CouponCount.objects.create(**request.data)

        return Response(new_couponcount.id)
    
    def put(self, request: Request, couponcount_id: int = None):
        
        CouponCount.objects.filter(pk=couponcount_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, couponcount_id: int = None):
        
        return Response(CouponCount.objects.get(pk=couponcount_id).delete())

# ##################### OrderState Views
class OrderStateView(APIView):

    def get(self, request: Request, orderstate_id: int = None):

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

    def post(self, request: Request, orderstate_id: int = None):

        new_orderstate = OrderState.objects.create(**request.data)

        return Response(new_orderstate.id)
    
    def put(self, request: Request, orderstate_id: int = None):
        
        OrderState.objects.filter(pk=orderstate_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, orderstate_id: int = None):
        
        return Response(OrderState.objects.get(pk=orderstate_id).delete())

# ##################### Cart Views
class CartView(APIView):

    def get(self, request: Request, cart_id: int = None):

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

    def post(self, request: Request, cart_id: int = None):

        new_cart = Cart.objects.create(**request.data)

        return Response(new_cart.id)
    
    def put(self, request: Request, cart_id: int = None):
        
        Cart.objects.filter(pk=cart_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, cart_id: int = None):
        
        return Response(Cart.objects.get(pk=cart_id).delete())

# ##################### CartItem Views
class CartItemView(APIView):

    def get(self, request: Request, cartitem_id: int = None):

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

    def post(self, request: Request, cartitem_id: int = None):

        new_cartitem = CartItem.objects.create(**request.data)

        return Response(new_cartitem.id)
    
    def put(self, request: Request, cartitem_id: int = None):
        
        CartItem.objects.filter(pk=cartitem_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, cartitem_id: int = None):
        
        return Response(CartItem.objects.get(pk=cartitem_id).delete())

# ##################### Notification Views
class NotificationView(APIView):

    def get(self, request: Request, notification_id: int = None):

        order_by, offset, limit, filters, values, annotations, aggregations = extract_params(request)

        if notification_id is not None:
            notifications = Notification.objects.filter(pk=notification_id).values(*values).annotate(**annotations)

            if aggregations:
                return Response({"notification": notifications.first(), **notifications.aggregate(**aggregations)})

            return Response({"notification": notifications.first()})

        notifications = (
            Notification.objects
                .values(*values).annotate(**annotations)
                .filter(**filters).distinct()
                .order_by(order_by)
        )
        notifications = notifications[offset: offset + limit]

        if aggregations:
            return Response({"notifications": notifications, **notifications.aggregate(**aggregations)})

        return Response({"notifications": notifications})

    def post(self, request: Request, notification_id: int = None):

        new_notification = Notification.objects.create(**request.data)

        return Response(new_notification.id)
    
    def put(self, request: Request, notification_id: int = None):
        
        Notification.objects.filter(pk=notification_id).update(**request.data)

        return Response("success")

    def delete(self, request: Request, notification_id: int = None):
        
        return Response(Notification.objects.get(pk=notification_id).delete())

# ################ Test
@api_view(["GET", "POST", "PUT", "DELETE"])
def test_view(request: Request):

    return Response(data="nothing")

# ################ get Store
@api_view(["POST"])
def get_stores(request: Request):

    body = request.data
    aggregations = {}

    items = Store.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get Client
@api_view(["POST"])
def get_clients(request: Request):

    body = request.data
    aggregations = {}

    items = Client.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get Group
@api_view(["POST"])
def get_groups(request: Request):

    body = request.data
    aggregations = {}

    items = Group.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get Product
@api_view(["POST"])
def get_products(request: Request):

    body = request.data
    aggregations = {}

    items = Product.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get Category
@api_view(["POST"])
def get_categories(request: Request):

    body = request.data
    aggregations = {}

    items = Category.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get PackType
@api_view(["POST"])
def get_packtypes(request: Request):

    body = request.data
    aggregations = {}

    items = PackType.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get Coupon
@api_view(["POST"])
def get_coupons(request: Request):

    body = request.data
    aggregations = {}

    items = Coupon.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get CouponCount
@api_view(["POST"])
def get_couponcounts(request: Request):

    body = request.data
    aggregations = {}

    items = CouponCount.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get Order
@api_view(["POST"])
def get_orders(request: Request):

    body = request.data
    aggregations = {}

    items = Order.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get OrderState
@api_view(["POST"])
def get_orderstates(request: Request):

    body = request.data
    aggregations = {}

    items = OrderState.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get OrderCoupon
@api_view(["POST"])
def get_ordercoupons(request: Request):

    body = request.data
    aggregations = {}

    items = OrderCoupon.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get OrderItem
@api_view(["POST"])
def get_orderitems(request: Request):

    body = request.data
    aggregations = {}

    items = OrderItem.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get Cart
@api_view(["POST"])
def get_carts(request: Request):

    body = request.data
    aggregations = {}

    items = Cart.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get CartItem
@api_view(["POST"])
def get_cartitems(request: Request):

    body = request.data
    aggregations = {}

    items = CartItem.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get Notification
@api_view(["POST"])
def get_notifications(request: Request):

    body = request.data
    aggregations = {}

    items = Notification.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get Advertisement
@api_view(["POST"])
def get_advertisements(request: Request):

    body = request.data
    aggregations = {}

    items = Advertisement.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})

# ################ get AdImage
@api_view(["POST"])
def get_adimages(request: Request):

    body = request.data
    aggregations = {}

    items = AdImage.objects.all().values()

    for operation in body:
        op_name = operation.get("operation")
        args = operation.get("args")

        if op_name and args:
            if op_name == "filter":
                items = filter_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "exclude":
                items = exclude_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "annotate":
                items = annotate_set(items=items, args=args, aggregations=aggregations)
                
            if op_name == "aggregate":
                aggregations.update(**aggregate_set(items=items, args=args, aggregations=aggregations))
                
            if op_name == "output_values":
                items = output_values(items=items, args=args)
                
            if op_name == "order":
                items = order_set(items=items, args=args)
                
            if op_name == "slice":
                items = slice_set(items=items, args=args)
        
    return Response({"aggregations": aggregations, "items": items})


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
    "cart": Cart,
    "cartitem": CartItem,
    "notification": Notification,
    "orderstate": OrderState,
}

# ################ 