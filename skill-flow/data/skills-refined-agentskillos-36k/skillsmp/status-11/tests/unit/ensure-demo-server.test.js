const { spawnSync } = require('child_process');
const net = require('net');

const scriptPath = require('path').join(__dirname, '..', '..', 'scripts', 'ensure-demo-server.js');
jest.setTimeout(30000);

function isListening(port) {
  return new Promise((resolve) => {
    const socket = net.createConnection({ port, host: '127.0.0.1' }, () => {
      socket.end();
      resolve(true);
    });
    socket.on('error', () => resolve(false));
  });
}

describe('ensure-demo-server script', () => {
  it('reuses existing server when port is busy', async () => {
    // Start a disposable server on the default port
    const server = net.createServer().listen(4173, '127.0.0.1');
    try {
      const result = spawnSync('node', [scriptPath], { env: { ...process.env }, encoding: 'utf8' });
      expect(result.status).toBe(0);
      expect(result.stdout).toMatch(/Using port 4173 \(reused existing server\)/);
    } finally {
      server.close();
    }
  });

  it('errors when a non-demo process holds the default port', async () => {
    const server = net.createServer().listen(4173, '127.0.0.1');
    try {
      const result = spawnSync('node', [scriptPath], { env: { ...process.env, DEMO_MARKER: 'unlikely-marker' }, encoding: 'utf8' });
      expect(result.status).toBe(1);
      expect(result.stderr).toMatch(/in use by a non-demo process/);
    } finally {
      server.close();
    }
  });

  it('starts new server on an alternate port when default is free', async () => {
    const result = spawnSync('node', [scriptPath], { env: { ...process.env, DEMO_PORT: '4180', DEMO_PORT_MAX: '4182' }, encoding: 'utf8' });
    expect(result.status).toBe(0);
    const match = result.stdout.match(/Using port (\d+)/);
    expect(match).not.toBeNull();
    const port = Number(match[1]);
    expect(port).toBeGreaterThanOrEqual(4180);
    expect(port).toBeLessThanOrEqual(4182);
    const listening = await isListening(port);
    expect(listening).toBe(true);
  });
});
