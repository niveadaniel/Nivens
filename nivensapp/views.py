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


def index(request):

    """Função que gera o index da aplicação.

    Args:
        request (object): Objeto da requisição.

    Returns:
        object: Redirecionamento da página.
    """
    return redirect('/login/')


@csrf_protect
def login_user(request):
    """Função para realizar login do usuário.

    Args:
        request (object): Objeto responsável pela requisição para a API.

    Returns:
        object: Objeto para redenderização em html da requisição.
    """
    return render(request, 'login.html')


@csrf_protect
def login_submit(request):
    """Submissão dos dados de login para a API.

    Args:
        request (object): Objeto responsável pela requisição para a API.

    Returns:
        object: Objeto com redirecionamento do login.
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

@csrf_protect
def change_password(request):
    """Função de troca de senha.

    Args:
        request (object): Objeto responsável pela requisição para a API.

    Returns:
        object: Objeto para redenderização em html da requisição.
    """
    if request.method == 'POST':
        kwargs = dict(request.POST)
        print(kwargs)
    return render(request, 'change_password.html')


@csrf_protect
def logout_user(request):
    """Função de logout do usuário.

    Args:
        request (object): Objeto responsável pela requisição para a API.

    Returns:
        object: Objeto com redirecionamento do login.
    """
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def employee_list(request):
    """Função de listagem de funcionários.

    Args:
        request (object): Objeto responsável pela requisição para a API.

    Returns:
        object: Objeto para redenderização em html da requisição.
    """
    department = Department.objects.all()
    dic = {'department': department}
    return render(request, 'employee_list.html', dic)


def create_data_table_employees(employees):
    """Função cria tabela de funcionários.

    Args:
        employees (dict): Lista de dados de funcionários.

    Returns:
        list: Lista de funcionários com os dados anexados.
    """
    employees_list = []
    if employees:
        for employee in employees:
            employees_list.append(
                [employee.name,
                 employee.email,
                 employee.department.name,
                 employee.situation.description,
                 "<a href='/edit/employee/?id=%s'>"
                    "<button type='button' class='btn btn-primary btn-sm' id='' style='padding-right: 5px;'>"
                 "<span class='edit'>Editar</span></button>"
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
    """Função chama a lista de funcionários.

    Args:
        request (object): Objeto responsável pela requisição para a API.

    Returns:
        file: Json com resposta da requisição.
    """
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
    """Função para edição de dados de um funcionário.

    Args:
        request (object): Objeto responsável pela requisição para a API.

    Returns:
        object: Objeto para redenderização em html da requisição.
    """
    manager_id = request.user.id
    manager_name = request.user
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
    """Função para salvar edições nos dados do funcionário.

    Args:
        request (object): Objeto responsável pela requisição para a API.

    Returns:
        file: Json com resposta da requisição.
    """
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
    """Função para listagem dos pontos recebidos pelo sistema.

    Args:
        request (object): Objeto responsável pela requisição para a API.

    Returns:
        object: Objeto para redenderização em html da requisição.
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
    """Função para pedir lista de pontos trecebidos.

    Args:
        request (object): Objeto responsável pela requisição para a API.

    Returns:
        file: Json com resposta da requisição.
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
    """Função para calcular total de horas trabalhadas.

    Args:
        point (object): Objeto com os tempos inserdidos via Discord.

    Returns:
        total_hour (object): Objeto contendo o total de horas calculadas.
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
    """Função que cria atabela de dados de pontos.

    Args:
        point_time (object): Objeto contendo dados de pontos recebidos da API do Discord.

    Returns:
        list: Lista de dados de pontos já estruturados.
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
    """Função para chamar o report de horas trabalhadas.

    Args:
        request (object): Objeto responsável pela requisição para a API.

    Returns:
        object: Resposta da requisição.
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


def delete_employee(request):
    """Função que deleta um funcionário.

    Args:
        request (object): Objeto da requisição.

    Returns:
        object: Redirecionamento de página.
    """
    id = request.GET.get('id')
    if id:
        employee = Employee.objects.get(id=id)
        employee.active = False
        employee.save()
    return redirect('/list')


def insert_data_excel(lista, worksheet, keys):
    """Função para inserção de dados numa planilha excel.

    Args:
        lista (list): Lista com dados a serem gravados.
        worksheet (object): Objeto para gravação de arquivo excel.
        keys (dict): Chaves dos dados a serem gravados.
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
