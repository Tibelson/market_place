from rest_framework import routers
from django.urls import path, include
from .views import VendorViewSet, ProductViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls))
]