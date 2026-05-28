import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const projectRoot = path.resolve(__dirname, '../../..');

// Load env vars
const envLocalPath = path.resolve(projectRoot, '.env.local');
const envPath = path.resolve(projectRoot, '.env');

console.log('Loading environment from:', projectRoot);

if (fs.existsSync(envLocalPath)) {
    console.log('Loading .env.local...');
    dotenv.config({ path: envLocalPath });
} else {
    console.log('⚠️ .env.local not found');
}

if (fs.existsSync(envPath)) {
    console.log('Loading .env...');
    dotenv.config({ path: envPath });
} else {
    console.log('⚠️ .env not found');
}

const REQUIRED_VARS = [
    'SUPABASE_URL',
    'SUPABASE_SERVICE_ROLE_KEY',
    'GOOGLE_SERVICE_ACCOUNT_EMAIL',
    'GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY'
];

const OPTIONAL_VARS = [
    'VITE_SUPABASE_URL',
    'VITE_SUPABASE_ANON_KEY',
    'PAYPAL_CLIENT_ID',
    'PAYPAL_CLIENT_SECRET'
];

let missing = [];
let warnings = [];

REQUIRED_VARS.forEach(key => {
    if (!process.env[key]) {
        missing.push(key);
    }
});

OPTIONAL_VARS.forEach(key => {
    if (!process.env[key]) {
        warnings.push(key);
    }
});

console.log('\n--- Environment Check Results ---');

if (missing.length > 0) {
    console.error('❌ Missing REQUIRED variables:');
    missing.forEach(key => console.error(`   - ${key}`));
    process.exit(1);
} else {
    console.log('✅ All REQUIRED variables found.');
}

if (warnings.length > 0) {
    console.warn('⚠️  Missing OPTIONAL variables:');
    warnings.forEach(key => console.warn(`   - ${key}`));
} else {
    console.log('✅ All OPTIONAL variables found.');
}

// Check for common issues
if (process.env.GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY) {
    const key = process.env.GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY;
    if (!key.includes('BEGIN PRIVATE KEY')) {
        console.warn('⚠️  GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY does not look like a valid PEM key.');
    } else {
        console.log('✅ GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY format looks valid.');
    }
}

console.log('\nEnvironment check complete.');
