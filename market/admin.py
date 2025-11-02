from django.contrib import admin


from .models import (
    Vendor,
    Order,
    Chat,
    Subscription,
    User,
)
admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Order)
admin.site.register(Chat)
admin.site.register(Subscription)   