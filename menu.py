import InquirerPy, DB
from MyLibrary import Clean
from datetime import datetime
import re

def Principal():
    menu = [
        {
            'type': 'list',
            'name': 'opcao',
            'message': f'\nSISTEMA: Qual ação deseja realizar?',
            'choices': ['Registrar Entrada', 'Registrar Saida', 'Listar', 'Buscar'],
        }
    ]
    Clean()
    match InquirerPy.prompt(menu):
        case {'opcao': 'Registrar Entrada'}:
            Registrar.Entrada()
        case {'opcao': 'Registrar Saida'}:
            Registrar.Saida()
        case {'opcao': 'Listar'}:
            Listar()
            input()
        case {'opcao': 'Buscar'}:
            Buscar()
            input()

def Nome() -> str:
    nome = InquirerPy.prompt([
        {
            'type': 'input',
            'name': 'nome',
            'message': 'Digite o nome do aluno:',
        }
    ])['nome']
    Clean()
    return nome

def Turma() -> str:
    curso = [
        {
            'type': 'list',
            'name': 'opcao',
            'message': f'Qual o curso do visitante?',
            'choices': ['INFO', 'AGRO', 'MINE', 'ADM'],
        }
    ]
    match InquirerPy.prompt(curso):
        case {'opcao': 'INFO'}:
            turma = [
                {
                    'type': 'list',
                    'name': 'opcao',
                    'message': f'Qual o ano do visitante?',
                    'choices': ['1° INFO', '2° INFO', '3° INFO'],
                }
            ]
            Clean()
            return InquirerPy.prompt(turma)['opcao']
        case {'opcao': 'AGRO'}:
            turma = [
                {
                    'type': 'list',
                    'name': 'opcao',
                    'message': f'Qual o ano do visitante?',
                    'choices': ['1° AGRO', '2° AGRO', '3° AGRO'],
                }
            ]
            Clean()
            return InquirerPy.prompt(turma)['opcao']
        case {'opcao': 'MINE'}:
            turma = [
                {
                    'type': 'list',
                    'name': 'opcao',
                    'message': f'Qual o ano do visitante?',
                    'choices': ['1° MINE', '2° MINE', '3° MINE'],
                }
            ]
            Clean()
            return InquirerPy.prompt(turma)['opcao']
        case {'opcao': 'ADM'}:
            turma = [
                {
                    'type': 'list',
                    'name': 'opcao',
                    'message': f'Qual o ano do visitante?',
                    'choices': ['1° ADM', '2° ADM', '3° ADM'],
                }
            ]
            Clean()
            return InquirerPy.prompt(turma)['opcao']
    Clean()

class Registrar:
    def Entrada():
        nome = Nome()
        turma = Turma()
        tipo = 'Entrada'
        return DB.insert(nome, turma, tipo)

    def Saida():
        nome = Nome()
        turma = Turma()
        tipo = 'Saida'
        return DB.insert(nome, turma, tipo)

def data(gambiarra: str) -> str:
    data = None
    while not data:
        data = InquirerPy.prompt([
            {
                'type': 'input',
                'name': 'data',
                'message': f'Digite a data {gambiarra} (AAAA-MM-DD):',
            }
        ])['data']
        Clean()
        try:
            datetime.strptime(data, "%Y-%m-%d")
            return data
        except ValueError:
            print("3RR0R: Data inexistente! Tente novamente.")
            data = None

def hora(gambiarra: str) -> str:
    hora = None
    while not hora:
        hora = InquirerPy.prompt([
            {
                'type': 'input',
                'name': 'hora',
                'message': f'Digite a hora {gambiarra} (HH:MM:SS):',
            }
        ])['hora']
        Clean()
        try:
            datetime.strptime(hora, "%H:%M:%S")
            return hora
        except ValueError:
            print("3RR0R: Formato inválido! Use HH:MM:SS (00-23:00-59:00-59)")
            hora = None

def Buscar():
    data_inicio = data('de inicio da busca')
    hora_inicio = hora('de inicio da busca')
    data_fim = data('de fim da busca')
    hora_fim = hora('de fim da busca')
    while datetime.strptime(f"{data_inicio} {hora_inicio}", "%Y-%m-%d %H:%M:%S") > datetime.strptime(f"{data_fim} {hora_fim}", "%Y-%m-%d %H:%M:%S"):
        Clean()
        print("3RR0R: inicio maior que fim! Tente novamente.")
        data_fim = data('de fim da busca')
        hora_fim = hora('de fim da busca')
    registros = DB.get_all([data_inicio, data_fim], [hora_inicio, hora_fim])
    Clean()
    if not registros:
        print("Nenhum registro encontrado nesse período.")
    else:
        for registro in registros:
            print(f"Nome: {registro['nome']} - Turma: {registro['turma']} - Tipo: {registro['tipo']} - {registro['data']} às {registro['hora']}")


def Listar():
    now = datetime.now()
    registros = DB.get_all(['2025-01-01', now.date().strftime("%Y-%m-%d")], ['00:00:00', now.time().strftime("%H:%M:%S")])
    Clean()
    for registro in registros:
        print(f"Nome: {registro['nome']} - Turma: {registro['turma']} - Tipo: {registro['tipo']} - {registro['data']} às {registro['hora']}")
