/* Smoke tests for key API endpoints (Node 18+ with native fetch) */

const API_BASE = (process.env.API_URL || 'http://localhost:4000/api/v1').replace(/\/+$/, '');

async function ping(path: string, options: any = {}) {
    const url = `${API_BASE}/${path.replace(/^\/+/, '')}`;
    try {
        const res = await fetch(url, options);
        return { ok: res.ok, status: res.status, body: await res.text() };
    } catch (error: any) {
        return { ok: false, status: 0, body: error.message };
    }
}

async function run() {
    console.log(`Checking API base: ${API_BASE}`);

    const health = await ping('/health');
    console.log('GET /health =>', health.status, health.ok ? 'OK' : 'FAIL');

    const feed = await ping('/wall/feed');
    console.log('GET /wall/feed =>', feed.status, feed.ok ? 'OK' : 'FAIL');

    const me = await ping('/auth/me', {
        headers: { Authorization: 'Bearer fake_token' },
    });
    console.log('GET /auth/me (fake token) =>', me.status, me.ok ? 'UNEXPECTED OK' : 'Expected fail');
}

run().catch((err) => {
    console.error('Health check crashed:', err);
    process.exit(1);
});
