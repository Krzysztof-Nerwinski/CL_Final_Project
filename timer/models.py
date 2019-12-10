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
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True)
    pause_time_start = models.DateTimeField(null=True)
    pause_time_end = models.DateTimeField(null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Timer no {self.id}, started on {self.start_time}, finished on {self.end_time}," \
               f"duration {self.duration}, for  {self.client}, by {self.employee} on case {self.case}" \
               f"and task {self.task}"

    @property
    def duration(self):
        return (self.end_time - self.start_time) - (self.pause_time_end - self.pause_time_start)
