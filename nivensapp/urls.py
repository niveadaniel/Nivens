from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('login/submit', views.login_submit),
    path('list/', views.employee_list, name='employee_list'),
    path('api/list_employee/', views.get_employees_list, name='get_list_employees'),
    path('edit/employee/', views.edit_employee, name='edit_employee'),
    path('delete/employee/', views.delete_employee, name='delete_employee'),
    path('edit/employee/submit/', views.save_employee, name='save_employee'),
    path('list/point_time/', views.list_point_time, name='list_point_time'),
    path('api/list_point_time/', views.get_point_time_list, name='get_point_time_list'),
    path('report/api/', views.get_report, name='get_report')
]