from django import template

register = template.Library()


@register.filter(name='change_timedelta_format')
def smooth_timedelta(timedeltaobj):
    """Convert a datetime.durationfield object into Days, Hours, Minutes, Seconds."""
    secs = timedeltaobj.total_seconds()
    timetot = ""
    if secs > 86400:
        days = secs // 86400
        if days == 1:
            timetot += f"{int(days)} dzień"
        else:
            timetot += f"{int(days)} dni"
        secs = secs - days * 86400

    if secs > 3600:
        hrs = secs // 3600
        timetot += f" {int(hrs)}h"
        secs = secs - hrs * 3600

    if secs > 60:
        mins = secs // 60
        timetot += f" {int(mins)}m"
        secs = secs - mins * 60

    if secs > 0:
        timetot += f" {int(secs)}s"
    return timetot


@register.filter(name='no_microseconds')
def no_microseconds(duration):
    return str(duration)[:-7]
