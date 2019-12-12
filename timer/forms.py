from django.core.exceptions import ValidationError
from django.forms import ModelForm, HiddenInput, DateTimeField

from timer.models import Timer


class TimerOnForm(ModelForm):
    class Meta:
        model = Timer
        fields = ['client', 'case', 'task', 'employee', 'is_active']
        labels = {'client': 'Klient',
                  'case': 'Projekt',
                  'task': 'Zadanie'}
        widgets = {'employee': HiddenInput,
                   'is_active': HiddenInput}


class TimerAddForm(ModelForm):
    class Meta:
        model = Timer
        fields = ['start_time', 'end_time', 'duration', 'client', 'case', 'task', 'employee']
        widgets = {'employee': HiddenInput}
        labels = {'client': 'Klient',
                  'case': 'Projekt',
                  'task': 'Zadanie',
                  'start_time': 'Początek',
                  'end_time': 'Koniec'}

    def __init__(self, *args, **kwargs):
        super(TimerAddForm, self).__init__(*args, **kwargs)
        self.fields['end_time'].required = False
        self.fields['duration'].required = False

    def clean(self):
        cleaned_data = super(TimerAddForm, self).clean()
        #check times
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        duration = cleaned_data.get('duration')
        if not end_time and not duration:
            raise ValidationError('Wypełnij czas końcowy timera lub czas trwania')
        elif end_time and not duration:
            if end_time < start_time:
                raise ValidationError('Koniec nie może być wcześniej od początku')
            else:
                temp_duration = end_time - start_time
                cleaned_data['duration'] = temp_duration
        elif duration and not end_time:
            temp_end_time = start_time + duration
            cleaned_data['end_time'] = temp_end_time
        else:
            if end_time - start_time != duration:
                raise ValidationError('Podano złe dane. Wypełnij czas końcowy timera lub czas trwania')
        #check user
        employee = cleaned_data.get('employee')
        if employee != self.request.user:
            raise ValidationError('Złe id usera')
