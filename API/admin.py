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
        CouponCount,
        Order,
        OrderState,
        OrderCoupon,
        OrderItem,
        Cart,
        CartItem,
        Notification,
        Advertisement,
        AdImage,
    )
)
