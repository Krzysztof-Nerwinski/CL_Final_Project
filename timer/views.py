from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from timer.forms import TimerOnForm
from timer.models import Timer
from timer.utils import user_has_active_timer


class TimerView(View):
    def get(self, request):
        timer = user_has_active_timer(request)
        form = TimerOnForm(initial={'employee': request.user})
        return render(request, 'timer.html', {'form': form,
                                              'timer': timer})

    def post(self, request):
        form = TimerOnForm(request.POST)
        if form.is_valid():
            form = form.save()
            return render(request, 'timer_active.html', {'form': form})
        return render(request, 'timer.html', {'form': form})


class TimerListView(View):
    def get(self, request):
        timers = Timer.objects.filter(employee=request.user)
        return render(request, 'timers_list.html', {'timers': timers})


def timer_stop_view(request, id):
    if request.method == 'GET':
        timer = user_has_active_timer(request)
        if timer.id == id:
            timer.end_time = datetime.now()
            timer.is_active = False
            timer.save()
            return redirect('timer')
