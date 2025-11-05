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
    """Subscribe the current user to a vendor. Only non-vendor users can subscribe.

    Creates Subscription if missing or re-activates it. By default notifications are enabled
    (muted=False)."""
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    # Disallow vendors from subscribing to other vendors (business rule)
    if hasattr(request.user, 'vendor'):
        return redirect(request.META.get('HTTP_REFERER') or 'market:index')

    sub, created = Subscription.objects.get_or_create(vendor=vendor, user=request.user)
    if not sub.is_active:
        sub.is_active = True
    # When creating, ensure notifications are enabled by default
    sub.muted = False
    sub.save()
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


@login_required
def toggle_mute_subscription(request, vendor_id):
    """Toggle the muted flag on the current user's subscription to a vendor."""
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    try:
        sub = Subscription.objects.get(vendor=vendor, user=request.user)
        sub.muted = not sub.muted
        sub.save()
    except Subscription.DoesNotExist:
        # If no subscription exists, create one muted=False then flip to muted True
        sub = Subscription.objects.create(vendor=vendor, user=request.user, is_active=True, muted=True)
    return redirect(request.META.get('HTTP_REFERER') or 'market:index')


def notifications_list(request):
    """Show notifications for the current user. Marks notifications as read on view."""
    if not request.user.is_authenticated:
        return redirect('market:login')
    notifications = request.user.notifications.all()
    # mark unread as read
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'market/notifications.html', {'notifications': notifications})


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