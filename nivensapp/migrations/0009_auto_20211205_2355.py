# Generated by Django 3.1.7 on 2021-12-05 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nivensapp', '0008_employee_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointtime',
            name='day',
            field=models.DateField(),
        ),
    ]
