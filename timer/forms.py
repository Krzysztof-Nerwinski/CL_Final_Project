from datetimepicker.widgets import DateTimePicker
from django.core.exceptions import ValidationError
from django.forms import ModelForm, HiddenInput, DurationField

from timer.models import Timer


class TimerStartForm(ModelForm):
    class Meta:
        model = Timer
        fields = ['client', 'case', 'task', 'employee', 'is_active']
        widgets = {'employee': HiddenInput,
                   'is_active': HiddenInput}

    def clean(self):
        cleaned_data = super(TimerStartForm, self).clean()
        is_active = cleaned_data.get('is_active')
        #check is active
        if is_active is False:
            raise ValidationError('Błąd formularza, is_active == False, nie można wystartować timera')
        # #check employee_id
        # employee = cleaned_data.get('employee')
        # if employee != self.request.user:
        #     raise ValidationError('Złe id pracownika, nie można zacząc timera dla innego pracownika')
        #todo: sprawdz czy user == employee



class TimerAddForm(ModelForm):
    class Meta:
        model = Timer
        fields = ['start_time', 'end_time', 'duration', 'client', 'case', 'task', 'employee']
        widgets = {'employee': HiddenInput}
        labels = {'duration': 'Czas trwania (hh:mm:ss)'}

    def __init__(self, *args, **kwargs):
        super(TimerAddForm, self).__init__(*args, **kwargs)
        self.fields['end_time'].required = False
        self.fields['duration'].required = False

    def clean(self):
        cleaned_data = super(TimerAddForm, self).clean()
        check_start_end_duration_values(cleaned_data)


def check_start_end_duration_values(cleaned_data):
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


