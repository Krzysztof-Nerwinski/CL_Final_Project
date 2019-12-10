from django.db.models import Q
from timer.models import Timer


def user_has_active_timer(request):
    try:
        timer = Timer.objects.get(Q(employee=request.user) & Q(is_active=True))
    except Timer.DoesNotExist:
        timer = None
    return timer