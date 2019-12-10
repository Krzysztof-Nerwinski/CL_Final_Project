from django.urls import path
from timer.views import TimerView

urlpatterns = [
   path('', TimerView.as_view(), name='timer'),
]
