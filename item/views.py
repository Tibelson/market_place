from django.shortcuts import render, get_object_or_404
from .models import Item
from django.contrib.auth.decorators import login_required
from .forms import ItemForm





def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    context = {'item':item}

    return render(request, 'item/detail.html',context )

@login_required
def new_item(request):
    form = ItemForm()

    return render(request, 'item/item_form.html', {'form': form})
