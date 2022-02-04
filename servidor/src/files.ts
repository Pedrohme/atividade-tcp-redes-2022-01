import fs from "fs";

export function writeToFile(buffer: Buffer) {
    const fileName = buffer.slice(1, 257).toString().split('#')[0];

    console.log(fileName);

    var dir = './files';

    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir);
    }

    fs.writeFileSync(`${dir}/${fileName}`, buffer.slice(256));
}
