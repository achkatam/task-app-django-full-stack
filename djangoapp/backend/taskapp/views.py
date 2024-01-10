from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Task
from .serializers import EmployeeSerializer, TaskSerializer
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
# Employees views
@api_view(['GET'])
def employee_list(request):
    try:
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': 'List of employees not found'},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_employee(request):
    try:
        existing_employee = Employee.objects.filter(
            email=request.data.get('email')
        ).first()

        if existing_employee:
            return Response({'error': 'Employee with this email already exist'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid data provided'},
                            status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': 'An error occurred'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# get single employee by id
@api_view(['GET'])
def employee_details(request, pk):
    try:
        employee = Employee.objects.get(id=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': f'Employee with id: {pk} does not exist.'})


# update employee
@api_view(['PUT'])
def update_employee(request, pk):
    try:
        employee = Employee.objects.get(id=pk)

        serializer = EmployeeSerializer(instance=employee, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Employee with id: {pk} does not exist.'})


@api_view(['DELETE'])
# delete employee
def delete_employee(request, pk):
    try:
        employee = Employee.objects.get(id=pk)
        employee.delete()
        return Response({'message': f'Employee with id: {pk} successfully deleted'},
                        status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Employee with id: {pk} does not exist.'})


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
