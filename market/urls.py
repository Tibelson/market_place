from rest_framework import routers
from django.urls import path, include
from .views import VendorViewSet, OrderViewSet, index, signup


# router = routers.DefaultRouter()
# router.register(r'vendors', VendorViewSet)


# router.register(r'orders', OrderViewSet)
app_name = 'market'

urlpatterns = [
    path('',index,name='index'),
    path('signup/ ',signup,name='signup'),
    # path('', include(router.urls))

]