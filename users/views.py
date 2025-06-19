from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from .forms import LoginUserForm, RegisterUserForm, ProfileUpdateForm, AvatarUploadForm
from django.contrib.auth.models import User
from .models import Profile
from news.models import Articles
from friends.models import Friendship
from django.db.models import Q

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = '/users/login/'

    def get_user_context(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items() + list(c_def.items())))


@login_required
def profile_edit(request, username):
    try:
        profile = request.user.profile
    except Exception:
        Profile.objects.create(user=request.user)
        profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile', username=username)
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'users/profile_edit.html', {'form' : form})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    try:
        profile = request.user.profile
    except Exception:
        Profile.objects.create(user=request.user)
        profile = request.user.profile
    is_owner = request.user == user
    news = Articles.objects.filter(author=user).order_by('-date')
    friends = User.objects.filter(
        Q(friendship_requests_received__from_user=request.user,
          friendship_requests_received__status=Friendship.ACCEPTED) |
        Q(friendship_requests_sent__to_user=request.user, friendship_requests_sent__status=Friendship.ACCEPTED)
    ).distinct()

    friendship_status = {
        'request_sent': Friendship.objects.filter(
            from_user=request.user,
            to_user=user,
            status=Friendship.PENDING
        ).exists(),
        'request_received': Friendship.objects.filter(
            from_user=user,
            to_user=request.user,
            status=Friendship.PENDING
        ).exists(),
        'is_friend': Friendship.objects.filter(
            Q(from_user=request.user, to_user=user, status=Friendship.ACCEPTED) |
            Q(from_user=user, to_user=request.user, status=Friendship.ACCEPTED)
        ).exists()
    }

    context = {
        'profile_user': user,
        'profile': profile,
        'is_owner': is_owner,
        'news': news,
        'friends': friends,
        'friendship_status': friendship_status,
    }

    return render(request, 'users/profile.html', context)

@login_required
def upload_avatar(request):
    try:
        profile = request.user.profile
    except Exception:
        Profile.objects.create(user=request.user)
        profile = request.user.profile
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = AvatarUploadForm(instance=profile)

    return render(request, 'users/profile.html', {'avatar_form' : form })
