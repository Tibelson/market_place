from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from django.contrib.auth.decorators import login_required
from .forms import ItemForm





def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    # Check subscription status for the current authenticated user
    is_subscribed = False
    try:
        from market.models import Subscription
        if request.user.is_authenticated:
            is_subscribed = Subscription.objects.filter(vendor=item.owner, user=request.user, is_active=True).exists()
    except Exception:
        # If the Subscription model isn't available for any reason, default to False
        is_subscribed = False

    context = {'item': item, 'is_subscribed': is_subscribed}

    return render(request, 'item/detail.html',context )

@login_required
def new_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            # set sold flag from form checkbox (checkbox sends value when checked)
            item.is_sold = bool(request.POST.get('is_sold'))
            # ensure owner is a Vendor linked to the logged-in user
            try:
                vendor = request.user.vendor
            except Exception:
                # create a vendor profile automatically if missing
                from market.models import Vendor
                vendor = Vendor.objects.create(user=request.user, store_name=(getattr(request.user, 'name', '') or request.user.username), email=getattr(request.user, 'email', ''))
            item.owner = vendor
            item.save()
            return redirect('item:detail', pk=item.pk)
    else:
        form = ItemForm()

    return render(request, 'item/item_form.html', {'form': form})
