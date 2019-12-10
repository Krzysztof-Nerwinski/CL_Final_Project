from django.forms import ModelForm

from timer.models import Timer


class TimerOnForm(ModelForm):
    class Meta:
        model = Timer
        fields = ['client', 'case', 'task']
        labels = {'client': 'Klient',
                  'case': 'Projekt',
                  'task': 'Zadanie'}
