from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.employee_list, name='employee_list'),
    path('api/list_employee/', views.get_employees_list, name='get_list_employees'),
    path('edit/employee/', views.edit_employee, name='edit_employee'),
    path('edit/employee/submit/', views.save_employee, name='save_employee')
]