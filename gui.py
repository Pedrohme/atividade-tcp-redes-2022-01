import PySimpleGUI as sg

def files_list(list_name):
    if len(list_name) == 0:
        return 'Não há arquivos no servidor'

    return [item for item in list_name]

FILMS = [
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
        arquivo_desejado = sg.popup_get_text('Qual arquivo deseja?', background_color='white', text_color='black', no_titlebar=True)

    if event == 'Listagem':
        sg.popup('Arquivos presentes no servidor:', *files_list(FILMS), background_color='white', text_color='black', no_titlebar=True, keep_on_top=True)    #trocar a lisat passada como parâmetro

    if event == 'Enviar':
        sg.popup_get_file('Insira o arquivo:', background_color='white', text_color='black', no_titlebar=True)

    if event == sg.WIN_CLOSED or event == 'Encerrar':
        break

window.close()