from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from item.models import Item
from .forms import MessageForm
from django.http import HttpResponseForbidden


@login_required
def chat_list(request):
    # Chats where the user is a member
    chats = Chat.objects.filter(members=request.user).order_by('-modified_at')
    return render(request, 'messaging/chat_list.html', {'chats': chats})


@login_required
def start_chat(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    # Determine vendor for the item
    vendor = item.owner
    # If vendor user is the same as requester, don't create a chat
    if hasattr(vendor, 'user') and vendor.user == request.user:
        return redirect('messaging:chat_list')

    # Find or create a chat for this item that includes both members
    chat_qs = Chat.objects.filter(item=item)
    chat = None
    for c in chat_qs:
        if request.user in c.members.all() and vendor.user in c.members.all():
            chat = c
            break

    if not chat:
        chat = Chat.objects.create(item=item)
        chat.members.add(request.user)
        if hasattr(vendor, 'user'):
            chat.members.add(vendor.user)
        chat.save()

    return redirect('messaging:chat_detail', chat_id=chat.pk)


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    if not chat.members.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden('You are not a member of this chat.')

    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        content = form.cleaned_data['content']
        message = Message.objects.create(chat=chat, sender=request.user, content=content)
        # touch chat to update modified_at
        chat.save()
        return redirect('messaging:chat_detail', chat_id=chat.pk)

    # Mark unread messages as read for this user (messages from others)
    chat.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    messages = chat.messages.select_related('sender').order_by('timestamp')
    return render(request, 'messaging/chat_detail.html', {'chat': chat, 'messages': messages, 'form': form})
