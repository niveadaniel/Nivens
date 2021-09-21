from calendar import monthrange
from datetime import date, datetime
from io import BytesIO

import xlsxwriter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from .choices import MONTHS
from .models import Department, Employee, PointTime, Situation


def login_user(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    return render(request, 'login.html')


@csrf_protect
def login_submit(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    kwargs = dict(request.POST)
    if request.POST:
        username = kwargs['username'][0]
        password = kwargs['password'][0]
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('/list/')
        else:
            messages.error(request, 'Usuário ou senha inválidos')

    return redirect('/login/')


def change_password(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.method == 'POST':
        kwargs = dict(request.POST)
        print(kwargs)
    return render(request, 'change_password.html')


def logout_user(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def employee_list(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    department = Department.objects.all()
    dic = {'department': department}
    return render(request, 'employee_list.html', dic)


def create_data_table_employees(employees):
    """[summary]

    Args:
        employees ([type]): [description]

    Returns:
        [type]: [description]
    """
    employees_list = []
    if employees:
        for employee in employees:
            employees_list.append(
                [employee.name,
                 employee.email,
                 employee.department.name,
                 employee.situation.description,
                 "<a href='/edit/employee/?id=%s' style='padding-right: 5px;'>"
                    "<button type='button' class='btn btn-primary btn-sm' id='' style='padding-right: 5px;'>"
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
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
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


@login_required(login_url='/login/')
def edit_employee(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
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


@login_required(login_url='/login/')
def save_employee(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
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
        situation = default_situation = Situation.objects.filter(description='Ativo')[
            0].id
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
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    years = []
    employee_id = request.GET.get('id')
    employee = Employee.objects.get(id=employee_id)
    point_time = PointTime.objects.filter(employee=employee_id)
    actual_year = date.today().year
    initial_year = point_time.first().start_time.year if point_time else actual_year
    for year in range(initial_year, actual_year+1):
        years.append(year)
    months_choices = MONTHS
    actual_month = date.today().month
    dic = {'employee': employee, 'MONTHS_CHOICES': months_choices,
           'actual_month': actual_month, 'years': years,
           'actual_year': actual_year}
    return render(request, 'point_time_list.html', dic)


def get_point_time_list(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    draw = int(request.GET['draw'])
    month = int(request.GET['month'])
    year = int(request.GET['year'])
    employee_id = request.GET['employee']
    days_in_month = monthrange(year, month)
    point_time = PointTime.objects.filter(employee=employee_id,
                                          start_time__gte=datetime(
                                              year, month, 1, 0, 0),
                                          start_time__lte=datetime(year, month, days_in_month[1], 0, 0))
    total = point_time.count()
    point_timelist = create_data_table_point_time(point_time)
    return JsonResponse({'data': point_timelist,
                         'draw': draw + 1,
                         'recordsTotal': total})


def get_total_hour(point):
    """[summary]

    Args:
        point ([type]): [description]

    Returns:
        [type]: [description]
    """
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
    return total_hour


def create_data_table_point_time(point_time):
    """[summary]

    Args:
        point_time ([type]): [description]

    Returns:
        [type]: [description]
    """
    point_time_list = []
    if point_time:
        for point in point_time:
            total_hour = get_total_hour(point)
            point_time_list.append(
                [point.start_time.strftime('%d/%m'),
                 point.start_time.strftime('%H:%M:%S'),
                 point.break_time.strftime(
                     '%H:%M:%S') if point.break_time else '-',
                 point.back_time.strftime(
                     '%H:%M:%S') if point.back_time else '-',
                 point.finish_time.strftime(
                     '%H:%M:%S') if point.finish_time else '-',
                 'h'.join(str(total_hour).split(':')[
                          :2]) if total_hour else '0h',
                 ]
            )
    return point_time_list


def get_report(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    try:
        employee_id = request.GET.get('id')
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))
        days_in_month = monthrange(year, month)
        point_time = PointTime.objects.filter(employee=employee_id,
                                              start_time__gte=datetime(
                                                  year, month, 1, 0, 0),
                                              start_time__lte=datetime(year, month, days_in_month[1], 0, 0))
        times = []
        for time in point_time:
            dic = dict()
            dic['Funcionario'] = time.employee.name
            dic['Data'] = time.day.strftime('%d/%m/%Y')
            dic['Entrada'] = time.start_time.strftime(
                '%H:%M:%S') if time.start_time else '-'
            dic['Pausa'] = time.break_time.strftime(
                '%H:%M:%S') if time.break_time else '-'
            dic['Retorno'] = time.back_time.strftime(
                '%H:%M:%S') if time.back_time else '-'
            dic['Saida'] = time.finish_time.strftime(
                '%H:%M:%S') if time.finish_time else '-'
            total_hour = get_total_hour(time)
            dic['Total'] = 'h'.join(str(total_hour).split(':')[
                                    :2]) if total_hour else '0h'
            times.append(dic)
        keys = dic.keys()
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        insert_data_excel(times, worksheet, keys)
        workbook.close()
        output.seek(0)
        response = HttpResponse(output,
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        response['Content-Disposition'] = 'attachment; filename=Relatorio_%s_%s_%s.xlsx' % (
            point_time[0].employee.name, MONTHS[month-1][1], year)
        return response
    except Exception as e:
        print(e)
        return HttpResponseServerError('Houve um erro, não foi possível gerar relatório.')


def insert_data_excel(lista, worksheet, keys):
    """[summary]

    Args:
        lista ([type]): [description]
        worksheet ([type]): [description]
        keys ([type]): [description]
    """
    if len(lista) > 0:
        for idx, l in enumerate(lista):
            idx = idx + 1
            for idx_l, (key, value) in enumerate(l.items()):
                worksheet.write(idx, idx_l, value)

    for idx, key in enumerate(keys):
        worksheet.write(0, idx, key)
        if len(lista) > 0:
            max_len = max(
                [max([(len(str(v[1]))) if v[1] is not None else 0, (len(str(v[0]))) if v[0] is not None else 0]) for v
                 in
                 [list(x.items())[idx] for x in lista]])
        else:
            max_len = len(key)
        worksheet.set_column(idx, idx, max_len + 3)


@login_required(login_url='/login/')
def dashboard_with_pivot(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    tipos = PointTime.objects.raw(
        "select 1 as id, ponto.`day`, ponto.start_time from nivens.ponto group by employee_id;")
    return render(request, 'templates/dashborad_with_pivot.html', {'tipos': tipos})
