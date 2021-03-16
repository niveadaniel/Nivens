from django.contrib import admin
from .models import Employee, Department, Situation


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'cell_phone', 'manager']
    search_fields = ('name', 'email', 'cell_phone', 'manager')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ('id', 'name')


@admin.register(Situation)
class SituationAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']
    search_fields = ('id', 'description')
