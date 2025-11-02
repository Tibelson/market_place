from rest_framework import viewsets
from .models import Vendor, Order
from .serializers import (
    VendorSerializer,       
    OrderSerializer,
)
from django.shortcuts import render, redirect 
from item.models import Item, Category
from .forms import SignUpForm, AuthenticationForm


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories

    }

    return render(request, 'market/index.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'market/signup.html', context)


# def login(request):
#     form = AuthenticationForm()

#     context = {'form': form}
#     return render(request, 'market/login.html', context)