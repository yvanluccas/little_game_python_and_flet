import flet as ft
import random, time, re

def main(page: ft.Page):
    page.title = "Jogos de Adivinhação e Operações Numéricas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def login(e):
        global nome
        nome = nickname.value
        if not nome.startswith('@'):
            nickname.error_text = 'Insira um nickname válido\n(Deve começar com @).'
            page.update()
        else: 
            page.clean()
            primeira_fase(page)

    global tela_inicial
    def tela_inicial(e):
        global nickname
        page.clean()
        nickname = ft.TextField(label="@nickname", width=220, border_radius=20)
        page.add(
            nickname,
            ft.ElevatedButton("Avançar", on_click=login, color='black', bgcolor='#A5EA4F')
        )

    def ranking(e):
        page.clean()
        page.add(ft.ElevatedButton('Ranking Jogo de Adivinhação', on_click=ranking1, bgcolor='#FFCDD3', color='red'))
        page.add(ft.ElevatedButton('Ranking Jogo de Operações Numéricas', on_click=ranking2, bgcolor='#E2F3FD', color='blue'))

    def ranking1(e):
        page.clean()
        ranking_adivinhacao(page)

    def ranking2(e):
        page.clean()
        ranking_operacoes(page)
        
    global voltar
    def voltar(e):
        page.clean()
        page.add(
            ft.ElevatedButton('Jogar', on_click=tela_inicial, color='black', bgcolor='#A5EA4F'),
            ft.ElevatedButton('Ranking', on_click=ranking, color='black', bgcolor='#F7CD23')
        )

    page.add(
        ft.ElevatedButton('Jogar', on_click=tela_inicial, color='black', bgcolor='#A5EA4F')
    )
    page.add(
        ft.ElevatedButton('Ranking', on_click=ranking, color='black', bgcolor='#F7CD23')
    )

def primeira_fase(page: ft.Page):
    page.title = "Jogo de Adivinhação"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(ft.Text(f"Bem-vindo à primeira fase, {nome}!", size=35, weight='bold'))
    time.sleep(3)
    page.clean()
    page.add(ft.Text("Na primeira fase, você terá que adivinhar um número\nentre 1 e 100 com o mínimo de tentativas possíveis.",
                    size=28,
                    font_family='Consolas',
                    weight='BOLD'))
    time.sleep(5)
    numero = random.randint(0,100)
    tentativas = 0
    def verificar_palpite(e):
        global palpites
        nonlocal tentativas
        try:
            palpite = int(entrada_palpite.value)
        except ValueError:
            page.add(ft.Text("Por favor, digite um número válido."))
            page.update()
            return
        global palpites
        tentativas += 1
        palpites = tentativas

        if palpite < numero:
            page.add(ft.Text(f"Tente um número maior. Tentativas: {tentativas}"))
        elif palpite > numero:
            page.add(ft.Text(f"Tente um número menor. Tentativas: {tentativas}"))
        else:
            page.add(ft.Text(f"Parabéns! Você adivinhou o número em {tentativas} tentativa(s).", 
                             size=15, 
                             weight='bold'))
            time.sleep(6)
            arquivo_ranking_1()
            passar_para_segunda_fase(page)

    entrada_palpite = ft.TextField(label="Seu palpite:", 
                                   width=120, 
                                   border_radius=20, 
                                   border_color='black')

    page.add(
        entrada_palpite,
        ft.ElevatedButton("Verificar", on_click=verificar_palpite, bgcolor='#FFCDD3', color='black'))

def passar_para_segunda_fase(page: ft.Page):
    page.clean()
    segunda_fase(page)

def segunda_fase(page: ft.Page):
    page.title = "Jogo de Operações Numéricas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(ft.Text("Bem-vindo à segunda fase!", 
                    size=35,
                    weight='bold'))
    time.sleep(3)
    page.clean()
    page.add(ft.Text('Nessa fase, você deve realizar o máximo de operações de soma\ne subtração em 1 minuto. Quanto mais acertos, maior a pontuação.',
                    size=27,
                    font_family='Consolas',
                    weight='BOLD'))
    time.sleep(7)
    tempo_limite = 60
    tempo_inicio = time.time()
    pontuacao = 0

    def realizar_operacao():
        nonlocal pontuacao
        num1 = random.randint(1, 10)
        num2 = random.randint(2, 9)
        operador = random.choice(['+', '-'])

        expressao = f"{num1} {operador} {num2}"
        if operador == '-':
            expressao = f"{num1} - {num2}"

        page.add(ft.Text(f"Quanto é {expressao}?",
                        size=18,
                        font_family='Consolas',
                        weight='BOLD'))

        resposta_usuario = ft.TextField(label="Sua resposta:", 
                                        width=150, 
                                        border_radius=20, 
                                        border_color='black')
        page.add(resposta_usuario)
        botao_verificar = ft.ElevatedButton(
            "Verificar",
            on_click=lambda e: verificar_resposta(resposta_usuario, expressao), 
            bgcolor='#E2F3FD', color='black')
        page.add(botao_verificar)

    def verificar_resposta(resposta_usuario, expressao):
        global acertos
        nonlocal pontuacao
        resposta_usuario_value = resposta_usuario.value.strip()

        if not resposta_usuario_value or not re.match(r'^[-+]?[0-9]+$', resposta_usuario_value):
            page.add(ft.Text("Digite uma resposta válida."))
            return

        try:
            resposta_correta = eval(expressao)
            if int(resposta_usuario_value) == resposta_correta:
                pontuacao += 1
        except Exception as ex:
            print(f"Erro ao avaliar expressão: {ex}")

        page.clean()
        page.add(ft.Text(f"Pontuação: {pontuacao}",
                        size=18,
                        font_family='Consolas'))
        acertos = pontuacao
        realizar_operacao()

    realizar_operacao()

    while time.time() - tempo_inicio < tempo_limite:
        time.sleep(3)
    arquivo_ranking_2()

    def voltar_para_o_inicio(e):
        page.clean()
        main(page)

    page.clean()
    page.add(ft.Text(f"Tempo esgotado! Você realizou {pontuacao} operações corretamente.",
                    weight='bold',
                    size=20,
                    font_family='Consolas'))
    page.add(ft.ElevatedButton("Voltar para o ínicio", on_click=voltar_para_o_inicio, bgcolor='#FFCDD3', color='black'))

def arquivo_ranking_1():
    with open('ranking.csv', 'r', encoding='utf-8') as ranking:
        lista_nicknames = []
        lista_pontuacoes = []
        dicionario = {}
        for item in ranking:
            item = item.split(',')
            lista_nicknames.append(item[0])
            lista_pontuacoes.append(item[1])
            dicionario[item[0]] = int(item[1])

    if nome in lista_nicknames:
        if palpites < dicionario[nome]:
            dicionario[nome] = palpites        
    else:
        dicionario[nome] = palpites

    with open('ranking.csv', 'w', encoding='utf-8') as ranking:
        for item in dicionario:
            ranking.write(f'{item},{dicionario[item]}\n')

    dicionario_ordenado = sorted(dicionario.items(), key=lambda x: x[1])
    return dicionario_ordenado

def arquivo_ranking_2():
    global dicionario_ordenado2
    with open('ranking2.csv', 'r', encoding='utf-8') as ranking:
        lista_nicknames = []
        lista_pontuacoes = []
        dicionario = {}
        for item in ranking:
            item = item.split(',')
            lista_nicknames.append(item[0])
            lista_pontuacoes.append(item[1])
            dicionario[item[0]] = int(item[1])

    if nome in lista_nicknames:
        if acertos > dicionario[nome]:
            dicionario[nome] = acertos        
    else:
        dicionario[nome] = acertos

    with open('ranking2.csv', 'w', encoding='utf-8') as ranking:
        for item in dicionario:
            ranking.write(f'{item},{dicionario[item]}\n')

    dicionario_ordenado2 = sorted(dicionario.items(), key=lambda x: x[1], reverse=True)
    return dicionario_ordenado2

def ranking_adivinhacao(page: ft.Page):
    with open('ranking.csv', 'r', encoding='utf-8') as ranking1:
        bd = []
        dados = [linha.split(',') for linha in ranking1]
        for info in dados:
            bd.append({'nome': info[0], 'pontuacao': int(info[1])})

        def ordem(lista):
            return lista['pontuacao']

        cadastro_ordenados = sorted(bd,key=ordem)

        page.title = "Ranking Jogo de Adivinhação"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.add(ft.Text(value='Jogo de Adivinhação',color='red',size=35,weight='BOLD',font_family='Consolas'))
        page.add(
            ft.DataTable(
                bgcolor='#F0534F',
                border_radius=6,
                border=ft.border.all(2, "black"),
                heading_row_color='#E67373',
                horizontal_lines=ft.border.BorderSide(1, "black"),
                columns=[
                    ft.DataColumn(ft.Text("Posição", weight='bold')),
                    ft.DataColumn(ft.Text('Nickname', weight='bold')),
                    ft.DataColumn(ft.Text("Tentativas", weight='bold'), numeric=True,),
                ],
                rows=[ft.DataRow(cells=data_line(id+1, cad)) for id, cad in enumerate(cadastro_ordenados)],
            ),
        )

        page.add(ft.ElevatedButton('Jogar', on_click=tela_inicial, bgcolor='#FFCDD3', color='red'))
        page.add(ft.ElevatedButton('Voltar para o início', on_click=voltar, bgcolor='#FFCDD3', color='red'))

def data_line(posicao, cadastro):
    return [
            ft.DataCell(ft.Text(posicao, weight='bold')),
            ft.DataCell(ft.Text(cadastro['nome'], weight='bold')),
            ft.DataCell(ft.Text(cadastro['pontuacao'], weight='bold')),
        ]

def ranking_operacoes(page: ft.Page):
        with open('ranking2.csv', 'r', encoding='utf-8') as ranking1:
            bd = []
            dados = [linha.split(',') for linha in ranking1]
            for info in dados:
                bd.append({'nome': info[0], 'pontuacao': int(info[1])})

            def ordem(lista):
                return lista['pontuacao']

            cadastro_ordenados = sorted(bd,key=ordem,reverse=True)

            page.title = "Ranking Jogo de Operações Numéricas"
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            page.add(ft.Text(value='Jogo de Operações Numéricas',color='blue',size=35,weight='BOLD',font_family='Consolas'))
            page.add(
                ft.DataTable(
                    bgcolor='blue',
                    border_radius=6,
                    border=ft.border.all(2, "black"),
                    heading_row_color='#63B5F7',
                    horizontal_lines=ft.border.BorderSide(1, "black"),
                    columns=[
                        ft.DataColumn(ft.Text("Posição", weight='bold')),
                        ft.DataColumn(ft.Text("Nickname", weight='bold')),
                        ft.DataColumn(ft.Text("Pontuação", weight='bold'), numeric=True),
                    ],
                    rows=[ft.DataRow(cells=data_line(id+1,cad)) for id,cad in enumerate(cadastro_ordenados)],
                ),
            )
        
        page.add(ft.ElevatedButton('Jogar', on_click=tela_inicial, bgcolor='#E2F3FD', color='blue'))
        page.add(ft.ElevatedButton('Voltar para o início', on_click=voltar, bgcolor='#E2F3FD', color='blue'))