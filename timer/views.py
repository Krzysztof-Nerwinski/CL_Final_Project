from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.forms import HiddenInput
from django.http import Http404, JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from timer.forms import TimerStartForm, TimerAddForm, check_start_end_duration_values
from timer.models import Timer
from timer.utils import user_has_active_timer, calculate_pause_time


class TimerView(LoginRequiredMixin, View):
    def get(self, request):
        if user_has_active_timer(request):
            return redirect('timer_active')
        form = TimerStartForm(initial={'employee': request.user,
                                       'is_active': True})
        return render(request, 'timer_start.html', {'form': form})

    def post(self, request):
        timer = user_has_active_timer(request)
        form = TimerStartForm(request.POST)
        if (timer is None) and form.is_valid():
            form.save()
            return redirect('timer_active')
        return render(request, 'timer_start.html', {'form': form})


class TimerActiveView(View):
    def get(self, request):
        timer = user_has_active_timer(request)
        if not timer:
            return redirect('timer')
        form = TimerStartForm(initial={
            'client': timer.client,
            'case': timer.case,
            'task': timer.task,
            'employee': timer.employee,
            'is_active': timer.is_active
        })
        return render(request, 'timer_active.html', {'timer': timer,
                                                     'form': form})

    def post(self, request):
        timer = user_has_active_timer(request)
        form = TimerStartForm(request.POST)
        if (timer is not None) and form.is_valid():
            timer.client = form.cleaned_data['client']
            timer.case = form.cleaned_data['case']
            timer.task = form.cleaned_data['task']
            timer.save()
            return redirect('timer_active')
        return render(request, 'timer_active.html', {'timer': timer,
                                                     'form': form})


class TimerAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = TimerAddForm(initial={'employee': request.user})
        return render(request, 'timer_add.html', {'form': form})

    def post(self, request):
        form = TimerAddForm(request.POST)
        if form.is_valid():
            new_timer = form.save()
            return redirect('timer_details', new_timer.id)
        return render(request, 'timer_add.html', {'form': form})


class TimerListView(LoginRequiredMixin, ListView):
    model = Timer
    context_object_name = "timers"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TimerListView, self).get_context_data(**kwargs)
        timers = Timer.objects.filter(employee_id=self.request.user.id).order_by('-end_time')
        context['timers'] = timers
        paginator = Paginator(timers, self.paginate_by)
        page = self.request.GET.get('page')
        timers = paginator.get_page(page)
        context['timers'] = timers
        return context


class TimerDetailedView(LoginRequiredMixin, DetailView):
    model = Timer
    context_object_name = 'timer'


class TimerEditView(LoginRequiredMixin, UpdateView):
    model = Timer
    fields = ['start_time', 'end_time', 'client', 'case', 'task']

    def form_valid(self, form):
        redirect_url = super(TimerEditView, self).form_valid(form)
        start_time = form.cleaned_data.get('start_time')
        end_time = form.cleaned_data.get('end_time')
        temp_timer = Timer.objects.get(pk=self.kwargs['pk'])
        if end_time < start_time:
            form.add_error('end_time', 'Koniec nie może być wcześniej od początku')
            return super(TimerEditView, self).form_invalid(form)
        else:
            if temp_timer.pause_duration_total is None:
                temp_timer.duration = end_time - start_time
            else:
                temp_timer.duration = end_time - start_time - temp_timer.pause_duration_total
        if temp_timer.duration < timedelta(seconds=0):
            form.add_error('end_time', 'Czas pracy z przerwą mniejszy od zera')
            return super(TimerEditView, self).form_invalid(form)
        temp_timer.save()
        return redirect_url

    def get_success_url(self):
        return reverse('timer_details', args=[self.object.id])


class TimerDeleteView(LoginRequiredMixin, DeleteView):
    model = Timer
    success_url = reverse_lazy('timer_list')


@login_required
def timer_stop(request, timer_id):
    if request.method == 'GET':
        timer = user_has_active_timer(request)
        if timer.id == timer_id:
            if timer.pause_active:
                timer.pause_active = False
                calculate_pause_time(timer)
            timer.is_active = False
            timer.end_time = timezone.now()
            timer.calculate_timer_duration()
            timer.save()
            return redirect('timer_details', timer.id)
        else:
            raise Exception('Złe id timera')
    else:
        raise Http404('Wrong HTTP method')


@login_required
def timer_pause(request, timer_id):
    if request.method == 'GET':
        timer = user_has_active_timer(request)
        if timer.id == timer_id and not timer.pause_active:
            timer.pause_start_time = timezone.now()
            timer.pause_active = True
            timer.save()
            data = {'pause_from': timer.pause_start_time}
        else:
            data = {'error_info': 'Złe id timera'}
        return JsonResponse(data)


@login_required
def timer_unpause(request, timer_id):
    if request.method == 'GET':
        timer = user_has_active_timer(request)
        if timer.id == timer_id and timer.pause_active:
            calculate_pause_time(timer)
            timer.pause_active = False
            timer.save()
            data = {'pause_duration': str(timer.pause_duration_total)[:-7]}
        else:
            data = {'error_info': 'Złe id timera'}
        return JsonResponse(data)
