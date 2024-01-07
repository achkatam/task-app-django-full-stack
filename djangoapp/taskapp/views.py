from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Task
from .serializers import EmployeeSerializer, TaskSerializer
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
# Employees views
@api_view(['GET', "POST"])
def employee_list(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def employee_details(request, pk):
    employee = Employee.objects.get(id=pk)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployeeSerializer(isntance=employee, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Tasks
@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def task_create(request):
    try:
        existing_task = Task.objects.filter(
            title=request.data.get('title')
        ).first()

        if existing_task:
            return Response({'error': 'Task already exist'},
                            status=status.HTTP_400_BAD_REQUEST)

        existing_employee = Task.objects.filter(
            employee=request.data.get('employee')
        ).first()

        if not existing_employee:
            return Response({'error': f'Employee with this id does not exist'})

        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid data provided'},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'An error occurred'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# get a task
@api_view(['GET'])
def task_details(request, pk):
    try:
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'task not found'},
                        status=status.HTTP_404_NOT_FOUND)


# update task
@api_view(['PUT'])
def task_update(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({'error': 'task not found'},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(instance=task, data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': f'Invalid data provided. Details: {str(e)}'},
                        status=status.HTTP_400_BAD_REQUEST)


# delete task
@api_view(['DELETE'])
def delete_task(request, pk):
    try:
        task = Task.objects.get(id=pk)
        task.delete()
        return Response('Task deleted')
    except Exception as e:
        return Response({"error": f"Task with id: {pk} doesn't exist"},
                        status=status.HTTP_404_NOT_FOUND)
