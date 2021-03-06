# Generated by Django 3.1.7 on 2021-08-02 16:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nivensapp', '0004_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='name',
        ),
        migrations.AddField(
            model_name='employee',
            name='discord_username',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='report',
            name='back_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='break_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='day',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='nivensapp.employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='finish_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
