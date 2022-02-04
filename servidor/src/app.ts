import net from 'net';
import config from './config.json';
import { writeToFile } from './files';

enum Options {
    A,
    B,
    C
}

const server = net.createServer((socket) => {
    console.log('Cliente Conectou!');

    let first = true;
    let option = '';
    let buffers: Buffer[] = [];

    socket.on('data', (data) => {
        if (first) {
            first = false;
            const firstByteChar = String.fromCharCode(data[0]);

            if (Object.keys(Options).includes(firstByteChar)) {
                option = firstByteChar;
            }
            else {
                socket.write("Requisição inválida!");
                socket.destroy();
            }
        }
        buffers.push(data);
    });

    socket.on('end', () => {
        switch (option) {
            case 'A':
                const buf = Buffer.concat(buffers);
                writeToFile(buf);
                break;
            case 'B':

                break;
            case 'C':

                break;

            default:
                break;
        }
    });

    socket.on('close', () => {
        console.log('Conexão fechada!');
    });
});

server.on('error', (err) => {
    throw err;
});

server.listen(config.SERVER_PORT, () => {
    console.log('Servidor escutando!');
});

