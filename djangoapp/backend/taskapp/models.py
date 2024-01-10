from django.db import models


# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Task(models.Model):
    title = models.CharField(max_length=80)
    text = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    completed = False

    def __str__(self):
        return f'Task: {self.title} (Assigned to {self.employee}'
