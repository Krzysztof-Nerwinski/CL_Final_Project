from datetime import datetime

from django.db import models

class Timer(models.Model):
    time = models.IntegerField()
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Employee(models.Model):
    pass
