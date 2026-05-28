#!/usr/bin/env node

const { spawn } = require('child_process');
const { ensureDemoServer } = require('./ensure-demo-server');

function run(cmd, args, opts = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, args, { stdio: 'inherit', ...opts });
    child.on('exit', (code, signal) => {
      if (code === 0) return resolve();
      const reason = signal ? `signal ${signal}` : `exit code ${code}`;
      reject(new Error(`${cmd} ${args.join(' ')} failed with ${reason}`));
    });
    child.on('error', reject);
  });
}

(async () => {
  let close = async () => {};
  try {
    const { port, reused, close: closer } = await ensureDemoServer();
    close = closer;
    const env = {
      ...process.env,
      DEMO_PORT: String(port),
      DEMO_BASE_URL: `http://127.0.0.1:${port}`,
    };
    console.log(`[demo-test] Running Playwright against ${env.DEMO_BASE_URL}${reused ? ' (reused existing server)' : ''}`);
    await run('npx', ['playwright', 'test', '--config=playwright.config.ts', '--reporter=list,html,junit'], { env });
    await close();
    process.exit(0);
  } catch (err) {
    console.error('[demo-test] Failed:', err.message);
    try {
      await close();
    } catch (closeErr) {
      console.error('[demo-test] Cleanup error:', closeErr.message);
    }
    process.exit(1);
  }
})();
