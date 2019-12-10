from django.urls import path
from timer.views import TimerView, timer_stop_view, TimerListView

urlpatterns = [
    path('', TimerView.as_view(), name='timer'),
    path('timer/stop/<int:id>', timer_stop_view, name="timer_stop"),
    path('timer/list', TimerListView.as_view(), name='timer_list'),
]
