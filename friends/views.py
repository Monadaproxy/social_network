from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Friendship, User
from .forms import FriendRequestActionForm


@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, pk=user_id)

    if Friendship.objects.filter(from_user=request.user, to_user=to_user).exists():
        messages.warning(request, 'Запрос уже отправлен')
    elif Friendship.objects.filter(from_user=to_user, to_user=request.user).exists():
        messages.warning(request, 'Этот пользователь уже отправил вам запрос')
    else:
        Friendship.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, 'Запрос дружбы отправлен')

    return redirect('users:profile', username=to_user.username)


@login_required
def handle_friend_request(request, request_id):
    friendship = get_object_or_404(Friendship, pk=request_id, to_user=request.user)

    if request.method == 'POST':
        form = FriendRequestActionForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']

            if action == 'accept':
                friendship.status = Friendship.ACCEPTED
                messages.success(request, 'Запрос дружбы принят')
            else:
                friendship.status = Friendship.REJECTED
                messages.info(request, 'Запрос дружбы отклонен')

            friendship.save()

    return redirect('friends:friendship_requests')


@login_required
def friend_list(request):
    friends = User.objects.filter(
        Q(friendship_requests_received__from_user=request.user,
          friendship_requests_received__status=Friendship.ACCEPTED) |
        Q(friendship_requests_sent__to_user=request.user, friendship_requests_sent__status=Friendship.ACCEPTED)
    ).distinct()

    received_requests = Friendship.objects.filter(
        to_user=request.user,
        status=Friendship.PENDING
    ).select_related('from_user')

    return render(request, 'friends/friend_list.html', {'friends': friends, 'received_requests' : received_requests})


@login_required
def friendship_requests(request):
    received_requests = Friendship.objects.filter(
        to_user=request.user,
        status=Friendship.PENDING
    ).select_related('from_user')

    return render(request, 'friends/requests.html', {'received_requests': received_requests})