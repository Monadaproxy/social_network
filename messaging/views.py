from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message, Conversation
from .forms import MessageForm
from users.models import User, Profile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')

    def get_other_user(conversation):
        return conversation.participants.exclude(id=request.user.id).first()

    for conv in conversations:
        conv.other_user = get_other_user(conv)
        conv.last_message = conv.messages.order_by('-timestamp').first()

    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(
        Conversation.objects.filter(participants=request.user),
        pk=pk
    )
    messages = conversation.messages.all().order_by('timestamp')

    Message.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            conversation.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{pk}',
                {
                    'type': 'chat_message',
                    'message': message.text,
                    'sender': request.user.username
                }
            )


    else:
        form = MessageForm()

    other_user = conversation.participants.exclude(id=request.user.id).first()

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form,
        'other_user': other_user,
        'ws_url': f"ws://{request.get_host()}/ws/conversation/{conversation.id}/"
    })





@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)

    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
        conversation.save()

    return redirect('messaging:conversation_detail', pk=conversation.pk)