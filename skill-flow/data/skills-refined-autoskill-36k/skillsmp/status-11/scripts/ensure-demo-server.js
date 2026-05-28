#!/usr/bin/env node

const { spawn } = require('child_process');
const http = require('http');

const DEFAULT_PORT = Number(process.env.DEMO_PORT || 4173);
const MAX_PORT = Number(process.env.DEMO_PORT_MAX || DEFAULT_PORT + 20);
const HOST = process.env.DEMO_HOST || '127.0.0.1';
const MARKER = process.env.DEMO_MARKER || 'InkJS Smoke Demo';

const OCCUPIED_ERROR = 'occupied';

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function probeDemoServer(port, { host = HOST, marker = MARKER } = {}) {
  return new Promise((resolve) => {
    const req = http.get({ host, port, path: '/demo/', timeout: 1500 }, (res) => {
      let body = '';
      res.on('data', (chunk) => { body += chunk.toString(); });
      res.on('end', () => {
        if (res.statusCode && res.statusCode >= 200 && res.statusCode < 400 && body.includes(marker)) {
          resolve({ status: 'demo' });
        } else {
          resolve({ status: OCCUPIED_ERROR, reason: `Unexpected response code ${res.statusCode}` });
        }
      });
    });
    req.on('timeout', () => {
      req.destroy(new Error('timeout'));
    });
    req.on('error', (err) => {
      if (['ECONNREFUSED', 'ECONNRESET', 'EHOSTUNREACH', 'ENOTFOUND', 'ETIMEDOUT'].includes(err.code)) {
        resolve({ status: 'free' });
      } else {
        resolve({ status: OCCUPIED_ERROR, reason: err.message });
      }
    });
  });
}

async function findFreePort(start, end) {
  for (let port = start; port <= end; port += 1) {
    const probe = await probeDemoServer(port);
    if (probe.status === 'free') return port;
    if (probe.status === OCCUPIED_ERROR && port === start) throw new Error(`Port ${start} is in use by a non-demo process.`);
  }
  throw new Error(`No free port found in range ${start}-${end}`);
}

async function waitForDemo(port, opts = {}) {
  const timeoutAt = Date.now() + (opts.timeoutMs || 30_000);
  while (Date.now() < timeoutAt) {
    const probe = await probeDemoServer(port, opts);
    if (probe.status === 'demo') return true;
    if (probe.status === OCCUPIED_ERROR) throw new Error(probe.reason || `Port ${port} is occupied by a non-demo process.`);
    await wait(300);
  }
  throw new Error(`Demo server did not become ready on port ${port}`);
}

function startDemoServer(port, env = process.env) {
  const child = spawn('npm', ['run', 'serve-demo', '--', '--port', String(port)], { stdio: 'inherit', env });
  const exited = new Promise((resolve) => {
    child.on('exit', (code, signal) => resolve({ code, signal }));
  });
  const stop = async () => {
    if (!child || child.killed) return;
    child.kill('SIGTERM');
    await Promise.race([exited, wait(5000)]);
  };
  return { child, stop, exited };
}

async function ensureDemoServer(options = {}) {
  const basePort = Number(options.basePort || DEFAULT_PORT);
  const maxPort = Number(options.maxPort || MAX_PORT);
  const host = options.host || HOST;
  const marker = options.marker || MARKER;
  const startServer = options.startServer || ((port) => startDemoServer(port, options.env));

  // First check if something already answers; if demo, reuse.
  const probe = await probeDemoServer(basePort, { host, marker });
  if (probe.status === 'demo') {
    process.env.DEMO_PORT = String(basePort);
    return { port: basePort, reused: true, close: async () => {} };
  }
  if (probe.status === OCCUPIED_ERROR) {
    throw new Error(`Port ${basePort} is in use by a non-demo process.`);
  }

  const port = await findFreePort(basePort, maxPort);
  const { stop, exited } = startServer(port);
  try {
    await waitForDemo(port, { host, marker });
    process.env.DEMO_PORT = String(port);
    return {
      port,
      reused: false,
      close: async () => {
        await stop();
        await exited;
      },
    };
  } catch (err) {
    await stop();
    await exited;
    throw err;
  }
}

if (require.main === module) {
  (async () => {
    try {
      const { port, reused, close } = await ensureDemoServer();
      console.log(`[demo-server] Using port ${port}${reused ? ' (reused existing server)' : ''}`);
      const stop = async () => {
        await close();
        process.exit(0);
      };
      process.on('SIGINT', stop);
      process.on('SIGTERM', stop);
      // Keep process alive only if we started the server; otherwise exit immediately.
      if (reused) {
        process.exit(0);
      }
      await new Promise(() => {});
    } catch (err) {
      console.error('[demo-server] Failed to ensure demo server:', err.message);
      process.exit(1);
    }
  })();
}

module.exports = {
  ensureDemoServer,
  probeDemoServer,
  waitForDemo,
  startDemoServer,
};
