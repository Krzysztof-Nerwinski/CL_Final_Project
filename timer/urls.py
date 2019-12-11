from django.urls import path
from timer.views import TimerView, timer_stop, TimerListView, TimerDetailedView, timer_pause_toggle, TimerEditView

urlpatterns = [
    path('', TimerView.as_view(), name='index'),
    path('timer/', TimerView.as_view(), name='timer'),
    path('timer/stop/<int:id>', timer_stop, name="timer_stop"),
    path('timer/pause/<int:id>', timer_pause_toggle, name="timer_pause"),
    path('timer/list/', TimerListView.as_view(template_name='timers_list.html'), name='timer_list'),
    path('timer/<int:pk>/', TimerDetailedView.as_view(template_name='timer_details.html'), name='timer_details'),
    path('timer/edit/<int:pk>/', TimerEditView.as_view(template_name='timer_edit.html'), name='timer_edit'),

]
