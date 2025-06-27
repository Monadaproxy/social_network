from .models import Conversation, Message


def unread_messages(request):
    if not request.user.is_authenticated:
        return {}

    conversations = Conversation.objects.filter(participants=request.user)

    unread_messages_count = Message.objects.filter(
        conversation__in=conversations,
        is_read=False
    ).exclude(sender=request.user).count()

    return {
        'unread_messages_count': unread_messages_count
    }