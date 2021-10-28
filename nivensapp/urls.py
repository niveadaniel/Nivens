from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('login/submit', views.login_submit),
    path('list/', views.employee_list, name='employee_list'),
    path('change-password/', views.change_password, name='change_password'),
    path('api/list_employee/', views.get_employees_list, name='get_list_employees'),
    path('edit/employee/', views.edit_employee, name='edit_employee'),
    path('delete/employee/', views.delete_employee, name='delete_employee'),
    path('edit/employee/submit/', views.save_employee, name='save_employee'),
    path('list/point_time/', views.list_point_time, name='list_point_time'),
    path('api/list_point_time/', views.get_point_time_list, name='get_point_time_list'),
    path('report/api/', views.get_report, name='get_report'),
    path('about-us/', views.get_about_us_page, name='get_about_us_page'),
]