import net from 'net';
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
                action.Act(request);
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

    socket.on('end', async () => {
        console.log("Data stream ended");
    });

    socket.on('close', () => {
        console.log('Connection closed');
    });
});

server.on('error', (err) => {
    throw err;
});

server.listen(config.SERVER_PORT, () => {
    console.log('Server listening!');
});

