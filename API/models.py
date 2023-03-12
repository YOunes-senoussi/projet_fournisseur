from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

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

    store_name = models.CharField(max_length=100, default="")

    full_name = models.CharField(max_length=100, default="")
    image_url = models.CharField(max_length=1000, default="")

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

    # reverse relationships: [group*, coupon*, order*, product*, notification*, ad*]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['store_name'], name='unique_store_name'),
            models.UniqueConstraint(fields=['phone_number'], name='unique_store_phone_numbre'),
        ]
    
    def __str__(self):
        return f"Store: {self.store_name} ({self.full_name})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class Client(models.Model):

    shop_name = models.CharField(max_length=100, default="")

    full_name = models.CharField(max_length=100, default="")
    image_url = models.CharField(max_length=1000, default="")

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
    fav_stores_list = models.ManyToManyField(to="Store")

    # reverse relationships: [couponcount*, order*, orderitem*, notification*, cart]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['shop_name'], name='unique_shop_name'),
            models.UniqueConstraint(fields=['phone_number'], name='unique_shop_phone_numbre'),
        ]

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'store_id'], name='unique_group_name'),
        ]

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

    # reverse relationships: [orderitem*, cartitem*, ad*]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'store_id'], name='unique_product_name'),
            models.CheckConstraint(check=Q(price__gte=1), name='positive_price'),
            models.CheckConstraint(check=Q(nbr_units__gte=1), name='positive_nbr_units'),
            models.CheckConstraint(check=Q(discount__gte=0) & Q(discount__lte=100), 
                                   name='correct_product_discount'),
        ]

    def __str__(self):
        return f"{self.name} ({self.brand}): {self.price}DA"


class Category(models.Model):
    name = models.CharField(max_length=100, default="")
    image_url = models.CharField(max_length=100, default="")

    # reverse relationships: [product*]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name'),
        ]

    def __str__(self):
        return f"{self.name}"


class PackType(models.Model):
    name = models.CharField(max_length=100, default="")

    # reverse relationships: [product*]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_pack_type_name'),
        ]

    def __str__(self):
        return f"{self.name}"

# ################## 
class Coupon(models.Model):
    string = models.CharField(max_length=100)
    discount = models.IntegerField(default=1)
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

    # reverse relationships: [couponcount*, ordercoupon*]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['string', 'store_id'], name='unique_coupon'),
            models.CheckConstraint(check=Q(max_nbr_uses__gte=1), name='positive_max_nbr_uses'),
            models.CheckConstraint(check=Q(discount__gte=1) & Q(discount__lte=100), 
                                   name='correct_coupon_discount'),
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

    count = models.IntegerField(default=1)

    # reverse relationships: []

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client_id', 'coupon_id'], name='unique_client_coupon'),
            models.CheckConstraint(check=Q(count__gte=1), name='coupon_count_positive_count'),
        ]

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
    total_price = models.FloatField(default=1.0)

    archived_by_store = models.BooleanField(default=False)
    archived_by_client = models.BooleanField(default=False)

    # reverse relationships: [orderstate*, ordercoupon*, orderitem*]
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(total_price__gte=1), name='order_positive_total_price'),
            models.CheckConstraint(check=Q(client_id__isnull=False) | Q(store_id__isnull=False), 
                            name='valide_order'),
        ]


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

    def save(self, *args, **kwargs):
        print("this is State save")
        super().save(*args, **kwargs)


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

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(quantity__gte=1), name='item_positive_quantity'),
            models.CheckConstraint(check=Q(original_price__gte=1), name='item_positive_original_price'),
            models.CheckConstraint(check=Q(new_price__gte=0), name='item_positive_new_price'),
            models.CheckConstraint(check=Q(discount__gte=0) & Q(discount__lt=100), 
                                   name='item_correct_discount'),
        ]

# ################## 
class Cart(models.Model):

    client = models.OneToOneField(
        to="Client",
        on_delete=models.CASCADE,
        related_name="cart",
        related_query_name="cart",
    )

    # reverse relationships: [cartitem*]


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

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(quantity__gte=1), name='cart_positive_quantity'),
        ]

# ################## 
class Notification(models.Model):

    # User who recieves the notification (Client, Store)
    client = models.ForeignKey(
        to="Client",
        on_delete=models.CASCADE,
        null=True,
        related_name="notifications",
        related_query_name="notification",
    )

    store = models.ForeignKey(
        to="Store",
        on_delete=models.CASCADE,
        null=True,
        related_name="notifications",
        related_query_name="notification",
    )

    action = models.CharField(max_length=100, choices=actions, default="Created")
    message = models.TextField(default="")

    seen = models.BooleanField(default=False)
    created_at = models.IntegerField(default=get_now_stamp)

    # reverse relationships: []

    def __str__(self) -> str:
        return self.message
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(client_id__isnull=True) ^ Q(store_id__isnull=True), 
                name='valide_notification', 
                violation_error_message="both client and store are/aren't null"
            ),
        ]

# ################## 
class Advertisement(models.Model):

    store = models.ForeignKey(
        to="Store",
        on_delete=models.CASCADE,
        related_name="ads",
        related_query_name="ad",
    )
    
    product = models.ForeignKey(
        to="Product",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ads",
        related_query_name="ad",
    )

    type_choices = (("Store", "store"), ("Product", "product"))
    ad_type = models.CharField(max_length=100, choices=type_choices, default="Store")
    description = models.TextField()

    # reverse relationships: [image*]


class AdImage(models.Model):

    ad = models.ForeignKey(
        to="Advertisement",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="images",
        related_query_name="image",
    )
    url = models.CharField(max_length=1000, default="")


# fournisseur yban ghir a quelque clients