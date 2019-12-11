from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView

from timer.forms import TimerOnForm
from timer.models import Timer
from timer.utils import user_has_active_timer


class TimerView(LoginRequiredMixin, View):
    def get(self, request):
        timer = user_has_active_timer(request)
        form = TimerOnForm(initial={'employee': request.user})
        return render(request, 'timer.html', {'form': form,
                                              'timer': timer})

    def post(self, request):
        timer = user_has_active_timer(request)
        form = TimerOnForm(request.POST)
        if (timer is None) and form.is_valid():
            form.save()
            return redirect('timer')
        return render(request, 'timer.html', {'form': form})


class TimerListView(ListView):
    model = Timer
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TimerListView, self).get_context_data(**kwargs)
        timers = Timer.objects.filter(employee_id=self.request.user.id)
        context['timers'] = timers
        return context


class TimerDetailedView(DetailView):
    model = Timer


class TimerEditView(UpdateView):
    model = Timer
    fields = ['start_time', 'end_time', 'duration', 'client', 'case', 'task']
    # exclude = ['added_on', 'pause_active', 'pause_start_time', 'pause_duration_total', 'employee']

    def clean(self):
        cleaned_data = super(TimerEditView, self).clean()
        if cleaned_data.get('is_active') and cleaned_data.get('end_time'):
            raise ValidationError('Wyłącz timer zanim wprowadzisz jego datę zakończenia')
        if not cleaned_data.get('is_active') and not cleaned_data.get('end_time'):
            raise ValidationError('Wprowadź datę zakończenia timera')

    def get_success_url(self):
        return reverse('timer_details', args=[self.object.id])



def timer_stop(request, id):
    if request.method == 'GET':
        timer = user_has_active_timer(request)
        if timer.id == id:
            timer.is_active = False
            timer.end_time = timezone.now()
            timer.duration = timer.calculate_timer_duration
            timer.save()
            return redirect('timer_list')
        else:
            raise Exception('Złe id timera')


def timer_pause_toggle(request, id):
    if request.method == 'GET':
        timer = user_has_active_timer(request)
        if timer.id == id:
            if not timer.pause_active:
                timer.pause_start_time = timezone.now()
                timer.pause_active = True
                timer.save()
                return redirect('timer')
            else:
                if timer.pause_duration_total is not None:
                    timer.pause_duration_total += timezone.now() - timer.pause_start_time
                else:
                    timer.pause_duration_total = timezone.now() - timer.pause_start_time
                timer.pause_active = False
                timer.save()
                return redirect('timer')
        else:
            raise Exception('Złe id timera')

