from django.forms import ModelForm, HiddenInput

from timer.models import Timer


class TimerOnForm(ModelForm):
    class Meta:
        model = Timer
        fields = ['client', 'case', 'task', 'employee']
        labels = {'client': 'Klient',
                  'case': 'Projekt',
                  'task': 'Zadanie'}
        widgets = {'employee': HiddenInput}



