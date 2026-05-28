import fetch from 'node-fetch';
import dotenv from 'dotenv';
import fs from 'fs';

dotenv.config({ path: '.env' });

async function verifyPaypal() {
    console.log('🔍 Starting PayPal Environment Verification...\n');

    const env = process.env.PAYPAL_ENVIRONMENT;
    const clientId = process.env.PAYPAL_CLIENT_ID;
    const clientSecret = process.env.PAYPAL_CLIENT_SECRET;

    if (!clientId || !clientSecret) {
        console.error('❌ ERROR: Missing PAYPAL_CLIENT_ID or PAYPAL_CLIENT_SECRET in .env');
        return;
    }

    // 1. Check for hidden characters
    const hasClientIdNewline = clientId.includes('\n') || clientId.includes('\r');
    const hasSecretNewline = clientSecret.includes('\n') || clientSecret.includes('\r');
    const hasClientIdTrailingSpace = clientId !== clientId.trim();
    const hasSecretTrailingSpace = clientSecret !== clientSecret.trim();

    if (hasClientIdNewline || hasSecretNewline || hasClientIdTrailingSpace || hasSecretTrailingSpace) {
        console.warn('⚠️ WARNING: Hidden characters detected!');
        if (hasClientIdNewline) console.warn('   - Client ID has a newline character.');
        if (hasSecretNewline) console.warn('   - Client Secret has a newline character.');
        if (hasClientIdTrailingSpace) console.warn('   - Client ID has trailing spaces.');
        if (hasSecretTrailingSpace) console.warn('   - Client Secret has trailing spaces.');
        console.log('   💡 FIX: Re-save your .env file or use sync script with printf.');
    } else {
        console.log('✅ No hidden whitespaces detected in credentials.');
    }

    // 2. Validate Environment
    const cleanEnv = (env || 'SANDBOX').trim().toUpperCase();
    console.log(`📡 Target Environment: ${cleanEnv}`);
    const baseUrl = cleanEnv === 'LIVE' ? 'https://api.paypal.com' : 'https://api.sandbox.paypal.com';

    // 3. Attempt Connection
    console.log(`🌐 Connecting to: ${baseUrl}/v1/oauth2/token ...`);

    try {
        const auth = Buffer.from(`${clientId.trim()}:${clientSecret.trim()}`).toString('base64');
        const response = await fetch(`${baseUrl}/v1/oauth2/token`, {
            method: 'POST',
            headers: {
                'Authorization': `Basic ${auth}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'grant_type=client_credentials'
        });

        if (response.ok) {
            const data = await response.json();
            console.log('\n✨ SUCCESS: PayPal connection verified!');
            console.log(`   - Access Token obtained: ${data.access_token.substring(0, 15)}...`);
            console.log(`   - App Name: ${data.app_id}`);
        } else {
            const errBody = await response.text();
            console.error('\n❌ AUTHENTICATION FAILED');
            console.error(`   - Status: ${response.status} ${response.statusText}`);
            console.error(`   - Response: ${errBody}`);

            if (errBody.includes('invalid_client')) {
                console.log('\n   🛠️ TROUBLESHOOTING:');
                console.log('   - Verify you are using LIVE credentials for the LIVE environment (and vice versa).');
                console.log('   - Ensure your PayPal App is enabled in the Dashboard.');
                console.log('   - Check for any restricted characters in the secret.');
            }
        }
    } catch (err) {
        console.error('\n💥 NETWORK ERROR:', err.message);
    }
}

verifyPaypal();
