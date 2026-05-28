
import http from 'http';

const req = http.request('http://localhost:3000', { method: 'HEAD' }, (res) => {
    console.log(`STATUS: ${res.statusCode}`);
    if (res.statusCode && res.statusCode >= 200 && res.statusCode < 400) {
        process.exit(0);
    } else {
        process.exit(1);
    }
});

req.on('error', (e) => {
    console.error(`problem with request: ${e.message}`);
    process.exit(1);
});

req.end();
