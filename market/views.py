from rest_framework import viewsets
from .models import Vendor, Order
from .serializers import (
    VendorSerializer,       
    OrderSerializer,
)
from django.shortcuts import render, redirect 
from django.contrib.auth import get_user_model
from item.models import Item, Category
from .forms import SignUpForm


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
            # Create user and populate extra fields not present on the default form
            User = get_user_model()
            user = form.save(commit=False)
            # Name input isn't part of the base UserCreation form fields, read from POST as fallback
            user.name = form.cleaned_data.get('name') or request.POST.get('name', '').strip()
            # Map frontend role values to model role choices
            role_choice = request.POST.get('role', 'customer')
            user.role = 'VENDORS' if role_choice == 'vendor' else 'customer'
            user.email = form.cleaned_data.get('email')
            user.save()

            # If vendor, create Vendor profile from extra fields
            if role_choice == 'vendor':
                store_name = request.POST.get('store_name', '').strip()
                phone = request.POST.get('phone', '').strip()
                location = request.POST.get('location', '').strip()
                if store_name:
                    Vendor.objects.create(user=user, store_name=store_name, email=user.email, phone=phone, location=location)

            # Redirect to namespaced login URL
            return redirect('market:login')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'market/signup.html', context)


# def login(request):
#     form = AuthenticationForm()

#     context = {'form': form}
#     return render(request, 'market/login.html', context)