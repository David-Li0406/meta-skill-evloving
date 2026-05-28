const https = require('https');
const fs = require('fs');
const path = require('path');
const dotenvx = require('@dotenvx/dotenvx');

// Load env quietly
const envPath = path.join(__dirname, '../../../../.env');
dotenvx.config({ path: envPath, quiet: true });

const apiKey = process.env.KAGI_API_KEY;
if (!apiKey) {
    console.error("Error: KAGI_API_KEY not found in .env");
    process.exit(1);
}

// Check for --url argument
const args = process.argv.slice(2);
let url = '';
let engine = 'muriel';
let summaryType = 'summary';

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--url') {
        url = args[i + 1];
        i++;
    } else if (args[i] === '--engine') {
        engine = args[i + 1];
        i++;
    } else if (args[i] === '--type') {
        summaryType = args[i + 1];
        i++;
    } else if (!url) {
        url = args[i]; // Fallback if no flag used
    }
}

if (!url) {
    console.error("Usage: node summarize.cjs --url <url> [--confirm] [--engine <muriel|cecil>]");
    process.exit(1);
}

// Cost Safeguard
if (!process.argv.includes('--confirm')) {
    console.warn("⚠️  KAGI COST WARNING: Universal Summarizer uses API credits.");
    console.warn("   To proceed, please re-run the command with the '--confirm' flag.");
    process.exit(0);
}

const apiUrl = `https://kagi.com/api/v0/summarize?url=${encodeURIComponent(url)}&engine=${engine}&summary_type=${summaryType}`;

const options = {
    method: 'GET',
    headers: {
        'Authorization': `Bot ${apiKey}`,
        'Content-Type': 'application/json'
    }
};

console.error(`Summarizing ${url} using ${engine}...`);

const req = https.request(apiUrl, options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
        data += chunk;
    });

    res.on('end', () => {
        if (res.statusCode === 200) {
            try {
                const json = JSON.parse(data);
                // Output just the data part to stdout for chaining, or formatted text
                if (json.data && json.data.output) {
                    console.log(json.data.output);
                } else {
                    console.log(JSON.stringify(json, null, 2));
                }
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
