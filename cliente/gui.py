import PySimpleGUI as sg

def files_list(list_name):
    if len(list_name) == 0:
        return 'Não há arquivos no servidor'

    return [item for item in list_name]

FILES = [
    "There will be blood", "Paul Thomas Anderson",
    "Lion King","Rob Minkoff",
    "Toy Story","Josh Cooley",
    "Monty Python's Life of Brian","Terry Jones",
    "Die Hard","John McTiernan",
    "Rocky","John G. Avildsen",
]

layout = [
    [sg.Text('Bem-vindo(a) ao Servidor TCP!')],
    [sg.Text('O que deseja fazer?')],
    [sg.Button('Solicitar arquivo', size=(20,2), key='Receber')],
    [sg.Button('Listar arquivos', size=(20,2), key='Listagem')],
    [sg.Button('Enviar arquivo', size=(20,2), key='Enviar')],
    [sg.Button('Encerrar', button_color=('white', 'red'), size=(10,2))]
]

window = sg.Window('Servidor TCP', layout, margins=(120, 180), element_justification='c', element_padding=(0,5))
while True:
    event, values = window.read()
    if event == 'Receber':
        sg.popup('Arquivos disponíveis:', *files_list(FILES), background_color='white', text_color='black', no_titlebar=True, keep_on_top=True)    #trocar a lisat passada como parâmetro
        arquivos_desejados = sg.popup_get_text('Qual arquivo deseja? Para mais de um arquivo, separe-os por vírgula.', background_color='white', text_color='black', no_titlebar=True)
        try:
            arquivos_desejados = [x.strip() for x in arquivos_desejados.split(',')]
        except AttributeError:
            arquivos_desejados = ['']

    if event == 'Listagem':
        sg.popup('Arquivos presentes no servidor:', *files_list(FILES), background_color='white', text_color='black', no_titlebar=True, keep_on_top=True)    #trocar a lisat passada como parâmetro

    if event == 'Enviar':
        arquivos_enviados = sg.popup_get_file('Insira o arquivo:', background_color='white', text_color='black', no_titlebar=True, multiple_files=True)
        try:
            arquivos_enviados = arquivos_enviados.split(';')
        except AttributeError:
            arquivos_enviados = ['']

    if event == sg.WIN_CLOSED or event == 'Encerrar':
        break

window.close()
