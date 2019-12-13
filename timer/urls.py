from django.urls import path
from timer.views import TimerView, timer_stop, TimerListView, TimerDetailedView, timer_pause_toggle, TimerEditView, \
    TimerAddView, TimerActiveView, TimerDeleteView

urlpatterns = [
    path('', TimerView.as_view(), name='timer'),
    path('timer/', TimerActiveView.as_view(), name='timer_active'),
    path('timer/stop/<int:timer_id>', timer_stop, name="timer_stop"),
    path('timer/pause/<int:timer_id>', timer_pause_toggle, name="timer_pause"),
    path('timer/list/', TimerListView.as_view(template_name='timers_list.html'), name='timer_list'),
    path('timer/<int:pk>/', TimerDetailedView.as_view(template_name='timer_details.html'), name='timer_details'),
    path('timer/edit/<int:pk>/', TimerEditView.as_view(template_name='timer_edit.html'), name='timer_edit'),
    path('timer/add/', TimerAddView.as_view(), name='timer_add'),
    path('timer/delete/<int:pk>', TimerDeleteView.as_view(template_name='timer_delete.html'), name='timer_delete'),

]
