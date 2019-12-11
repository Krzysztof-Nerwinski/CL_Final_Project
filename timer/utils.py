from django.db.models import Q
from timer.models import Timer


def user_has_active_timer(request):
    try:
        timer = Timer.objects.get(Q(employee_id=request.user.id) &
                                  Q(is_active=True))
    except Timer.DoesNotExist:
        timer = None
    except Timer.MultipleObjectsReturned:
        raise Exception('Many active timers for one user. Contact administrator')
    return timer
