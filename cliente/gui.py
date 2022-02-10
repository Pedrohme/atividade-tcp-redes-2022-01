# script da interface gráfica, meio de interação com o servidor

import PySimpleGUI as sg
from cliente import receber_arquivos, listar_arquivos_servidor, enviar_arquivos

# função que retorna todos os elementos de uma lista


def files_list(list_name):
    if len(list_name) == 0:
        vazio = []
        vazio.append('Não há arquivos no servidor')
        return vazio

    return [item for item in list_name]


# layout da janela principal da GUI
layout = [
    [sg.Text('Bem-vindo(a) ao Servidor TCP!')],
    [sg.Text('O que deseja fazer?')],
    [sg.Button('Solicitar arquivo', size=(20, 2), key='Receber')],
    [sg.Button('Listar arquivos', size=(20, 2), key='Listagem')],
    [sg.Button('Enviar arquivo', size=(20, 2), key='Enviar')],
    [sg.Button('Encerrar', button_color=('white', 'red'), size=(10, 2))]
]

# criando janela principal e recebendo seus eventos (interações com os botões)
window = sg.Window('Servidor TCP', layout, margins=(
    120, 180), element_justification='c', element_padding=(0, 5))

win_receber_active = False

while True:
    event, values = window.read()

    # cliente deseja receber arquivo do servidor:
    if event == 'Receber' and not win_receber_active:
        arquivos_servidor = listar_arquivos_servidor()

        win_receber_active = True
        window.hide()

        layout2 = [[sg.Text('Selecione os arquivos a receber')]]

        for arq in arquivos_servidor:
            layout2.append([sg.Checkbox(arq, key=arq)])

        layout2.append([sg.Submit('Receber')])

        win_receber = sg.Window('Receber Arquivos', layout2)
        while True:
            ev2, vals2 = win_receber.Read()
            if ev2 == sg.WIN_CLOSED:
                win_receber.Close()
                win_receber_active = False
                window.UnHide()
                break

            elif ev2 == 'Receber':
                selecionados = []
                for key, value in vals2.items():
                    if (value):
                        selecionados.append(key)

                if len(selecionados) >= 1 and selecionados[0] != '':
                    window.perform_long_operation(lambda: receber_arquivos(
                        arquivos_servidor, selecionados), 'receber-arquivos')
                    win_receber.Close()
                    win_receber_active = False
                    window.UnHide()
                    sg.popup('Recebendo...', auto_close=True, no_titlebar=True,
                             background_color='white', text_color='black')

    # cliente deseja visualizar todos os arquivos presentes no servidor:
    if event == 'Listagem':
        arquivos_servidor = listar_arquivos_servidor()
        sg.popup('Arquivos presentes no servidor:', *files_list(arquivos_servidor),
                 background_color='white', text_color='black', no_titlebar=True, keep_on_top=True)

    # cliente deseja enviar arquivo(s) ao servidor:
    if event == 'Enviar':
        arquivos_enviados = sg.popup_get_file(
            'Insira o arquivo:', background_color='white', text_color='black', no_titlebar=True, multiple_files=True)
        # criando lista de arquivo(s) a ser(em) enviado(s):
        try:
            arquivos_enviados = arquivos_enviados.split(';')
        except AttributeError:
            arquivos_enviados = ['']

        if len(arquivos_enviados) >= 1 and arquivos_enviados[0] != '':
            window.perform_long_operation(lambda: enviar_arquivos(
                arquivos_enviados), 'arquivos-enviados')
            sg.popup('Enviando...', auto_close=True, no_titlebar=True,
                     background_color='white', text_color='black')

    if event == 'arquivos-enviados':
        sg.popup('Enviado!', auto_close=True, no_titlebar=True,
                 background_color='white', text_color='black')
    if event == 'receber-arquivos':
        sg.popup('Recebido!', auto_close=True, no_titlebar=True,
                 background_color='white', text_color='black')

    if event == sg.WIN_CLOSED or event == 'Encerrar':
        break

window.close()
