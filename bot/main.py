import discord
from discord.ext import commands
import time
import random
# import mysql.connector

# con = mysql.connector.connect(host='localhost',
                              # database='db_funcionario',
                              # user='root',
                              # password='18p94#',
                              # auth_plugin='mysql_native_password')

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
    await ctx.send("-------------------------------------Bem-vindo!-------------------------------------\nAbaixo estão os comandos necessários para bater o ponto da forma correta:\n"
                   "\nDigite .entrar (Para registrar sua primeira entrada)\n"
                   "\nDigite .almoco (Para registrar sua saída para o almoço)\n"
                   "\nDigite .almocov (Para registrar sua volta do almoço)\n"
                   "\nDigite .saida (Para registrar sua saída)")

@client.command()
async def entrar(ctx):
    funcionario = ctx.message.author.name
    await ctx.send(f"Ponto batido: {funcionario}\n{time.strftime('%d/%m/%Y às %H : %M : %S', time.localtime())}")

@client.command()
async def almoco(ctx):
    funcionario = ctx.message.author.name
    await ctx.send(f"Saiu para o almoço: {funcionario}\n{time.strftime('%d/%m/%Y às %H : %M : %S', time.localtime())}")

@client.command()
async def almocov(ctx):
    funcionario = ctx.message.author.name
    await ctx.send(f"Retornou do almoço: {funcionario}\n{time.strftime('%d/%m/%Y às %H : %M : %S', time.localtime())}")

@client.command()
async def saida(ctx):
    funcionario = ctx.message.author.name
    await ctx.send(f"Saiu: {funcionario}\n{time.strftime('%d/%m/%Y às %H : %M : %S', time.localtime())}")

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