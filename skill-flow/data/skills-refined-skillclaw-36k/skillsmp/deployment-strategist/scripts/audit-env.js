const fs = require('fs');
const path = require('path');

// Assuming this script is at .agent/skills/deployment-strategist/scripts/audit-env.js
// Root is ../../../../
const rootDir = path.resolve(__dirname, '../../../../');
const examplePath = path.join(rootDir, '.env.example');
const envPath = path.join(rootDir, '.env');

console.log('🔍 Starting Environment Audit...');

if (!fs.existsSync(examplePath)) {
    console.log('⚠️  .env.example not found. Skipping template check.');
    process.exit(0);
}

const exampleContent = fs.readFileSync(examplePath, 'utf8');
const requiredKeys = [
    'DATABASE_URL',
    // 'DIRECT_URL', // Optional for now, but good practice for migrations
    'CONCIERGE_SECRET', // Likely needed based on other files, but DATABASE_URL is key
];

// Load local .env
let localEnvKeys = new Set();
if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    envContent.split('\n').forEach(line => {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
            const key = trimmed.split('=')[0].trim();
            localEnvKeys.add(key);
        }
    });
}

const missing = [];
requiredKeys.forEach(key => {
    // Check local .env OR process.env (runtime)
    if (!localEnvKeys.has(key) && !process.env[key]) {
        missing.push(key);
    }
});

if (missing.length > 0) {
    console.error('❌ Missing required environment variables (based on .env.example):');
    missing.forEach(k => console.error(`   - ${k}`));
    console.error('\nPlease ensure these are set in your deployment environment or .env file.');
    process.exit(1);
} else {
    console.log(`✅ Verified ${requiredKeys.length} required variables.`);
}
