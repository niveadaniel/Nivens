from calendar import monthrange

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from .models import Department, Employee, Situation, PointTime
from .choices import MONTHS
from datetime import date, datetime
from django.core import serializers


def testing(request):
    department = Department.objects.all()
    dic = {'department': department}
    return render(request, 'table_test.html', dic)


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
                 employee.situation.description,
                 "<a href='/edit/employee/?id=%s'>"
                    "<button type='button' class='btn btn-primary btn-sm' id=''>"
                         "<span class='edit'>Editar</span></button>"
                 "</a>" % str(employee.id) +
                 "<a href='/list/point_time/?id=%s'>"
                    "<button type='button' class='btn btn-dark btn-sm' id=''>"
                        "<span class='edit'>Espelho</span></button>"
                 "</a>" % str(employee.id)
                 ]
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


def edit_employee(request):
    manager_id = request.user.id
    manager_name = request.user
    employee_id = request.GET.get('id')
    employee = Employee.objects.get(id=employee_id) if employee_id else None
    departments = Department.objects.all()
    situations = Situation.objects.all()
    default_situation = Situation.objects.filter(description='Ativo')
    if default_situation:
        default_situation = default_situation[0]
    dic = {'employee': employee,
           'manager_id': manager_id,
           'manager_name': manager_name,
           'departments': departments,
           'situations': situations,
           'default_situation': default_situation}
    return render(request, 'edit_employee.html', dic)


def save_employee(request):
    print(request.POST)
    employee_id = request.POST['id']
    name = request.POST['name']
    email = request.POST['email']
    cell_phone = request.POST['cell_phone']
    city = request.POST['city']
    department = request.POST['department']
    manager = request.POST['manager']
    if 'situation' in request.POST:
        situation = request.POST['situation']
    else:
        situation = default_situation = Situation.objects.filter(description='Ativo')[0].id
    try:
        if employee_id:
            Employee.objects.filter(id=employee_id).update(name=name,
                                                           email=email,
                                                           cell_phone=cell_phone,
                                                           city=city,
                                                           department_id=department,
                                                           manager_id=manager,
                                                           situation_id=situation)
        else:
            Employee.objects.create(name=name,
                                    email=email,
                                    cell_phone=cell_phone,
                                    city=city,
                                    department_id=department,
                                    manager_id=manager,
                                    situation_id=situation)

        return JsonResponse({'success': True})
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Não foi possível salvar dados.'})


def list_point_time(request):
    years = []
    employee_id = request.GET.get('id')
    employee = Employee.objects.get(id=employee_id)
    point_time = PointTime.objects.filter(employee=employee_id)
    initial_year = point_time.first().start_time.year
    actual_year = date.today().year
    for year in range(initial_year, actual_year+1):
        years.append(year)
    months_choices = MONTHS
    actual_month = date.today().month
    dic = {'employee': employee, 'MONTHS_CHOICES': months_choices,
           'actual_month': actual_month, 'years': years,
           'actual_year': actual_year}
    return render(request, 'point_time_list.html', dic)


def get_point_time_list(request):
    draw = int(request.GET['draw'])
    month = int(request.GET['month'])
    year = int(request.GET['year'])
    employee_id = request.GET['employee']
    days_in_month = monthrange(year, month)
    point_time = PointTime.objects.filter(employee=employee_id,
                                          start_time__gte=datetime(year, month, 1, 0, 0),
                                          start_time__lte=datetime(year, month, days_in_month[1], 0, 0))
    total = point_time.count()
    point_timelist = create_data_table_point_time(point_time)
    return JsonResponse({'data': point_timelist,
                         'draw': draw + 1,
                         'recordsTotal': total})


def create_data_table_point_time(point_time):
    point_time_list = []
    if point_time:
        for point in point_time:
            total_hour = None
            if point.finish_time:
                total_hour = point.finish_time - point.start_time
                if point.break_time and point.back_time:
                    total_hour = total_hour - (point.back_time - point.break_time)
            else:
                if point.back_time:
                    total_hour = point.back_time - point.start_time
                elif point.break_time:
                    total_hour = point.break_time - point.start_time

            point_time_list.append(
                [point.start_time.strftime('%d/%m'),
                 point.start_time.strftime('%H:%M:%S'),
                 point.break_time.strftime('%H:%M:%S') if point.break_time else '-',
                 point.back_time.strftime('%H:%M:%S') if point.back_time else '-',
                 point.finish_time.strftime('%H:%M:%S') if point.finish_time else '-',
                 'h'.join(str(total_hour).split(':')[:2]) if total_hour else '0h',
                 ]
            )
    return point_time_list
   

def dashboard_with_pivot(request):
    tipos = PointTime.objects.raw(
        "select 1 as id, ponto.`day`, ponto.start_time from nivens.ponto group by employee_id;")
    return render(request, 'templates/dashborad_with_pivot.html', {'tipos': tipos})




