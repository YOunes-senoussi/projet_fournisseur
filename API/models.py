from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

import time

# choices
coupon_types = (
    ("Product", "Product"),
    ("Category", "Category"),
    ("All", "All"),
)

order_states = (
    ("Created", "Created"),
    ("Updated", "Updated"),
    ("Deleted", "Deleted"),
    ("Accepted", "Accepted"),
    ("Refused", "Refused"),
    ("Canceled", "Canceled"),
    ("Submited", "Submited"),
    ("Sent", "Sent"),
    ("Completed", "Completed"),
    ("Started Shipping", "Started Shipping"),
    ("Delivered", "Delivered"),
)

actions = (
    ("Created", "Created"),
    ("Updated", "Updated"),
    ("Deleted", "Deleted"),
    ("Accepted", "Accepted"),
    ("Refused", "Refused"),
    ("Canceled", "Canceled"),
    ("Submited", "Submited"),
    ("Sent", "Sent"),
    ("Completed", "Completed"),
    ("Started Shipping", "Started Shipping"),
    ("Delivered", "Delivered"),
)

# ################## 
def get_now_stamp():
    return int(time.time())

# ################## 

# Create your models here.
class Store(models.Model):
    full_name = models.CharField(max_length=100, default="")
    store_name = models.CharField(max_length=100, default="")
    image_url = models.CharField(max_length=100, default="")

    phone_number = models.CharField(max_length=20, default="")
    password = models.CharField(max_length=100, default="")
    e_mail = models.CharField(max_length=100, default="")

    wilaya = models.CharField(max_length=100, default="")
    commune = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=100, default="")

    created_at = models.IntegerField(default=get_now_stamp)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # many to many relationship
    fav_clients_list = models.ManyToManyField(to="Client")

    notifications = GenericRelation(
        to="OrderNotification", 
        content_type_field="user_1_type", 
        object_id_field="user_1_id",
    )

    # reverse relationships: [group, coupon, order, product]
    
    def __str__(self):
        return f"Store: {self.store_name} ({self.full_name})"


class Client(models.Model):
    full_name = models.CharField(max_length=100, default="")
    shop_name = models.CharField(max_length=100, default="")

    phone_number = models.CharField(max_length=20, default="0")
    password = models.CharField(max_length=100, default="")
    e_mail = models.CharField(max_length=100, default="")

    wilaya = models.CharField(max_length=100, default="")
    commune = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=100, default="")

    created_at = models.IntegerField(default=get_now_stamp)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # many to many relationship
    fav_stores_list = models.ManyToManyField(to="Store")

    notifications = GenericRelation(
        to="OrderNotification", 
        content_type_field="user_1_type", 
        object_id_field="user_1_id",
    )

    # reverse relationships: [couponcount, order, orderitem, cart]

    def __str__(self):
        return f"({self.id})Shop: {self.shop_name} ({self.full_name})"


class Group(models.Model):
    name = models.CharField(max_length=100, default="")
    store = models.ForeignKey(
        to="Store",
        on_delete=models.CASCADE,
        related_name="groups",
        related_query_name="group",
    )
    created_at = models.IntegerField(default=get_now_stamp)

    # many to many relationship
    clients_list = models.ManyToManyField(to="Client")

    # reverse relationships: []

    def __str__(self):
        return f"{self.name} {self.store}"

# ################## 
class Product(models.Model):
    name = models.CharField(max_length=100, default="")
    brand = models.CharField(max_length=100, default="")
    price = models.FloatField()
    image_url = models.CharField(max_length=100, default="")

    store = models.ForeignKey(
        to="Store",
        on_delete=models.CASCADE,
        related_name="products",
        related_query_name="product",
    )
    category = models.ForeignKey(
        to="Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        related_query_name="product",
    )
    pack_type = models.ForeignKey(
        to="PackType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        related_query_name="product",
    )

    description = models.TextField(default="")
    nbr_units = models.IntegerField(default=1)
    discount = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)

    created_at = models.IntegerField(default=get_now_stamp)

    # reverse relationships: [orderitem, cartitem]

    def __str__(self):
        return f"{self.name} ({self.brand}): {self.price}DA"


class Category(models.Model):
    name = models.CharField(max_length=100, default="")
    image_url = models.CharField(max_length=100, default="")

    # reverse relationships: [product]

    def __str__(self):
        return f"{self.name}"


class PackType(models.Model):
    name = models.CharField(max_length=100, default="")

    # reverse relationships: [product]

    def __str__(self):
        return f"{self.name}"

# ################## 
class Coupon(models.Model):
    string = models.CharField(max_length=100)
    discount = models.IntegerField(default=0)
    store = models.ForeignKey(
        to="Store",
        on_delete=models.CASCADE,
        related_name="coupons",
        related_query_name="coupon",
    )

    coupon_type = models.CharField(max_length=100, choices=coupon_types, default="All")
    target_id = models.IntegerField(null=True, blank=True, default=None)

    max_nbr_uses = models.IntegerField(default=1)
    created_at = models.IntegerField(default=get_now_stamp)
    is_active = models.BooleanField(default=True)

    # reverse relationships: [couponcount, ordercoupon]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['string', 'store_id'], name='unique_coupon'),
        ]

    def __str__(self):
        return f"{self.string} => {self.coupon_type} ({self.discount}%)"


class CouponCount(models.Model):

    client = models.ForeignKey(
        to="Client",
        on_delete=models.CASCADE,
        related_name="couponcounts",
        related_query_name="couponcount",
    )

    coupon = models.ForeignKey(
        to="Coupon",
        on_delete=models.CASCADE,
        related_name="couponcounts",
        related_query_name="couponcount",
    )

    count = models.IntegerField(default=0)

    # reverse relationships: []

# ################## 
class Order(models.Model):
    store = models.ForeignKey(
        to="Store",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        related_query_name="order",
    )
    client = models.ForeignKey(
        to="Client",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        related_query_name="order",
    )

    created_at = models.IntegerField(default=get_now_stamp)
    total_price = models.FloatField(default=0.0)

    # reverse relationships: [orderstate, ordercoupon, orderitem]


class OrderState(models.Model):

    order = models.ForeignKey(
        to="Order",
        on_delete=models.CASCADE,
        related_name="orderstates",
        related_query_name="orderstate",
    )

    state = models.CharField(max_length=100, choices=order_states, default="Created")
    description = models.TextField(default="")
    time_stamp = models.IntegerField(default=get_now_stamp)

    # reverse relationships: []

    def __str__(self):
        return f"{self.order}: {self.state}"


class OrderCoupon(models.Model):

    order = models.ForeignKey(
        to="Order",
        on_delete=models.CASCADE,
        related_name="ordercoupons",
        related_query_name="ordercoupon",
    )

    coupon = models.ForeignKey(
        to="Coupon",
        on_delete=models.CASCADE,
        related_name="ordercoupons",
        related_query_name="ordercoupon",
    )

    # reverse relationships: []


class OrderItem(models.Model):
    order = models.ForeignKey(
        to="Order",
        on_delete=models.CASCADE,
        related_name="orderitems",
        related_query_name="orderitem",
    )
    product = models.ForeignKey(
        to="Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orderitems",
        related_query_name="orderitem",
    )

    quantity = models.IntegerField(default=1)
    discount = models.IntegerField(default=0)
    original_price = models.FloatField()
    new_price = models.FloatField()

    # reverse relationships: []

# ################## 
class Cart(models.Model):

    client = models.OneToOneField(
        to="Client",
        on_delete=models.CASCADE,
        related_name="cart",
        related_query_name="cart",
    )

    # reverse relationships: [cartitem]


class CartItem(models.Model):

    cart = models.ForeignKey(
        to="Cart",
        on_delete=models.CASCADE,
        related_name="cartitems",
        related_query_name="cartitem",
    )

    product = models.ForeignKey(
        to="Product",
        on_delete=models.CASCADE,
        related_name="cartitems",
        related_query_name="cartitem",
    )

    quantity = models.IntegerField(default=1)

    # reverse relationships: []

# ################## 
class OrderNotification(models.Model):

    # user who recieves the notification (Client, Store)
    user_1_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="notifications")
    user_1_id = models.PositiveIntegerField()
    user_1 = GenericForeignKey('user_1_type', 'user_1_id')

    # user who comitted the action (Client, Store)
    user_2_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    user_2_id = models.PositiveIntegerField()
    user_2 = GenericForeignKey('user_2_type', 'user_2_id')

    # action commited by user_2
    action = models.CharField(max_length=100, choices=actions, default="Created")
    message = models.TextField(default="")

    # Order that user_2 commited the action on
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True, blank=True)

    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if self.user_2_type_id == 16:
            return f"Client {self.user_2_id} {self.action} order_{self.order_id} {self.created_at.date()}"  
        else:
            return f"Store {self.user_2_id} {self.action} order_{self.order_id} {self.created_at.date()}"  

# Store:
#   client x: sent an order
#   client x: updated an order
#   client x: deleted an order
#   client x: canceled an order
# 
# 
# client:
#   store x: accepted your order
#   store x: refused your order
#   store x: order is ready
#   store x: shipping your order
# 
# 
# 
# 