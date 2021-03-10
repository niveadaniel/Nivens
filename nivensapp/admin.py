from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'cell_phone', 'manager']
    search_fields = ('name', 'email', 'cell_phone', 'manager')