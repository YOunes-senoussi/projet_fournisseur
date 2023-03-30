from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(
    (
        Store,
        Client,
        Group,
        Product,
        Category,
        PackType,
        Coupon,
        CouponClient,
        Order,
        OrderState,
        OrderCoupon,
        OrderProduct,
        ClientProduct,
        StoreNotification,
        ClientNotification,
        Advertisement,
        AdImage,
    )
)
