from rest_framework import routers
from django.urls import path, include
from .views import VendorViewSet, OrderViewSet, index


router = routers.DefaultRouter()
router.register(r'vendors', VendorViewSet)


router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('',index,name='index'),
    # path('', include(router.urls))

]