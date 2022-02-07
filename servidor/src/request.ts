import Stream from "stream";

export const headerSize = 16;

export class RequestStream extends Stream.Transform {
    private header: RequestHeader;
    private payloadTotalSize: number;

    constructor(options?: Stream.TransformOptions) {
        if (options) options.decodeStrings = false;
        super(options);

        this.header = new RequestHeader();
        this.payloadTotalSize = -headerSize;
    }

    _transform(chunk: Buffer, encoding: BufferEncoding, callback: Stream.TransformCallback): void {
        this.push(chunk);
        this.payloadTotalSize += chunk.byteLength;
        if (!this.header.valid && this.readableLength >= 16) {
            const buffer: Buffer = this.read(16);
            if (buffer) {
                this.header.parseHeader(buffer);

                this.header.valid ? this.emit('gotValidHeader', this.header) : this.emit('invalidHeader', this.header);
            }
            else {
                throw new Error("Stream buffer read error");
            }
        }
        if (this.header.valid && this.payloadTotalSize > this.header.payloadSize) {
            this.emit('payloadExceeded');
        }
        callback();
    }

    public getHeader(): RequestHeader {
        return this.header;
    }
}

export class RequestHeader {
    public action: RequestActions;
    public payloadSize: number;
    public valid: boolean;

    constructor() {
        this.valid = false;
        this.action = RequestActions.WriteFile;
        this.payloadSize = 0;
    }

    public parseHeader(buffer: Buffer) {
        this.valid = true;

        const firstByteChar = String.fromCharCode(buffer[0]);

        Object.values(RequestActions).includes(firstByteChar as RequestActions) ? this.action = (firstByteChar as RequestActions) : this.valid = false;

        this.payloadSize = parseInt(buffer.slice(1, 16).toString().split('#')[0]);
        if (isNaN(this.payloadSize)) this.valid = false;
    }
}

export enum RequestActions {
    WriteFile = "A",
    ListFiles = "B",
    SendFile = "C",
}