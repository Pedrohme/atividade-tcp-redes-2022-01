import fs from "fs";
import Stream from "stream";

const fileDir = './files/';

export abstract class fileAction {
    public abstract Act(stream: Stream.Readable): any;
    public abstract handleError(): any;
}

export class fileWriter extends fileAction {
    public fileName: string;
    public written: boolean;

    constructor() {
        super();

        this.fileName = fileDir;
        this.written = false;
    }

    public Act(stream: Stream.Readable) {
        const thisFileWriter = this;

        stream.on('readable', function getFileName() {
            let readStream: Buffer | null = null;
            if ((readStream = stream.read(256)) !== null) {
                thisFileWriter.fileName += readStream.toString().split('#')[0];
                stream.removeListener('readable', getFileName);
                stream.emit('gotName');
            }
        });

        stream.once('gotName', function writeFile() {
            thisFileWriter.written = true;
            console.log(`Writing ${thisFileWriter.fileName}`);
            const fileStream = fs.createWriteStream(thisFileWriter.fileName);
            stream.pipe(fileStream).on('finish', () => {
                console.log(`${thisFileWriter.fileName} written to disk!`);
            });
        });
    }

    public handleError() {
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
