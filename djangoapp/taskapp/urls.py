from django.urls import path
from . import views

urlpatterns = [
    path('employees', views.employee_list, name='employee_list'),
    path('employee/<int:pk>', views.employee_details, name='employee_details'),
    path('tasks', views.task_list, name='task_list'),
    path('task/<int:pk>', views.task_details, name='task_details'),
]
