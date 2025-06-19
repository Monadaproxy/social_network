from .models import Friendship

def friendship_requests(request):
    if request.user.is_authenticated:
        return {
            'pending_requests_count': Friendship.objects.filter(
                to_user=request.user,
                status=Friendship.PENDING
            ).count()
        }
    return {}