const https = require('https');
const path = require('path');
const dotenvx = require('@dotenvx/dotenvx');

// Load env quietly using dotenvx
const envPath = path.join(__dirname, '../../../../.env');
dotenvx.config({ path: envPath, quiet: true });

const apiKey = process.env.KAGI_API_KEY;
if (!apiKey) {
    console.error("Error: KAGI_API_KEY not found in .env");
    process.exit(1);
}

const query = process.argv[2];
if (!query) {
    console.error("Usage: node fastgpt.cjs <query> [--confirm]");
    process.exit(1);
}

// Cost Safeguard
if (!process.argv.includes('--confirm')) {
    console.warn("⚠️  KAGI COST WARNING: FastGPT queries use API credits.");
    console.warn("   To proceed, please re-run the command with the '--confirm' flag.");
    process.exit(0);
}

const options = {
    hostname: 'kagi.com',
    path: '/api/v0/fastgpt',
    method: 'POST',
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
                // Output clean JSON for the caller
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

req.write(JSON.stringify({ query: query }));
req.end();
