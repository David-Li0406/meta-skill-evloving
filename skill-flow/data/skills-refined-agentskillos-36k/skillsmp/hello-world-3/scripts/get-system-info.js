const os = require('os');

function getOsInfo() {
    return {
        platform: os.platform(),
        type: os.type(),
        release: os.release(),
        arch: os.arch(),
        hostname: os.hostname(),
        cpuCount: os.cpus().length,
        cpuModels: os.cpus().map(c => c.model),
        totalMemory: os.totalmem(),
        freeMemory: os.freemem(),
        uptimeSeconds: os.uptime()
    };
}

const asciiHelloWorld = [
    ' _   _      _ _         __        __         _     _ ',
    '| | | | ___| | | ___    \\ \\      / /__  _ __| | __| |',
    '| |_| |/ _ \\ | |/ _ \\    \\ \\ /\\ / / _ \\| \'__| |/ _` |',
    '|  _  |  __/ | | (_) |    \\ V  V / (_) | |  | | (_| |',
    '|_| |_|\\___|_|_|\\___/      \\_/\\_/ \\___/|_|  |_|\\__,_|',
].join('\n');

console.log(asciiHelloWorld);
console.log('\nSystem Information:');
console.log(JSON.stringify(getOsInfo(), null, 2));
