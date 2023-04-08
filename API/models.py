from django.db import models
from django.core.exceptions import FieldError
from django.contrib.auth.models import User
from API.some_functions import *
from itertools import chain

from projet_fournisseur.settings import (
    DEFAULT_STORE_IMG_PATH, DEFAULT_CLIENT_IMG_PATH, 
    DEFAULT_PRODUCT_IMG_PATH, DEFAULT_CATEGORY_IMG_PATH, DEFAULT_AD_IMG_PATH
)
# ################## 

# choices
coupon_types = (
    ("product", "product"),
    ("category", "category"),
    ("all", "all"),
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
    dir_path = models.CharField(max_length=100, default="")

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    account = models.OneToOneField(to=User, null=True, on_delete=models.SET_NULL, related_name="store")

    # many to many relationship
    fav_clients = models.ManyToManyField(to="Client", through="StoreFavClient")

    # reverse relationships: [group*, coupon*, order*, product*, notification*, ad*]

    # ###############
    fields_to_update = [
        "store_name", "full_name", "phone_number", "password", "e_mail", 
        "wilaya", "commune", "address", "latitude", "longitude"
    ]

    to_dict_fields = [
        "id", "store_name", "full_name", "image_url", "phone_number", "password", "e_mail", 
        "wilaya", "commune", "address", "created_at", "dir_path", "latitude", "longitude"
    ]
    # ###############

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['store_name'], name='unique_store_name'),
            models.UniqueConstraint(fields=['phone_number'], name='unique_store_phone_numbre'),
        ]
    
    def __str__(self):
        return f"Store_{self.id}: {self.store_name}"
    
    @classmethod
    def create(cls, *args, **kwargs):
        
        img = kwargs.pop("image", "default")

        if img =="default":
            store = cls(**kwargs)
            store.save()
            store.refresh_from_db()

            store.dir_path = f"static/stores/store_{store.id}"
            store.image_url = f"{store.dir_path}/store_{store.id}"
            store.save()
            store.refresh_from_db()

            pathlib.Path(store.dir_path).mkdir(exist_ok=True)
            store.image_url = copy_image(source_path=DEFAULT_STORE_IMG_PATH, destination_path=store.image_url)

        else:
            img = img.split(",")[-1]
            image = decode_image(img)

            store = cls(**kwargs)
            store.save()
            store.refresh_from_db()

            store.dir_path = f"static/stores/store_{store.id}"
            store.image_url = f"{store.dir_path}/store_{store.id}.{image.format}"
            store.save()
            store.refresh_from_db()

            pathlib.Path(store.dir_path).mkdir(exist_ok=True)
            image.save(store.image_url)

        store.save()
        store.refresh_from_db()

        # creating an account
        store.account = User.objects.create_user(username=store.phone_number, password=store.password)
        store.save()
        store.refresh_from_db()
        
        return store
    
    def update(self, *args, **kwargs):

        if "image" in kwargs:
            img = kwargs["image"]

            if img=="default":
                self.update_fields(*args, **kwargs)
                
                delete_img(self.image_url)
                img_path = f"{self.dir_path}/store_{self.id}"
                img_path = copy_image(source_path=DEFAULT_STORE_IMG_PATH, destination_path=img_path)

            else:
                img = img.split(",")[-1]
                image = decode_image(img)

                self.update_fields(*args, **kwargs)
                
                delete_img(self.image_url)
                img_path = f"{self.dir_path}/store_{self.id}.{image.format}"
                image.save(img_path)

            self.image_url = img_path
            self.save()
            self.refresh_from_db()

        else:
            self.update_fields(*args, **kwargs)

        # updating the account
        self.account.username = self.phone_number
        self.account.set_password(self.password)
        self.account.save()

        self.save()
        self.refresh_from_db()

        return self

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


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
    dir_path = models.CharField(max_length=100, default="")

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    account = models.OneToOneField(to=User, null=True, on_delete=models.SET_NULL, related_name="client")

    # many to many relationship
    fav_stores = models.ManyToManyField(to="Store", through="ClientFavStore")

    # reverse relationships: [couponclient*, order*, notification*]

    # ###############
    fields_to_update = [
        "shop_name", "full_name", "phone_number", "password", "e_mail", 
        "wilaya", "commune", "address", "latitude", "longitude"
    ]

    to_dict_fields = [
        "id", "shop_name", "full_name", "image_url", "phone_number", "password", "e_mail", 
        "wilaya", "commune", "address", "created_at", "dir_path", "latitude", "longitude"
    ]
    # ###############

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['shop_name'], name='unique_shop_name'),
            models.UniqueConstraint(fields=['phone_number'], name='unique_shop_phone_numbre'),
        ]

    def __str__(self):
        return f"({self.id})Shop: {self.shop_name} ({self.full_name})" 
    
    
    @classmethod
    def create(cls, *args, **kwargs):
        
        img = kwargs.pop("image", "default")

        if img =="default":
            client = cls(**kwargs)
            client.save()
            client.refresh_from_db()

            client.dir_path = f"static/clients/client_{client.id}"
            client.image_url = f"{client.dir_path}/client_{client.id}"
            client.save()
            client.refresh_from_db()

            pathlib.Path(client.dir_path).mkdir(exist_ok=True)
            client.image_url = copy_image(source_path=DEFAULT_CLIENT_IMG_PATH, destination_path=client.image_url)

        else:
            img = img.split(",")[-1]
            image = decode_image(img)

            client = cls(**kwargs)
            client.save()
            client.refresh_from_db()

            client.dir_path = f"static/clients/client_{client.id}"
            client.image_url = f"{client.dir_path}/client_{client.id}.{image.format}"
            client.save()
            client.refresh_from_db()
            
            pathlib.Path(client.dir_path).mkdir(exist_ok=True)
            image.save(client.image_url)

        client.save()
        client.refresh_from_db()

        # creating an account
        client.account = User.objects.create_user(username=client.phone_number, password=client.password)
        client.save()
        client.refresh_from_db()
        
        return client

    def update(self, *args, **kwargs):

        if "image" in kwargs:
            img = kwargs["image"]

            if img=="default":
                self.update_fields(*args, **kwargs)
                
                delete_img(self.image_url)
                img_path = f"{self.dir_path}/client_{self.id}"
                img_path = copy_image(source_path=DEFAULT_CLIENT_IMG_PATH, destination_path=img_path)

            else:
                img = img.split(",")[-1]
                image = decode_image(img)
                
                self.update_fields(*args, **kwargs)
                
                delete_img(self.image_url)
                img_path = f"{self.dir_path}/client_{self.id}.{image.format}"
                image.save(img_path)

            self.image_url = img_path
            self.save()
            self.refresh_from_db()
        else:
            self.update_fields(*args, **kwargs)

        # updating the account
        self.account.username = self.phone_number
        self.account.set_password(self.password)
        self.account.save()

        self.save()
        self.refresh_from_db()

        return self

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


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
    clients = models.ManyToManyField(to="Client", through="GroupClient")

    # reverse relationships: []

    # ###############
    fields_to_update = [
        "name"
    ]

    to_dict_fields = [
        "id", "name", "store_id", "created_at"
    ]
    # ###############

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'store_id'], name='unique_group_name'),
        ]

    def __str__(self):
        return f"id:{self.id} store:{self.store_id}"

    @classmethod
    def create(cls, *args, **kwargs):
        
        group = cls(**kwargs)
        group.save()
        group.refresh_from_db()

        return group

    def update(self, *args, **kwargs):

        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


# Intermediary (simple)
class GroupClient(models.Model):

    group = models.ForeignKey(
        to="Group",
        on_delete=models.CASCADE,
        related_name="groupclients",
        related_query_name="groupclient",
    )

    client = models.ForeignKey(
        to="Client",
        on_delete=models.CASCADE,
        related_name="groupclients",
        related_query_name="groupclient",
    )

    # reverse relationships: []

    # ###############
    fields_to_update = [
        "group_id", "client_id"
    ]

    to_dict_fields = [
        "id", "group_id", "client_id"
    ]
    # ###############

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group_id', 'client_id'], name='unique_group_client'),
        ]

    @classmethod
    def create(cls, *args, **kwargs):
        
        group_client = cls(**kwargs)
        group_client.save()
        group_client.refresh_from_db()

        return group_client

    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


# Intermediary (simple)
class StoreFavClient(models.Model):

    store = models.ForeignKey(
        to="Store",
        on_delete=models.CASCADE,
        related_name="storefavclients",
        related_query_name="storefavclient",
    )

    client = models.ForeignKey(to="Client", on_delete=models.CASCADE)

    # reverse relationships: []

    # ###############
    fields_to_update = [
        "store_id", "client_id"
    ]

    to_dict_fields = [
        "id", "store_id", "client_id"
    ]
    # ###############

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['store_id', 'client_id'], name='unique_store_client'),
        ]

    @classmethod
    def create(cls, *args, **kwargs):
        
        fav_client = cls(**kwargs)
        fav_client.save()
        fav_client.refresh_from_db()

        return fav_client

    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


# Intermediary (simple)
class ClientFavStore(models.Model):

    client = models.ForeignKey(
        to="Client",
        on_delete=models.CASCADE,
        related_name="clientfavstores",
        related_query_name="clientfavstore",
    )

    store = models.ForeignKey(to="Store", on_delete=models.CASCADE)

    # reverse relationships: []

    # ###############
    fields_to_update = [
        "client_id", "store_id",
    ]

    to_dict_fields = [
        "id", "client_id", "store_id"
    ]
    # ###############

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client_id', 'store_id'], name='unique_client_store'),
        ]

    @classmethod
    def create(cls, *args, **kwargs):
        
        fav_store = cls(**kwargs)
        fav_store.save()
        fav_store.refresh_from_db()

        return fav_store

    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


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
    dir_path = models.CharField(max_length=100, default="")

    # reverse relationships: [orderproducts*, cartproduct*, ad*]

    # ###############
    fields_to_update = [
        "name", "brand", "price", "category_id", "pack_type_id", 
        "description", "nbr_units", "discount", "is_available"
    ]

    to_dict_fields = [
        "id", "name", "brand", "price", "image_url", "store_id", "category_id", "pack_type_id", 
        "description", "nbr_units", "discount", "is_available", "created_at", "dir_path"
    ]
    # ###############

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
    
    @classmethod
    def create(cls, *args, **kwargs):
        
        img = kwargs.pop("image", "default")

        if img =="default":
            product = cls(**kwargs)
            product.save()
            product.refresh_from_db()

            product.dir_path = f"static/products/product_{product.id}"
            product.image_url = f"{product.dir_path}/product_{product.id}"
            product.save()
            product.refresh_from_db()
            
            pathlib.Path(product.dir_path).mkdir(exist_ok=True)
            product.image_url = copy_image(source_path=DEFAULT_PRODUCT_IMG_PATH, destination_path=product.image_url)

        else:
            img = img.split(",")[-1]
            image = decode_image(img)

            product = cls(**kwargs)
            product.save()
            product.refresh_from_db()

            product.dir_path = f"static/products/product_{product.id}"
            product.image_url = f"{product.dir_path}/product_{product.id}.{image.format}"
            product.save()
            product.refresh_from_db()

            pathlib.Path(product.dir_path).mkdir(exist_ok=True)
            image.save(product.image_url)

        product.save()
        product.refresh_from_db()

        return product
        
    def update(self, *args, **kwargs):
        
        if "image" in kwargs:
            img = kwargs["image"]

            if img=="default":
                self.update_fields(*args, **kwargs)
                
                delete_img(self.image_url)
                
                img_path = f"{self.dir_path}/product_{self.id}"
                img_path = copy_image(source_path=DEFAULT_PRODUCT_IMG_PATH, destination_path=img_path)

            else:
                img = img.split(",")[-1]
                image = decode_image(img)
                
                self.update_fields(*args, **kwargs)
                
                delete_img(self.image_url)
                img_path = f"{self.dir_path}/product_{self.id}.{image.format}"
                image.save(img_path)

            self.image_url = img_path
            self.save()
            self.refresh_from_db()

        else:
            self.update_fields(*args, **kwargs)

        return self
    
    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


class Category(models.Model):
    
    name = models.CharField(max_length=100, default="")
    image_url = models.CharField(max_length=100, default="")
    dir_path = models.CharField(max_length=100, default="")

    # reverse relationships: [product*]

    # ###############
    fields_to_update = [
        "name"
    ]

    to_dict_fields = [
        "id", "name", "image_url", "dir_path"
    ]
    # ###############

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name'),
        ]

    def __str__(self):
        return f"{self.name}"
    
    @classmethod
    def create(cls, *args, **kwargs):
        
        img = kwargs.pop("image", "default")

        if img =="default":
            category = cls(**kwargs)
            category.save()
            category.refresh_from_db()

            category.dir_path = f"static/categories/category_{category.id}"
            category.image_url = f"{category.dir_path}/category_{category.id}"
            category.save()
            category.refresh_from_db()
            
            pathlib.Path(category.dir_path).mkdir(exist_ok=True)
            category.image_url = copy_image(source_path=DEFAULT_CATEGORY_IMG_PATH, destination_path=category.image_url)

        else:
            img = img.split(",")[-1]
            image = decode_image(img)

            category = cls(**kwargs)
            category.save()
            category.refresh_from_db()

            category.dir_path = f"static/categories/category_{category.id}"
            category.image_url = f"{category.dir_path}/category_{category.id}.{image.format}"
            category.save()
            category.refresh_from_db()

            pathlib.Path(category.dir_path).mkdir(exist_ok=True)
            image.save(category.image_url)

        category.save()
        category.refresh_from_db()
        return category
    
    def update(self, *args, **kwargs):

        if "image" in kwargs:
            img = kwargs["image"]

            if img=="default":
                self.update_fields(*args, **kwargs)
                
                delete_img(self.image_url)
                img_path = f"{self.dir_path}/category_{self.id}"
                img_path = copy_image(source_path=DEFAULT_CATEGORY_IMG_PATH, destination_path=img_path)

            else:
                img = img.split(",")[-1]
                image = decode_image(img)
                
                self.update_fields(*args, **kwargs)
                
                delete_img(self.image_url)
                img_path = f"{self.dir_path}/category_{self.id}.{image.format}"
                image.save(img_path)

            self.image_url = img_path
            self.save()
            self.refresh_from_db()

        else:
            self.update_fields(*args, **kwargs)

        return self
    
    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


class PackType(models.Model):
    
    name = models.CharField(max_length=100, default="")

    # reverse relationships: [product*]

    # ###############
    fields_to_update = [
        "name"
    ]

    to_dict_fields = [
        "id", "name"
    ]
    # ###############

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_pack_type_name'),
        ]

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def create(cls, *args, **kwargs):
        
        pack_type = cls(**kwargs)
        pack_type.save()
        pack_type.refresh_from_db()

        return pack_type

    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


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

    coupon_type = models.CharField(max_length=100, choices=coupon_types, default="all")
    target_id = models.IntegerField(null=True, blank=True, default=None)

    max_nbr_uses = models.IntegerField(default=1)
    created_at = models.IntegerField(default=get_now_stamp)
    is_active = models.BooleanField(default=True)

    clients = models.ManyToManyField(to="Client", through="CouponClient")

    # reverse relationships: [couponclient*, ordercoupon*]

    # ###############
    fields_to_update = [
        "string", "discount", "coupon_type", 
        "target_id", "max_nbr_uses", "is_active"
    ]

    to_dict_fields = [
        "id", "string", "discount", "store_id", "coupon_type", 
        "target_id", "max_nbr_uses", "created_at", "is_active"
    ]
    # ###############

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['string', 'store_id'], name='unique_coupon'),
            models.CheckConstraint(check=Q(max_nbr_uses__gte=1), name='positive_max_nbr_uses'),
            models.CheckConstraint(check=Q(discount__gte=1) & Q(discount__lte=100), 
                                   name='correct_coupon_discount'),
        ]

    def __str__(self):
        return f"{self.string} => {self.coupon_type} ({self.discount}%)"

    @classmethod
    def create(cls, *args, **kwargs):
        
        coupon = cls(**kwargs)
        coupon.save()
        coupon.refresh_from_db()

        return coupon

    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


# Intermediary
class CouponClient(models.Model):

    client = models.ForeignKey(
        to="Client",
        on_delete=models.CASCADE,
        related_name="couponclients",
        related_query_name="couponclient",
    )

    coupon = models.ForeignKey(
        to="Coupon",
        on_delete=models.CASCADE,
        related_name="couponclients",
        related_query_name="couponclient",
    )

    count = models.IntegerField(default=1)

    # reverse relationships: []

    # ###############
    fields_to_update = [
        "client_id", "coupon_id", "count"
    ]

    to_dict_fields = [
        "id", "client_id", "coupon_id", "count"
    ]
    # ###############

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client_id', 'coupon_id'], name='unique_client_coupon'),
            models.CheckConstraint(check=Q(count__gte=0), name='coupon_positive_count'),
        ]

    @classmethod
    def create(cls, *args, **kwargs):
        
        coupon_client = cls(**kwargs)
        coupon_client.save()
        coupon_client.refresh_from_db()

        return coupon_client

    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


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
    
    current_state = models.ForeignKey(
        to="OrderState",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_orders",
        related_query_name="current_order",
    )

    created_at = models.IntegerField(default=get_now_stamp)
    total_price = models.FloatField(default=1.0)

    coupons = models.ManyToManyField(to="Coupon", through="OrderCoupon")
    products = models.ManyToManyField(to="Product", through="OrderProduct")

    archived_by_store = models.BooleanField(default=False)
    archived_by_client = models.BooleanField(default=False)

    # reverse relationships: [orderstate*, ordercoupon*, orderproduct*]

    # ###############
    fields_to_update = [
        "current_state_id", "total_price", "archived_by_store", "archived_by_client"
    ]

    to_dict_fields = [
        "id", "store_id", "client_id", "current_state_id", "created_at",
        "total_price", "archived_by_store", "archived_by_client"
    ]
    # ###############

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(total_price__gte=1), name='order_positive_total_price'),
            models.CheckConstraint(check=Q(client_id__isnull=False) | Q(store_id__isnull=False), 
                            name='valide_order'),
        ]

    @classmethod
    def create(cls, *args, **kwargs):

        order = cls(**kwargs)
        order.save()
        order.refresh_from_db()

        return order

    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


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
    updated_by_store = models.BooleanField(default=True)

    # reverse relationships: []

    # ###############
    fields_to_update = [
        "state", "description",
    ]

    to_dict_fields = [
        "id", "order_id", "state", "description", "time_stamp", "updated_by_store",
    ]
    # ###############

    class Meta:
        constraints = []

    def __str__(self):
        return f"{self.order}: {self.state}"

    @classmethod
    def create(cls, *args, **kwargs):
        
        order_state = cls(**kwargs)
        order_state.save()
        order_state.refresh_from_db()

        return order_state
    
    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


# Intermediary (simple)
class OrderCoupon(models.Model):

    order = models.ForeignKey(
        to="Order",
        on_delete=models.CASCADE,
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

    # ###############
    fields_to_update = []

    to_dict_fields = [
        "id", "order_id", "coupon_id"
    ]
    # ###############

    class Meta:
        constraints = []

    @classmethod
    def create(cls, *args, **kwargs):
        
        order_coupon = cls(**kwargs)
        order_coupon.save()
        order_coupon.refresh_from_db()

        return order_coupon
    
    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


# Intermediary
class OrderProduct(models.Model):

    order = models.ForeignKey(
        to="Order",
        on_delete=models.CASCADE,
        related_name="orderproducts",
        related_query_name="orderproduct",
    )
    product = models.ForeignKey(
        to="Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orderproducts",
        related_query_name="orderproduct",
    )

    quantity = models.IntegerField(default=1)
    discount = models.IntegerField(default=0)
    original_price = models.FloatField()
    new_price = models.FloatField()

    # reverse relationships: []

    # ###############
    fields_to_update = [
        "quantity", "discount", "original_price", "new_price"
    ]

    to_dict_fields = [
        "id", "order_id", "product_id", "quantity", "discount", "original_price", "new_price"
    ]
    # ###############

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(quantity__gte=1), name='product_positive_quantity'),
            models.CheckConstraint(check=Q(original_price__gte=1), name='product_positive_original_price'),
            models.CheckConstraint(check=Q(new_price__gte=0), name='product_positive_new_price'),
            models.CheckConstraint(check=Q(discount__gte=0) & Q(discount__lt=100), 
                                   name='product_correct_discount'),
        ]

    @classmethod
    def create(cls, *args, **kwargs):
        
        order_product = cls(**kwargs)
        order_product.save()
        order_product.refresh_from_db()

        return order_product
    
    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))

    @classmethod
    def validate(cls, **kwargs):

        if not Product.objects.filter(pk=kwargs["product_id"]).exists():
            raise FieldError(f"product: {kwargs['product_id']} does not exist")
        
        if kwargs["quantity"] <= 0:
            raise FieldError(f"quantity: {kwargs['quantity']} is negative")
        
        if kwargs["original_price"] <= 0:
            raise FieldError(f"original_price: {kwargs['original_price']} is negative")
        
        if kwargs["new_price"] <= 0:
            raise FieldError(f"new_price: {kwargs['new_price']} is negative")
        
        if kwargs["discount"] < 0 or kwargs["discount"] > 100:
            raise FieldError(f"discount: {kwargs['discount']} is out of range [0, 100]")
        
        return True


# ################## 
# Intermediary
class ClientProduct(models.Model):

    client = models.ForeignKey(
        to="Client",
        on_delete=models.CASCADE,
        related_name="clientproducts",
        related_query_name="clientproduct",
    )

    product = models.ForeignKey(
        to="Product",
        on_delete=models.CASCADE,
        related_name="clientproducts",
        related_query_name="clientproduct",
    )

    quantity = models.IntegerField(default=1)

    # reverse relationships: []

    # ###############
    fields_to_update = [
        "quantity"
    ]

    to_dict_fields = [
        "id", "client_id", "product_id", "quantity"
    ]
    # ###############

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(quantity__gte=1), name='cart_positive_quantity'),
        ]

    @classmethod
    def create(cls, *args, **kwargs):
        
        cart_product = cls(**kwargs)
        cart_product.save()
        cart_product.refresh_from_db()

        return cart_product
    
    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


# ################## 
class StoreNotification(models.Model):

    store = models.ForeignKey(
        to="Store",
        on_delete=models.CASCADE,
        related_name="notifications",
        related_query_name="notification",
    )

    action = models.CharField(max_length=100, choices=actions, default="Created")
    message = models.TextField(default="")

    seen = models.BooleanField(default=False)
    created_at = models.IntegerField(default=get_now_stamp)

    # reverse relationships: []

    # ###############
    fields_to_update = [
        "seen"
    ]

    to_dict_fields = [
        "id", "store_id", "action", "message", "seen", "created_at"
    ]
    # ###############
    
    class Meta:
        constraints = []

    def __str__(self) -> str:
        return self.message

    @classmethod
    def create(cls, *args, **kwargs):
        
        notification = cls(**kwargs)
        notification.save()
        notification.refresh_from_db()

        return notification
    
    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


class ClientNotification(models.Model):

    client = models.ForeignKey(
        to="Client",
        on_delete=models.CASCADE,
        related_name="notifications",
        related_query_name="notification",
    )

    action = models.CharField(max_length=100, choices=actions, default="Created")
    message = models.TextField(default="")

    seen = models.BooleanField(default=False)
    created_at = models.IntegerField(default=get_now_stamp)

    # reverse relationships: []

    # ###############
    fields_to_update = [
        "seen"
    ]

    to_dict_fields = [
        "id", "client_id", "action", "message", "seen", "created_at"
    ]
    # ###############
    
    class Meta:
        constraints = []

    def __str__(self) -> str:
        return self.message

    @classmethod
    def create(cls, *args, **kwargs):
        
        notification = cls(**kwargs)
        notification.save()
        notification.refresh_from_db()

        return notification
    
    def update(self, *args, **kwargs):

        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


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

    created_at = models.IntegerField(default=get_now_stamp)
    dir_path = models.CharField(max_length=100, default="")
    
    # reverse relationships: [image*]

    # ###############
    fields_to_update = [
        "description"
    ]

    to_dict_fields = [
        "id", "store_id", "product_id", "ad_type", "description", "created_at", "dir_path"
    ]
    # ###############
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(product_id__isnull=False, ad_type__iexact="product"), 
                name='valide_ad', 
            ),
        ]

    @classmethod
    def create(cls, *args, **kwargs):
        
        ad = cls(**kwargs)
        ad.save()
        ad.refresh_from_db()

        ad.dir_path = f"static/ads/ad_{ad.id}"
        ad.save()
        ad.refresh_from_db()
        
        pathlib.Path(ad.dir_path).mkdir(exist_ok=True)

        return ad

    def update(self, *args, **kwargs):
        
        return self.update_fields(*args, **kwargs)

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


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
    
    # ###############
    fields_to_update = [
        "ad_id", "url"
    ]

    to_dict_fields = [
        "id", "ad_id", "url"
    ]
    # ###############

    class Meta:
        constraints = []

    @classmethod
    def create(cls, *args, **kwargs):
        
        img = kwargs.pop("image", "default")

        if img =="default":
            ad_image = cls(**kwargs)
            ad_image.save()
            ad_image.refresh_from_db()

            ad_image.url = f"{ad_image.ad.dir_path}/ad_image_{ad_image.id}"
            ad_image.save()
            ad_image.refresh_from_db()
            
            ad_image.url = copy_image(source_path=DEFAULT_AD_IMG_PATH, destination_path=ad_image.url)

        else:
            img = img.split(",")[-1]
            image = decode_image(img)
            
            ad_image = cls(**kwargs)
            ad_image.save()
            ad_image.refresh_from_db()
            
            ad_image.url = f"{ad_image.ad.dir_path}/ad_image_{ad_image.id}.{image.format}"
            ad_image.save()
            ad_image.refresh_from_db()
            
            image.save(ad_image.url)

        ad_image.save()
        ad_image.refresh_from_db()

        return ad_image
    
    def update(self, *args, **kwargs):
        
        if "image" in kwargs:
            img = kwargs["image"]

            if img=="default":
                self.update_fields(*args, **kwargs)
                
                delete_img(self.image_url)
                img_path = f"{self.dir_path}/ad_image_{self.id}"
                img_path = copy_image(source_path=DEFAULT_AD_IMG_PATH, destination_path=img_path)

            else:
                img = img.split(",")[-1]
                image = decode_image(img)
                
                self.update_fields(*args, **kwargs)
                
                delete_img(self.image_url)
                img_path = f"{self.dir_path}/ad_image_{self.id}.{image.format}"
                image.save(img_path)

            self.image_url = img_path
            self.save()
            self.refresh_from_db()

        else:
            self.update_fields(*args, **kwargs)

        return self

    def update_fields(self, *args, **kwargs):

        for field, value in kwargs.items():
            if field in self.fields_to_update:
                setattr(self, field, value)

        self.save()
        self.refresh_from_db()

        return self

    def to_dict(self):
        return dict(list(map(lambda field: [field, getattr(self, field, None)], self.to_dict_fields)))


# ################## 


