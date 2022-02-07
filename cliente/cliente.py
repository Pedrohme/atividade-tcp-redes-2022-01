# script do cliente, que se conecta ao servidor e informa as ações desejadas pelo usuário

import os, socket, pathlib

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8124        # The port used by the server

# função que conecta ao servidor e retorna a conexão:
def conectar_com_servidor():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    return cliente

# função que informa ao servidor o(s) arquivo(s) a ser(em) enviado(s) para o cliente:
def receber_arquivos(arquivos_desejados):
    cliente = conectar_com_servidor()

    action = 'C'
    payloadSize = ''.ljust(256, '#')

    for arq in arquivos_desejados:
        fileName = arq.ljust(256, '#')
        header = action + payloadSize + fileName
        encoded = str.encode(header)
        cliente.sendall(encoded)

# função que informa ao servidor que o cliente deseja visualizar os arquivos existentes no servidor:
def listar_arquivos_servidor():
    cliente = conectar_com_servidor()

    action = 'B'
    payloadSize = '0'.ljust(15, '#')

    header = action + payloadSize
    encoded = str.encode(header)
    cliente.sendall(encoded)
    arquivos = cliente.recv(1024)

    return arquivos

# função que informa ao servidor o(s) arquivo(s) a ser(em) enviado(s) pelo cliente:
def enviar_arquivos(arquivos):
    action = 'A'
    for arq in arquivos:
        cliente = conectar_com_servidor()
        
        payloadSize = str(os.path.getsize(arq) + 256).ljust(15, '#')
        fileName = pathlib.PurePath(arq).name.ljust(256, '#')
        header = action + payloadSize + fileName
        encoded = str.encode(header)
        
        cliente.sendall(encoded)
        
        file = open(arq, 'rb')
        buffer = file.read(1024)
        while (buffer):
            print('Sending...')
            cliente.sendall(buffer)
            buffer = file.read(1024)
        file.close()
        print("Done Sending")