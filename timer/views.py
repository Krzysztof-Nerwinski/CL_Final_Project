from django.shortcuts import render
from django.views import View

from timer.forms import TimerOnForm


class TimerView(View):
    def get(self, request):
        form = TimerOnForm()
        return render(request, 'timer.html', {'form': form})

    def post(self, request):
        form = TimerOnForm(request.POST)
        if form.is_valid():
            timer = form.save()
        return render(request, 'timer.html', {'timer': timer})
