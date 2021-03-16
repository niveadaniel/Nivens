from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.employee_list, name='employee_list'),
    path('api/list_employee/', views.get_employees_list, name='get_list_employees')
]