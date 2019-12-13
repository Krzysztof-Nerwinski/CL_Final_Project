from django import template

register = template.Library()


@register.filter(name='cut_microseconds')
def smooth_timedelta(timedeltaobj):
    """Convert a datetime.durationfield object into Days, Hours, Minutes, Seconds."""
    secs = timedeltaobj.total_seconds()
    timetot = ""
    if secs > 86400:  # 60sec * 60min * 24hrs
        days = secs // 86400
        timetot += "{} days".format(int(days))
        secs = secs - days * 86400

    if secs > 3600:
        hrs = secs // 3600
        timetot += f" {int(hrs)} godzin"
        secs = secs - hrs * 3600

    if secs > 60:
        mins = secs // 60
        timetot += f" {int(mins)} minut"
        secs = secs - mins * 60

    if secs > 0:
        timetot += f" {int(secs)} sekund"
    return timetot
