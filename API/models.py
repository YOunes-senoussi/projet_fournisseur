from django.db import models
import time

# choices
coupon_types_choices = (
    ("Product", "Product"),
    ("Category", "Category"),
    ("All", "All"),
)


#####################
def get_now_stamp():
    return int(time.time())


#####################

# Create your models here.
class Store(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    store_name = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.CharField(max_length=100, null=True, blank=True)

    phone_number = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    e_mail = models.CharField(max_length=100, null=True, blank=True)

    wilaya = models.CharField(max_length=100, null=True, blank=True)
    commune = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.IntegerField(null=True, blank=True, default=get_now_stamp)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # many to many relationship
    fav_clients_list = models.ManyToManyField(to="Client")

    # reverse relationships: [product, coupon, order, group]
    
    def __str__(self):
        return f"Store: {self.store_name} ({self.full_name})"


class Client(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    shop_name = models.CharField(max_length=100, null=True, blank=True)

    phone_number = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    e_mail = models.CharField(max_length=100, null=True, blank=True)

    wilaya = models.CharField(max_length=100, null=True, blank=True)
    commune = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.IntegerField(null=True, blank=True, default=get_now_stamp)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # many to many relationship
    fav_stores_list = models.ManyToManyField(to="Store")

    # reverse relationships: [order, orderitem]

    def __str__(self):
        return f"({self.id})Shop: {self.shop_name} ({self.full_name})"


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField()
    image_url = models.CharField(max_length=100, null=True, blank=True)

    store = models.ForeignKey(
        to="Store",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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

    description = models.TextField(null=True, blank=True, default="")
    nbr_units = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True, default=0)
    is_available = models.BooleanField(null=True, blank=True, default=True)

    created_at = models.IntegerField(null=True, blank=True, default=get_now_stamp)

    # reverse relationships: [order, orderitem]

    def __str__(self):
        return f"{self.name} ({self.brand}): {self.price}DA"


class Coupon(models.Model):
    string = models.CharField(max_length=100, null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True, default=0)
    store = models.ForeignKey(
        to="Store",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coupons",
        related_query_name="coupon",
    )

    coupon_type = models.CharField(max_length=100, choices=coupon_types_choices)
    target_id = models.IntegerField(null=True, blank=True)

    max_nbr_uses = models.IntegerField(null=True, blank=True)
    created_at = models.IntegerField(null=True, blank=True, default=get_now_stamp)
    is_active = models.BooleanField(null=True, blank=True, default=True)

    # reverse relationships: [ordercoupon]

    def __str__(self):
        return f"{self.string} => {self.coupon_type} ({self.discount}%)"


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

    created_at = models.IntegerField(null=True, blank=True, default=get_now_stamp)
    error_description = models.TextField(null=True, blank=True, default="")
    total_price = models.FloatField(null=True, blank=True, default=0)

    is_accepted = models.BooleanField(null=True, blank=True)
    is_delivered = models.BooleanField(null=True, blank=True)

    # reverse relationships: [ordercoupon, orderitem]


class OrderCoupon(models.Model):
    
    order = models.ForeignKey(
        to="Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ordercoupons",
        related_query_name="ordercoupon",
    )

    coupon = models.ForeignKey(
        to="Coupon",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ordercoupons",
        related_query_name="ordercoupon",
    )

    # reverse relationships: []


class OrderItem(models.Model):
    order = models.ForeignKey(
        to="Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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

    quantity = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    original_price = models.FloatField(null=True, blank=True)
    new_price = models.FloatField(null=True, blank=True)

    # reverse relationships: []


class Group(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    store = models.ForeignKey(
        to="Store",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="groups",
        related_query_name="group",
    )
    created_at = models.IntegerField(null=True, blank=True, default=get_now_stamp)

    # many to many relationship
    clients_list = models.ManyToManyField(to="Client")

    # reverse relationships: []

    def __str__(self):
        return f"{self.name} {self.store}"


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    # reverse relationships: [product]

    def __str__(self):
        return f"{self.name}"


class PackType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    # reverse relationships: [product]
    def __str__(self):
        return f"{self.name}"
