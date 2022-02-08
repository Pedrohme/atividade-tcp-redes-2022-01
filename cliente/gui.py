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
while True:
    event, values = window.read()
    # cliente deseja receber arquivo do servidor:
    if event == 'Receber':
        arquivos_servidor = listar_arquivos_servidor()
        sg.popup('Arquivos disponíveis:', *files_list(arquivos_servidor),
                 background_color='white', text_color='black', no_titlebar=True, keep_on_top=True)
        # lista de arquivo(s) desejado(s):
        arquivos_desejados = sg.popup_get_text(
            'Qual arquivo deseja? Para mais de um arquivo, separe-os por vírgula.', background_color='white', text_color='black', no_titlebar=True)
        try:
            arquivos_desejados = [x.strip()
                                  for x in arquivos_desejados.split(',')]
        except AttributeError:
            arquivos_desejados = ['']

        if len(arquivos_desejados) >= 1 and arquivos_desejados[0] != '':
            receber_arquivos(arquivos_desejados)

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
            enviar_arquivos(arquivos_enviados)

    if event == sg.WIN_CLOSED or event == 'Encerrar':
        break

window.close()
