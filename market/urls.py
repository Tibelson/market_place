from rest_framework import routers
from django.urls import path, include
from .views import VendorViewSet, OrderViewSet, index, signup, subscribe_vendor, unsubscribe_vendor, logout_view
from django.contrib.auth import views as auth_view
from .forms import LoginForm


# router = routers.DefaultRouter()
# router.register(r'vendors', VendorViewSet)


# router.register(r'orders', OrderViewSet)
app_name = 'market'

urlpatterns = [
    path('',index,name='index'),
    path('signup/',signup,name='signup'),
    path('login/',auth_view.LoginView.as_view(template_name='market/login.html',authentication_form=LoginForm), name='login'),
    path('logout/', logout_view, name='logout'),
    path('vendor/<int:vendor_id>/subscribe/', subscribe_vendor, name='subscribe'),
    path('vendor/<int:vendor_id>/unsubscribe/', unsubscribe_vendor, name='unsubscribe'),
    # path('', include(router.urls))

]