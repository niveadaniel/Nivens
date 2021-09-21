from django.contrib import admin

from .models import Department, Employee, PointTime, Situation


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Modelo de dados de entrada do funcionário.

    Args:
        admin (object): objeto do administrador.
    """
    list_display = ['name', 'email', 'cell_phone', 'manager']
    search_fields = ('name', 'email', 'cell_phone', 'manager')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Modelo de dados de departamento.

    Args:
         admin (object): objeto do administrador.
    """
    list_display = ['id', 'name']
    search_fields = ('id', 'name')


@admin.register(Situation)
class SituationAdmin(admin.ModelAdmin):
    """Modelo de dados de situação do funcionário.

    Args:
        admin (object): objeto do administrador.
    """
    list_display = ['id', 'description']
    search_fields = ('id', 'description')


@admin.register(PointTime)
class PointTimeAdmin(admin.ModelAdmin):
    """Modelo de dados de registro de pontos.

    Args:
        admin (object): objeto do administrador.
    """
    list_display = ['employee', 'start_time', 'finish_time']
    search_fields = ('employee__name', 'start_time', 'finish_time')
