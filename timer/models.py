from datetime import datetime

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


class Task(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()


class Case(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task, through="CaseTasks")


class CaseTasks(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Timer(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    added_on = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    @property
    def duration(self):
        return self.end_time - self.start_time
