from rest_framework import viewsets
from .models import Vendor, Order, Subscription
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .serializers import (
    VendorSerializer,       
    OrderSerializer,
)
from django.shortcuts import render, redirect 
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
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


@login_required
def subscribe_vendor(request, vendor_id):
    """Subscribe the current user to a vendor. Creates Subscription if missing or re-activates it."""
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    sub, created = Subscription.objects.get_or_create(vendor=vendor, user=request.user)
    if not sub.is_active:
        sub.is_active = True
        sub.save()
    # redirect back to referring page or vendor/home
    return redirect(request.META.get('HTTP_REFERER') or 'market:index')


@login_required
def unsubscribe_vendor(request, vendor_id):
    """Deactivate an existing subscription if present."""
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    try:
        sub = Subscription.objects.get(vendor=vendor, user=request.user)
        sub.is_active = False
        sub.save()
    except Subscription.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER') or 'market:index')


def logout_view(request):
    """Log out the current user and redirect to the site index.

    Uses django.contrib.auth.logout which flushes the session. This ensures
    the session is cleared and the user becomes anonymous on the next request.
    """
    logout(request)
    return redirect('market:index')


# def login(request):
#     form = AuthenticationForm()

#     context = {'form': form}
#     return render(request, 'market/login.html', context)