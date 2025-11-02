from rest_framework import routers
from django.urls import path, include
from .views import VendorViewSet, OrderViewSet, index, signup
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
    path('logout/', auth_view.LogoutView.as_view(next_page='/'), name='logout'),
    # path('', include(router.urls))

]