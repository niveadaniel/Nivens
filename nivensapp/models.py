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
    manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    cell_phone = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    situation = models.ForeignKey(Situation, on_delete=models.DO_NOTHING, max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'funcionario'
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'



