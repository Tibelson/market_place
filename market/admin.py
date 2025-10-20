from django.contrib import admin


from .models import (
    Vendor,
    Product,
    Order,
    Chat,
    Subscription,
)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Chat)
admin.site.register(Subscription)   