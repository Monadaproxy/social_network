from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation
from .forms import MessageForm
from users.models import User


@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(
        Conversation.objects.filter(participants=request.user),
        pk=pk
    )
    messages = conversation.messages.all().order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            conversation.save()  # Обновляем updated_at
            return redirect('conversation_detail', pk=pk)
    else:
        form = MessageForm()

    other_user = conversation.participants.exclude(id=request.user.id).first()

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form,
        'other_user': other_user
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

    return redirect('conversation_detail', pk=conversation.pk)