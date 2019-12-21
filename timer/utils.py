from django.utils import timezone

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


def calculate_pause_time(timer):
    if timer.pause_duration_total is not None:
        timer.pause_duration_total += timezone.now() - timer.pause_start_time
    else:
        timer.pause_duration_total = timezone.now() - timer.pause_start_time
    return timer

