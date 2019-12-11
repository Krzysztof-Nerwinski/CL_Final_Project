from django.db import migrations

from timer.models import Client, Case, Task, CaseTasks
from random import randint, uniform


def populate_clients():
    for i in range(1, 11):
        Client.objects.create(name=f"Klient number {i}", address=f"Ulica {i}/{i + 10}",
                              postal_code=f"00-00{i}" if i < 10 else f"00-0{i}", city=f"Miasto{i}",
                              phone=f"123-456-78{i}" if i < 10 else f"123-456-7{i}",
                              tax_no=f"123-456-00-01")


def populate_tasks():
    for i in range(1, 51):
        Task.objects.create(name=f"Przykładowe zadanie numer {i}", description=f"Przykladowi opis zadania {i}")


def populate_cases():
    for i in range(1, 31):
        case = Case.objects.create(name=f"Projekt numer {i}", description=f"przykladowy opis {i}",
                                   client_id=randint(1, 10))
        for j in range(1, randint(2, 11)):
            case.tasks.add(randint(2, 51))


def add_prices():
    casetasks = CaseTasks.objects.all()
    for cas in casetasks:
        if bool(randint(0,1)):
            cas.price = round(uniform(10, 1000), 2)
            cas.save()


class Migration(migrations.Migration):
    dependencies = [
        ('timer', '0003_auto_20191210_1401'),
    ]

    operations = []
