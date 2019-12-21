from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=256)
    added_on = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    tax_no = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return self.name


class Case(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task, through="CaseTasks")

    def __str__(self):
        return self.name


class CaseTasks(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        if self.price is not None:
            return f"Price per hour for: {self.case} - {self.task} is {self.price}"
        else:
            return f"No price defined for: {self.case} - {self.task}"


class Timer(models.Model):
    class Meta:
        ordering = ['-end_time']
    start_time = models.DateTimeField(default=timezone.now, verbose_name='Początek')
    end_time = models.DateTimeField(null=True, verbose_name='Koniec')
    added_on = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
    is_active = models.BooleanField(default=False)
    duration = models.DurationField(null=True, verbose_name='Czas trwania')
    pause_active = models.BooleanField(default=False)
    pause_start_time = models.DateTimeField(null=True)
    pause_duration_total = models.DurationField(null=True, verbose_name='Czas przerw')
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Klient')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='Projekt')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Zadanie')

    def __str__(self):
        return f"Timer no {self.id}, started on {self.start_time}, finished on {self.end_time}," \
               f"duration {self.duration}, for  {self.client}, by {self.employee} on case {self.case}" \
               f"and task {self.task}"

    def calculate_timer_duration(self):
        if self.pause_active or self.is_active:
            raise Exception('timer is active')
        elif self.pause_duration_total is not None:
            self.duration = self.end_time - self.start_time - self.pause_duration_total
        else:
            self.duration = self.end_time - self.start_time
