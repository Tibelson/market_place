from django.contrib import admin


from .models import (
    Vendor,
    Order,
    Subscription,
    User,
)
admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Order)
admin.site.register(Subscription)   