from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Message

@shared_task
def send_notification(user_id, message_id):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    User = get_user_model()
    user = User.objects.get(id=user_id)
    message = Message.objects.get(id=message_id)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "notification.message",
            "text": f"Новое сообщение: {message.text}",
            "unread_count": Message.objects.filter(receiver=user, is_read=False).count(),
        }
    )