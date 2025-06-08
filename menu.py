import InquirerPy, DB
from MyLibrary import Clean, Write
from datetime import datetime
from time import sleep

Save = []

def Principal(gambiarra: int):
    Clean()
    menu = [
        {
            'type': 'list',
            'name': 'opcao',
            'message': f'\nSISTEMA: Qual ação deseja realizar?',
            'choices': ['Registrar Entrada', 'Registrar Saida', 'Listar', 'Buscar', 'Encerrar'],
        }
    ]
    match InquirerPy.prompt(menu):
        case {'opcao': 'Registrar Entrada'}:
            Registrar.Entrada()
        case {'opcao': 'Registrar Saida'}:
            Registrar.Saida()
        case {'opcao': 'Listar'}:
            Exibir(Listar())
        case {'opcao': 'Buscar'}:
            Exibir(Buscar())
        case {'opcao': 'Encerrar'}:
            Clean()
            Write("Encerrando o sistema", 0.2)
            Write(".....", 0.2)
            sleep(1)
            Clean()
            print("Sistema encerrado com sucesso!")
            gambiarra = 0
            return gambiarra
        

def Nome() -> str:
    Clean()
    nome = InquirerPy.prompt([
        {
            'type': 'input',
            'name': 'nome',
            'message': 'Digite o nome do aluno:',
        }
    ])['nome']
    return nome

def Turma() -> str:
    Clean()
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
            Clean()
            turma = [
                {
                    'type': 'list',
                    'name': 'opcao',
                    'message': f'Qual o ano do visitante?',
                    'choices': ['1° INFO', '2° INFO', '3° INFO'],
                }
            ]
            return InquirerPy.prompt(turma)['opcao']
        case {'opcao': 'AGRO'}:
            Clean()
            turma = [
                {
                    'type': 'list',
                    'name': 'opcao',
                    'message': f'Qual o ano do visitante?',
                    'choices': ['1° AGRO', '2° AGRO', '3° AGRO'],
                }
            ]
            return InquirerPy.prompt(turma)['opcao']
        case {'opcao': 'MINE'}:
            Clean()
            turma = [
                {
                    'type': 'list',
                    'name': 'opcao',
                    'message': f'Qual o ano do visitante?',
                    'choices': ['1° MINE', '2° MINE', '3° MINE'],
                }
            ]
            return InquirerPy.prompt(turma)['opcao']
        case {'opcao': 'ADM'}:
            Clean()
            turma = [
                {
                    'type': 'list',
                    'name': 'opcao',
                    'message': f'Qual o ano do visitante?',
                    'choices': ['1° ADM', '2° ADM', '3° ADM'],
                }
            ]
            return InquirerPy.prompt(turma)['opcao']

class Registrar:
    def Entrada():
        Clean()
        nome = Nome()
        turma = Turma()
        x = DB.insert(nome, turma, 'Entrada')
        if x['success']:
            global Save
            Save.append({'nome': nome, 'turma': turma})
            return x
        else:
            print(f"3RR0R: {x['error']}")
            return None

    def Saida():
        Clean()
        choices = [
            {
                'name': f"{visitante['nome']} - {visitante['turma']}",
                'value': visitante 
            }
            for visitante in Save
        ]
        visitante = [
            {
                'type': 'list',
                'name': 'opcao',
                'message': 'Selecione o visitante para registrar saída:',
                'choices': choices,
            }
        ]
        opcao = InquirerPy.prompt(visitante)['opcao']
        if opcao == 'Nenhum visitante registrado':
            input("3RR0R: Nenhum visitante registrado! Registre uma entrada primeiro.")
        else:
            x = DB.insert(opcao['nome'], opcao['turma'], 'Saida')
            if x['success']:
                Save.remove(opcao)
                return x
            else:
                print(f"3RR0R: {x['error']}")
                return None

def data(gambiarra: str) -> str:
    Clean()
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
    Clean()
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

def Buscar() -> list:
    Clean()
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
    return registros

def Listar() -> list:
    Clean()
    now = datetime.now()
    registros = DB.get_all(['2025-01-01', now.date().strftime("%Y-%m-%d")], ['00:00:00', now.time().strftime("%H:%M:%S")])
    return registros

def Exibir(registros: list):
    Clean()
    if not registros:
        print("Nenhum registro encontrado.")
    else:
        for registro in registros:
            print(f"Nome: {registro['nome']} - Turma: {registro['turma']} - Tipo: {registro['tipo']} - {registro['data']} às {registro['hora']}")
    input("Pressione Enter para continuar...")
