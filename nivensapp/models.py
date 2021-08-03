from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'


class Situation(models.Model):
    description = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return str(self.description)

    class Meta:
        db_table = 'situacao'
        verbose_name = 'Situação'
        verbose_name_plural = 'Situações'


class Employee(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    manager = models.ForeignKey(User, on_delete=models.CASCADE,
                                blank=False, null=False)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING,
                                   null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False,
                              unique=True)
    cell_phone = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    situation = models.ForeignKey(Situation, on_delete=models.DO_NOTHING,
                                  max_length=20, null=True, blank=True)
    discord_username = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'funcionario'
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'


class PointTime(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 blank=False, null=False)
    day = models.DateField(auto_now_add=True, null=False,
                           blank=False, editable=True)
    start_time = models.DateTimeField(null=True, blank=True)
    break_time = models.DateTimeField(null=True, blank=True)
    back_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.employee.name) + ' - ' + str(self.day)

    class Meta:
        db_table = 'ponto'
        verbose_name = 'Ponto'
        verbose_name_plural = 'Pontos'
        unique_together = ('employee', 'day')


# class Report(models.Model):# refazer
#
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
#                                     blank=False, null=False)
#     day = models.DateField(auto_now_add=True, null=False,
#                         blank=False, editable=True)
#     start_time = models.DateTimeField(null=True, blank=True)
#     break_time = models.DateTimeField(null=True, blank=True)
#     back_time = models.DateTimeField(null=True, blank=True)
#     finish_time = models.DateTimeField(null=True, blank=True)
#
#     def __str__(self):
#         return str(self.employee.name) + ' - ' + str(self.day)
