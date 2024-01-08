from django.urls import path
from . import views

urlpatterns = [
    path('employees', views.employee_list, name='employee_list'),
    path('create_employee', views.create_employee, name='create_employee'),
    path('employee/<int:pk>', views.employee_details, name='employee_details'),
    path('tasks', views.task_list, name='task_list'),
    path('task_create', views.task_create, name='create_task'),
    path('task/<int:pk>', views.task_details, name='task_details'),
    path('update_task/<int:pk>', views.task_update, name='task_update'),
    path('delete_task/<int:pk>', views.delete_task, name='delete_task')
]
