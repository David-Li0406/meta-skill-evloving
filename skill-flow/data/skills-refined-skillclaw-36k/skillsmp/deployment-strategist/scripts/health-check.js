// Basic health check script
// Usage: node health-check.js --url https://example.com

const args = process.argv.slice(2);
let url = args.find(arg => arg.startsWith('--url='))?.split('=')[1];

if (!url) {
    // Try positional
    url = args[0];
}

if (!url) {
    console.error('❌ Error: Target URL is required.');
    console.error('Usage: node health-check.js --url=<url>');
    process.exit(1);
}

console.log(`🏥 Deployment Strategist: checking pulse of ${url}...`);

(async () => {
    try {
        const start = Date.now();
        const res = await fetch(url);
        const duration = Date.now() - start;

        if (res.ok) {
            console.log(`✅ [${res.status}] Connected in ${duration}ms`);

            const contentType = res.headers.get('content-type');
            console.log(`   Content-Type: ${contentType}`);

            // Allow 3xx as success if following redirects? fetch follows by default.

            const text = await res.text();
            if (!text || text.length === 0) {
                console.warn('⚠️  Warning: Response body is empty.');
            } else {
                console.log(`   Body Size: ${text.length} bytes`);
                // Simple check for HTML title if it's HTML
                if (contentType && contentType.includes('text/html')) {
                    const titleMatch = text.match(/<title>(.*?)<\/title>/i);
                    if (titleMatch) {
                        console.log(`   Page Title: "${titleMatch[1]}"`);
                    }
                }
            }

            console.log('🚀 Health Check Passed.');
            process.exit(0);
        } else {
            console.error(`❌ Health Check Failed: HTTP ${res.status} ${res.statusText}`);
            process.exit(1);
        }
    } catch (e) {
        console.error(`❌ Health Check Error: ${e.message}`);
        if (e.cause) console.error(e.cause);
        process.exit(1);
    }
})();
