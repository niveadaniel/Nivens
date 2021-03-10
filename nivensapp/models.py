from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    email = models.EmailField(max_length=50)
    cell_phone = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'funcionario'
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

