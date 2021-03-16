from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from .models import Department, Employee


def employee_list(request):
    department = Department.objects.all()
    dic = {'department': department}
    return render(request, 'employee_list.html', dic)


def create_data_table_employees(employees):
    employees_list = []
    if employees:
        for employee in employees:
            employees_list.append(
                [employee.name,
                 employee.email,
                 employee.department.name,
                 employee.situation.description]
            )
    return employees_list


def get_employees_list(request):
    draw = int(request.GET['draw'])
    value = request.GET['search[value]']
    department_id = request.GET['department']
    employees = Employee.objects.all()
    if department_id:
        employees = Employee.objects.filter(department_id=department_id)
    if value:
        employees = employees.filter(Q(name__icontains=value) |
                                     Q(email__icontains=value) |
                                     Q(department__name__icontains=value) |
                                     Q(situation__description__icontains=value))
    total = employees.count()
    employees_list = create_data_table_employees(employees)
    return JsonResponse({'data': employees_list,
                         'draw': draw + 1,
                         'recordsTotal': total,
                         'recordsFiltered': total})


