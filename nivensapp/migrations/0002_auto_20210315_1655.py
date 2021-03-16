# Generated by Django 3.1.7 on 2021-03-15 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nivensapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'db_table': 'departamento',
            },
        ),
        migrations.CreateModel(
            name='Situation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Situação',
                'verbose_name_plural': 'Situações',
                'db_table': 'situacao',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='nivensapp.department'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='situation',
            field=models.ForeignKey(blank=True, max_length=20, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='nivensapp.situation'),
        ),
    ]
