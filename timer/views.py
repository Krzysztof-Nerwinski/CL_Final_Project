from django.shortcuts import render
from django.views import View

from timer.forms import TimerOnForm


class TimerView(View):
    def get(self, request):
        form = TimerOnForm()
        return render(request, 'timer.html', {'form': form})
