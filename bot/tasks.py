import discord
from discord.ext import commands
import time
import random
import os
import django
from asgiref.sync import sync_to_async
# import mysql.connector

os.environ['DJANGO_SETTINGS_MODULE'] = 'nivensproject.settings'
django.setup()

from nivensapp.models import Employee, PointTime
from datetime import date, datetime

client = commands.Bot(command_prefix='.')

global entrada, saida, registro


@client.event
async def on_ready():
    print("Cheguei rapaziada do trampo!")


@client.event
async def on_member_join(member):
    print("Bem vindo!")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


@client.command()
async def ajuda(ctx):
    await ctx.send("-------------------------------------Bem-vindo!-------------------------------------"
                   "\nAbaixo estão os comandos necessários para bater o ponto da forma correta:\n"
                   "\nDigite .entrar (Para registrar sua primeira entrada)\n"
                   "\nDigite .almoco (Para registrar sua saída para o almoço)\n"
                   "\nDigite .almocov (Para registrar sua volta do almoço)\n"
                   "\nDigite .saida (Para registrar sua saída)")


@sync_to_async
def get_employee(employee):
    filter = Employee.objects.filter(discord_username__iexact=employee).exists()
    if filter:
        employee = Employee.objects.get(discord_username__iexact=employee)
        return employee
    return None


@sync_to_async
def get_employee_point(employee):
    filter = PointTime.objects.filter(employee=employee, day=date.today())
    if filter:
        return filter
    return None


@sync_to_async
def save_employee_point(employee, period):
    save_point = PointTime.objects.get(employee=employee, day=date.today())
    setattr(save_point, period, datetime.today())
    save_point.save()
    return save_point


@sync_to_async
def create_employee_point(employee):
    save_point = PointTime.objects.create(employee=employee,
                                          day=date.today(),
                                          start_time=datetime.today())
    return save_point


@client.command()
async def entrar(ctx):
    funcionario_username = ctx.message.author
    funcionario_nome = funcionario_username.name
    funcionario_obj = await get_employee(funcionario_username)
    if funcionario_obj:
        point = await get_employee_point(funcionario_obj)
        if point:
            if point[0].start_time:
                await ctx.send(f"Não foi possível realizar batida.\nEntrada já cadastrada:\n"
                               f"{point[0].start_time.strftime('%m/%d/%Y às %H:%M:%S')}")

        else:
            new_point = await create_employee_point(funcionario_obj)
            await ctx.send(f"Ponto batido, entrada: {funcionario_nome}"
                           f"\n{new_point.start_time.strftime('%m/%d/%Y às %H:%M:%S')}")


@client.command()
async def almoco(ctx):
    funcionario_username = ctx.message.author
    funcionario_nome = funcionario_username.name
    funcionario_obj = await get_employee(funcionario_username)
    if funcionario_obj:
        point = await get_employee_point(funcionario_obj)
        if point:
            print(point[0].day)
            if point[0].break_time:
                await ctx.send(f"Não foi possível realizar batida.\nPausa de almoço já cadastrada:\n"
                               f"{point[0].break_time.strftime('%m/%d/%Y às %H:%M:%S')}")
            else:
                new_point = await save_employee_point(funcionario_obj, 'break_time')
                await ctx.send(f"Ponto batido, almoço: {funcionario_nome}"
                               f"\n{new_point.break_time.strftime('%m/%d/%Y às %H:%M:%S')}")
        else:
            await ctx.send(f"Não foi possível realizar batida de almoço.\nEntrada não foi cadastrada.")


@client.command()
async def almocov(ctx):
    funcionario_username = ctx.message.author
    funcionario_nome = funcionario_username.name
    funcionario_obj = await get_employee(funcionario_username)
    if funcionario_obj:
        point = await get_employee_point(funcionario_obj)
        if point:
            if point[0].back_time:
                await ctx.send(f"Não foi possível realizar batida.\nRetorno de almoço já cadastrado:\n"
                               f"{point[0].back_time.strftime('%m/%d/%Y às %H:%M:%S')}")
            else:
                new_point = await save_employee_point(funcionario_obj, 'back_time')
                await ctx.send(f"Ponto batido, retorno almoço: {funcionario_nome}"
                               f"\n{new_point.back_time.strftime('%m/%d/%Y às %H:%M:%S')}")
        else:
            await ctx.send(f"Não foi possível realizar batida de retorno do almoço.\nEntrada não foi cadastrada.")


@client.command()
async def saida(ctx):
    funcionario_username = ctx.message.author
    funcionario_nome = funcionario_username.name
    funcionario_obj = await get_employee(funcionario_username)
    if funcionario_obj:
        point = await get_employee_point(funcionario_obj)
        if point:
            if point[0].finish_time:
                await ctx.send(f"Não foi possível realizar batida.\nSaída já cadastrada:\n"
                               f"{point[0].finish_time.strftime('%m/%d/%Y às %H:%M:%S')}")
            else:
                new_point = await save_employee_point(funcionario_obj, 'finish_time')
                await ctx.send(f"Ponto batido, retorno almoço: {funcionario_nome}"
                               f"\n{new_point.finish_time.strftime('%m/%d/%Y às %H:%M:%S')}")
        else:
            await ctx.send(f"Não foi possível realizar batida de saída.\nEntrada não foi cadastrada.")


@client.command(aliases =['8ball', 'Vidente', 'vidente'])
async def _8ball(ctx, *, pergunta):
    respostas = ['Com certeza!.',
                 'Sem dúvida!',
                 'Sim, definitivamente.',
                 'Você pode confiar nisso.',
                 'A meu ver, sim.',
                 'Provavelmente',
                 'Sim',
                 'Resposta confusa, tente novamente',
                 'Pergunte novamente mais tarde.',
                 'Melhor eu não te contar agora',
                 'Não conte com isso',
                 'Minha respostas é não',
                 'Minhas fontes dizem que não',
                 'Muito duvidoso',
                 'Com certeza não!',
                 'Nunca!']
    await ctx.send(f"Pergunta: {pergunta}\n Resposta: {random.choice(respostas)}")


client.run('ODE3OTM0OTYzNDUwMDUyNjI5.YEQvSw.WwCQLCGD7_wh8OI887UuU4NbaI4')