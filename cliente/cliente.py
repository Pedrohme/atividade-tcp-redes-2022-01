# script do cliente, que se conecta ao servidor e informa as ações desejadas pelo usuário

import os
import socket
import pathlib

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8124        # The port used by the server
BUFFERSIZE = 32768

# função que conecta ao servidor e retorna a conexão:


def conectar_com_servidor():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    return cliente

# função que informa ao servidor o(s) arquivo(s) a ser(em) enviado(s) para o cliente:


def receber_arquivos(arquivos_servidor, arquivos_desejados):
    for arq in arquivos_desejados:
        if arq in arquivos_servidor:
            cliente = conectar_com_servidor()

            action = 'C'
            payloadSize = '256'.ljust(15, '#')

            os.makedirs('./files', exist_ok=True)
            arquivos_existentes_cliente = os.listdir('./files')

            if arq not in arquivos_existentes_cliente:
                fileName = arq.ljust(256, '#')
                header = action + payloadSize + fileName
                encoded = str.encode(header)
                cliente.sendall(encoded)

                with open('./files/{}'.format(arq), 'ab') as f:
                    while True:
                        print('Receiving...')
                        chunk = cliente.recv(BUFFERSIZE)
                        if not chunk:
                            break
                        f.write(chunk)
                    print('Done Receiving')
            else:
                print("File {} already exists in client's folder.".format(arq))


# função que informa ao servidor que o cliente deseja visualizar os arquivos existentes no servidor:


def listar_arquivos_servidor():
    cliente = conectar_com_servidor()

    action = 'B'
    payloadSize = '0'.ljust(15, '#')

    header = action + payloadSize
    encoded = str.encode(header)
    cliente.sendall(encoded)

    arr = recvall(cliente).decode()

    arquivos = [arr[i:i+256].split('#')[0] for i in range(0, len(arr), 256)]

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
        buffer = file.read(BUFFERSIZE)
        while (buffer):
            print('Sending...')
            cliente.sendall(buffer)
            buffer = file.read(BUFFERSIZE)
        file.close()
        print("Done Sending")

        arr = recvall(cliente).decode()
        if (arr == '201'):
            print('Arquivo enviado com sucesso!')


def recvall(cliente):
    fragments = []
    while True:
        chunk = cliente.recv(BUFFERSIZE)
        if not chunk:
            break
        fragments.append(chunk)
    arr = b''.join(fragments)
    return arr
