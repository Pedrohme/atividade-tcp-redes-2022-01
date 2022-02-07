import fs from "fs";
import Stream from "stream";

const fileDir = './files';

export abstract class fileAction {
    public abstract Act(callback: () => unknown, stream?: Stream.Readable): unknown;
    public abstract handleError(): unknown;
}

export class fileWriter extends fileAction {
    public fileName: string;
    public written: boolean;

    constructor() {
        super();

        this.fileName = '';
        this.written = false;
    }

    public Act(callback: (() => unknown), stream: Stream.Readable): void {
        const thisFileWriter = this;

        stream.on('readable', function getFileName() {
            let readStream: Buffer | null = null;
            if ((readStream = stream.read(256)) !== null) {
                thisFileWriter.fileName = readStream.toString().split('#')[0];
                stream.removeListener('readable', getFileName);
                stream.emit('gotName');
            }
        });

        stream.once('gotName', function writeFile() {
            thisFileWriter.written = true;
            console.log(`Writing ${thisFileWriter.fileName}`);

            const fileStream = fs.createWriteStream(`${fileDir}/${thisFileWriter.fileName}`);
            stream.pipe(fileStream).on('finish', () => {
                callback();
            });
        });
    }

    public handleError(): void {
        if (this.written) {
            fs.rm(this.fileName, (err) => {
                if (err) {
                    console.log('Error undoing file write');
                    console.log(err);
                }
                else {
                    console.log('File write undone');
                }
            });
        }
    }
}

export class fileLister extends fileAction {
    constructor() {
        super();
    }

    public Act(callback: (err: NodeJS.ErrnoException | null, files: string[]) => void, stream?: Stream.Readable): void {
        fs.readdir(fileDir, callback);
    }

    public handleError(): void {
        return;
    }
}

export class fileReader extends fileAction {
    constructor() {
        super();
    }

    public Act(callback: (fileReadStream: Stream.Readable) => void, stream: Stream.Readable): void {
        let fileName = '';

        stream.on('readable', function getFileName() {
            let readStream: Buffer | null = null;
            if ((readStream = stream.read(256)) !== null) {
                fileName = readStream.toString().split('#')[0];
                stream.removeListener('readable', getFileName);
                stream.emit('gotName');
            }
        });

        stream.once('gotName', function writeFile() {
            console.log(`Reading ${fileName}`);

            fs.createReadStream(`${fileDir}/${fileName}`).on('ready', callback);
        });
    }

    public handleError(): void {
        return;
    }
}
