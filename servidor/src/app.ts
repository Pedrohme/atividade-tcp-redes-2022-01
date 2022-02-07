import { mkdir } from 'fs';
import net from 'net';
import Stream from 'stream';
import config from './config.json';
import * as Files from './files';
import { RequestStream, RequestActions, RequestHeader } from './request';

const server = net.createServer();

server.on('connection', socket => {
    console.log('Client connected');
    const request = new RequestStream();
    let action: Files.fileAction;

    request.once('gotValidHeader', function routeAction(header: RequestHeader) {
        console.log('Got header');
        switch (header.action) {
            case RequestActions.WriteFile:
                action = new Files.fileWriter();
                (action as Files.fileWriter).Act(() => {
                    console.log(`${(action as Files.fileWriter).fileName} written`);
                    socket.write('201');
                }, request);
                break;

            case RequestActions.ListFiles:
                action = new Files.fileLister();
                (action as Files.fileLister).Act((err, files) => {
                    if (err) {
                        console.log(err.message);
                        socket.write('500');
                        socket.end();
                    }
                    else {
                        const stream = new Stream.Readable({
                            read: () => {
                                const file = files.shift();
                                file ? stream.push(file.padEnd(256, '#')) : stream.push(null);
                            }
                        });
                        stream.pipe(socket);
                    }
                });
                break;

            default:
                break;
        }
    });

    request.once('invalidHeader', function breakConnection() {
        console.log('Got Invalid header');

        socket.write('400');

        socket.end();
    });

    request.once('payloadExceeded', function handleExceededPayload() {
        console.log('Payload too large');
        request.end();

        action.handleError();

        socket.write('413');
        socket.destroy();
    });

    socket.pipe(request);

    socket.on('end', () => {
        console.log("Data stream ended");
    });

    socket.on('close', () => {
        console.log('Connection closed');
    });
});

server.on('error', (err) => {
    throw err;
});

server.listen({ port: config.SERVER_PORT, host: 'localhost' }, () => {
    console.log('Server listening!');
    console.log('');
    const addr = server.address();
    if (addr && (typeof addr !== 'string')) {
        console.log('Server info:');
        console.log(`Address: ${addr.address}`);
        console.log(`Family: ${addr.family}`);
        console.log(`Port: ${addr.port}`);
    }
    console.log('');
});

process.on('SIGINT', function endProgramGracefully() {
    console.log('');
    console.log('Waiting for server to close...');
    console.log('');
    server.close((err) => {
        if (err) {
            console.log(err.message);
            process.exit(1);
        }
        console.log('Server closed!');
    });
});

mkdir('./files', { recursive: true }, (err) => {
    if (!err) {
        console.log('Files directory created');
    }
});