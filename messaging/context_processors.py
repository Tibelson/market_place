from django.db.models import Q
from .models import Message


def unread_message_count(request):
    """Return the number of unread messages for the current user.

    Only counts messages that are unread and where the current user is a member
    of the chat and the message sender is not the current user.
    """
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return {'unread_message_count': 0}

    count = Message.objects.filter(is_read=False, chat__members=user).exclude(sender=user).count()
    return {'unread_message_count': count}
