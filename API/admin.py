from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(
    (
        Store,
        Client,
        Product,
        Coupon,
        Order,
        OrderCoupon,
        OrderItem,
        Group,
        Category,
        PackType,
    )
)
