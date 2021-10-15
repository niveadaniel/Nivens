from calendar import monthrange
from io import BytesIO

import xlsxwriter
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages

from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from nivensproject.settings import EMAIL_HOST_USER
from .models import Department, Employee, Situation, PointTime
from .choices import MONTHS
from datetime import date, datetime
from django.core import serializers

from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string


def index(request):
    return redirect('/login/')


@csrf_protect
def login_user(request):
    return render(request, 'login.html')


@csrf_protect
def login_submit(request):
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


def logout_user(request):
    logout(request)
    return redirect('/login/')


def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Pedido de Redefinicao de Senha"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Nivens',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    message = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, message, EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except Exception as ex:
                        return HttpResponse(ex)
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html",
                  context={"password_reset_form": password_reset_form})


@login_required(login_url='/login/')
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
                    "<button type='button' class='btn btn-primary btn-sm' id='edit-list' style='padding-right: 5px;'>"
                        "</button>" 
                 "</a>" % str(employee.id) +
                 "<a href='/list/point_time/?id=%s'>"
                    "<button type='button' class='btn btn-dark btn-sm' id=''>"
                        "<span class='edit'>Espelho</span></button>"
                 "</a>" % str(employee.id) +
                 "<a href='/delete/employee?id=%s' notification-modal='1'>"
                    "<button type='button' class='btn btn-danger btn-sm btn-delete' >"
                        "<span class='delete'>Deletar</span></button>"
                 "</a>" % str(employee.id)
                 ]
            )
    return employees_list


def get_employees_list(request):
    draw = int(request.GET['draw'])
    value = request.GET['search[value]']
    department_id = request.GET['department']
    employees = Employee.objects.filter(manager_id=request.user.id, active=True)
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
    employee_id = request.GET.get('id')
    employee = Employee.objects.get(id=employee_id) if employee_id else None
    if employee_id:
        manager_id = employee.manager.id
        if employee.manager.first_name and employee.manager.last_name:
            manager_name = '%s %s' % (employee.manager.first_name, employee.manager.last_name)
        else:
            manager_name = employee.manager
    else:
        manager_id = request.user.id
        if request.user and request.user.first_name and request.user.last_name:
            manager_name = '%s %s' % (request.user.first_name, request.user.last_name)
        else:
            manager_name = request.user.username
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
    employee_id = request.POST['id']
    name = request.POST['name']
    email = request.POST['email']
    cell_phone = request.POST['cell_phone']
    city = request.POST['city']
    department = request.POST['department']
    manager = request.POST['manager']
    discord_username = request.POST['discord_username']
    if 'situation' in request.POST:
        situation = request.POST['situation']
    else:
        situation = Situation.objects.filter(description='Ativo')[0].id
    try:
        if employee_id:
            Employee.objects.filter(id=employee_id).update(name=name,
                                                           email=email,
                                                           cell_phone=cell_phone,
                                                           city=city,
                                                           department_id=department,
                                                           manager_id=manager,
                                                           situation_id=situation,
                                                           discord_username=discord_username)
        else:
            Employee.objects.create(name=name,
                                    email=email,
                                    cell_phone=cell_phone,
                                    city=city,
                                    department_id=department,
                                    manager_id=manager,
                                    situation_id=situation,
                                    discord_username=discord_username)

        return JsonResponse({'success': True})
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Não foi possível salvar dados.'})


def list_point_time(request):
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


def get_total_hour(point):
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
    point_time_list = []
    if point_time:
        for point in point_time:
            total_hour = get_total_hour(point)
            point_time_list.append(
                [point.start_time.strftime('%d/%m'),
                 point.start_time.strftime('%H:%M:%S'),
                 point.break_time.strftime('%H:%M:%S') if point.break_time else '-',
                 point.back_time.strftime('%H:%M:%S') if point.back_time else '-',
                 point.finish_time.strftime('%H:%M:%S') if point.finish_time else '-',
                 'h'.join(str(total_hour).split(':')[:2]) if total_hour else '0h',
                 '0,00',
                 ]
            )
    return point_time_list


def get_report(request):
    try:
        employee_id = request.GET.get('id')
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))
        days_in_month = monthrange(year, month)
        point_time = PointTime.objects.filter(employee=employee_id,
                                              start_time__gte=datetime(year, month, 1, 0, 0),
                                              start_time__lte=datetime(year, month, days_in_month[1], 0, 0))
        times = []
        for time in point_time:
            dic = dict()
            dic['Funcionario'] = time.employee.name
            dic['Data'] = time.day.strftime('%d/%m/%Y')
            dic['Entrada'] = time.start_time.strftime('%H:%M:%S') if time.start_time else '-'
            dic['Pausa'] = time.break_time.strftime('%H:%M:%S') if time.break_time else '-'
            dic['Retorno'] = time.back_time.strftime('%H:%M:%S') if time.back_time else '-'
            dic['Saida'] = time.finish_time.strftime('%H:%M:%S') if time.finish_time else '-'
            total_hour = get_total_hour(time)
            dic['Total'] = 'h'.join(str(total_hour).split(':')[:2]) if total_hour else '0h'
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

        response['Content-Disposition'] = 'attachment; filename=Relatorio_%s_%s_%s.xlsx' % (point_time[0].employee.name, MONTHS[month-1][1], year)
        return response
    except Exception as e:
        print(e)
        return HttpResponseServerError('Houve um erro, não foi possível gerar relatório.')


def delete_employee(request):
    id = request.GET.get('id')
    if id:
        employee = Employee.objects.get(id=id)
        employee.active = False
        employee.save()
    return redirect('/list')



def insert_data_excel(lista, worksheet, keys):
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
    tipos = PointTime.objects.raw(
        "select 1 as id, ponto.`day`, ponto.start_time from nivens.ponto group by employee_id;")
    return render(request, 'templates/dashborad_with_pivot.html', {'tipos': tipos})

