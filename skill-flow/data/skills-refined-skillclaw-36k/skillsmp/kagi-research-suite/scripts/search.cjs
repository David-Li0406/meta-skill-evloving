const https = require('https');
const fs = require('fs');
const path = require('path');
// Manual .env parsing to avoid dotenv logging
const envPath = path.join(__dirname, '../../../../.env');
let apiKey = process.env.KAGI_API_KEY;

if (!apiKey && fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf-8');
    const match = envContent.match(/^KAGI_API_KEY=(.+)$/m);
    if (match) {
        apiKey = match[1].trim();
    }
}

if (!apiKey) {
    console.error("Error: KAGI_API_KEY not found in .env or environment");
    process.exit(1);
}

const query = process.argv[2];
if (!query) {
    console.error("Usage: node search.js <query>");
    process.exit(1);
}

const options = {
    hostname: 'kagi.com',
    path: `/api/v0/search?q=${encodeURIComponent(query)}&limit=10`,
    method: 'GET',
    headers: {
        'Authorization': `Bot ${apiKey}`,
        'Content-Type': 'application/json'
    }
};

const req = https.request(options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
        data += chunk;
    });

    res.on('end', () => {
        if (res.statusCode === 200) {
            try {
                const json = JSON.parse(data);
                console.log(JSON.stringify(json.data, null, 2));
            } catch (e) {
                console.error("Error parsing response:", e);
                console.log(data);
            }
        } else {
            console.error(`Request failed with status: ${res.statusCode}`);
            console.log(data);
        }
    });
});

req.on('error', (e) => {
    console.error(`Problem with request: ${e.message}`);
});

req.end();
