from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from item.models import Item
from django.shortcuts import get_object_or_404, redirect


@login_required
def new_conversation(request, item_pk):
    item  = get_object_or_404(Item, pk=item_pk)

    if item.sender == request.user:
        return redirect('item:detail', pk=item.pk)
        
    chat  = Chat.objects.filter(item=item).filter(members__in=[request.user.id])

    
