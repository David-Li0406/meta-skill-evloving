#!/usr/bin/env bun
/**
 * Server Manager - Dev server lifecycle management
 *
 * Usage:
 *   bun server-manager.ts start [--port 5173] [--command "bun run dev"]
 *   bun server-manager.ts stop
 *   bun server-manager.ts status
 *   bun server-manager.ts detect-port
 *   bun server-manager.ts wait-ready [--url http://localhost:5173] [--timeout 30000]
 *
 * Auto-detects port from package.json if not specified.
 */

import { $ } from 'bun';
import { parseArgs } from 'util';

// Types
interface ServerState {
  pid: number | null;
  port: number;
  command: string;
  startedAt: string | null;
  status: 'running' | 'stopped' | 'unknown';
}

interface PackageJson {
  scripts?: {
    dev?: string;
    start?: string;
    serve?: string;
  };
}

// State file path
const STATE_FILE = new URL('../state.json', import.meta.url).pathname;

// Detect port from package.json
function detectPort(cwd: string = process.cwd()): number {
  try {
    const pkgPath = `${cwd}/package.json`;
    const pkg: PackageJson = JSON.parse(Bun.file(pkgPath).text());
    const devScript = pkg.scripts?.dev || pkg.scripts?.start || '';

    // Parse common patterns:
    // "vite --port 3000" → 3000
    // "next dev -p 4000" → 4000
    // "bun --port=5173" → 5173
    const portMatch = devScript.match(/(?:--port[=\s]?|-p\s?)(\d+)/);
    if (portMatch) return parseInt(portMatch[1]);

    // Framework defaults
    if (devScript.includes('vite')) return 5173;
    if (devScript.includes('next')) return 3000;
    if (devScript.includes('svelte')) return 5173;
    if (devScript.includes('gatsby')) return 8000;
    if (devScript.includes('nuxt')) return 3000;
    if (devScript.includes('astro')) return 4321;

    // Fallback
    return 5173;
  } catch {
    return 5173;
  }
}

// Detect start command from package.json
function detectCommand(cwd: string = process.cwd()): string {
  try {
    const pkgPath = `${cwd}/package.json`;
    const pkg: PackageJson = JSON.parse(Bun.file(pkgPath).text());

    if (pkg.scripts?.dev) return 'bun run dev';
    if (pkg.scripts?.start) return 'bun run start';
    if (pkg.scripts?.serve) return 'bun run serve';

    return 'bun run dev';
  } catch {
    return 'bun run dev';
  }
}

// Check if port is in use
async function isPortInUse(port: number): Promise<boolean> {
  try {
    const result = await $`lsof -i :${port} -t`.quiet();
    return result.stdout.toString().trim().length > 0;
  } catch {
    return false;
  }
}

// Get PID using port
async function getPidOnPort(port: number): Promise<number | null> {
  try {
    const result = await $`lsof -i :${port} -t`.quiet();
    const pid = parseInt(result.stdout.toString().trim().split('\n')[0]);
    return isNaN(pid) ? null : pid;
  } catch {
    return null;
  }
}

// Wait for server to be ready
async function waitForReady(url: string, timeout: number = 30000): Promise<boolean> {
  const startTime = Date.now();
  const checkInterval = 500;

  while (Date.now() - startTime < timeout) {
    try {
      const response = await fetch(url, { method: 'HEAD' });
      if (response.ok || response.status === 304) {
        return true;
      }
    } catch {
      // Server not ready yet
    }
    await Bun.sleep(checkInterval);
  }

  return false;
}

// Update state file
async function updateState(state: Partial<ServerState>): Promise<void> {
  let current: ServerState = {
    pid: null,
    port: 5173,
    command: '',
    startedAt: null,
    status: 'unknown',
  };

  try {
    const existing = JSON.parse(await Bun.file(STATE_FILE).text());
    current = { ...current, ...existing };
  } catch {
    // File doesn't exist yet
  }

  const updated = { ...current, ...state };
  await Bun.write(STATE_FILE, JSON.stringify(updated, null, 2));
}

// Start server
async function startServer(port: number, command: string): Promise<void> {
  // Check if already running
  if (await isPortInUse(port)) {
    const pid = await getPidOnPort(port);
    console.log(JSON.stringify({
      success: true,
      message: `Server already running on port ${port}`,
      pid,
      port,
      alreadyRunning: true,
    }));
    await updateState({ pid, port, status: 'running' });
    return;
  }

  // Start server in background
  const proc = Bun.spawn(command.split(' '), {
    cwd: process.cwd(),
    stdout: 'pipe',
    stderr: 'pipe',
  });

  // Wait for server to be ready
  const url = `http://localhost:${port}`;
  const ready = await waitForReady(url, 30000);

  if (!ready) {
    console.log(JSON.stringify({
      success: false,
      error: `Server did not become ready within 30 seconds`,
      port,
    }));
    process.exit(1);
  }

  const pid = await getPidOnPort(port);

  await updateState({
    pid,
    port,
    command,
    startedAt: new Date().toISOString(),
    status: 'running',
  });

  console.log(JSON.stringify({
    success: true,
    message: `Server started on port ${port}`,
    pid,
    port,
    url,
  }));
}

// Stop server
async function stopServer(port?: number): Promise<void> {
  let targetPort = port;

  if (!targetPort) {
    try {
      const state = JSON.parse(await Bun.file(STATE_FILE).text());
      targetPort = state.port;
    } catch {
      targetPort = detectPort();
    }
  }

  const pid = await getPidOnPort(targetPort!);

  if (!pid) {
    console.log(JSON.stringify({
      success: true,
      message: `No server running on port ${targetPort}`,
    }));
    await updateState({ pid: null, status: 'stopped' });
    return;
  }

  try {
    await $`kill ${pid}`.quiet();
    await updateState({ pid: null, status: 'stopped' });
    console.log(JSON.stringify({
      success: true,
      message: `Server stopped (PID: ${pid})`,
      pid,
    }));
  } catch (error) {
    console.log(JSON.stringify({
      success: false,
      error: `Failed to stop server: ${error}`,
      pid,
    }));
    process.exit(1);
  }
}

// Get server status
async function getStatus(port?: number): Promise<void> {
  let targetPort = port;

  if (!targetPort) {
    try {
      const state = JSON.parse(await Bun.file(STATE_FILE).text());
      targetPort = state.port;
    } catch {
      targetPort = detectPort();
    }
  }

  const inUse = await isPortInUse(targetPort!);
  const pid = inUse ? await getPidOnPort(targetPort!) : null;

  console.log(JSON.stringify({
    port: targetPort,
    running: inUse,
    pid,
    url: inUse ? `http://localhost:${targetPort}` : null,
  }));
}

// Main
async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      port: { type: 'string', short: 'p' },
      command: { type: 'string', short: 'c' },
      url: { type: 'string', short: 'u' },
      timeout: { type: 'string', short: 't' },
    },
    allowPositionals: true,
  });

  const command = positionals[0];

  switch (command) {
    case 'start': {
      const port = values.port ? parseInt(values.port) : detectPort();
      const cmd = values.command || detectCommand();
      await startServer(port, cmd);
      break;
    }

    case 'stop': {
      const port = values.port ? parseInt(values.port) : undefined;
      await stopServer(port);
      break;
    }

    case 'status': {
      const port = values.port ? parseInt(values.port) : undefined;
      await getStatus(port);
      break;
    }

    case 'detect-port': {
      const port = detectPort();
      console.log(JSON.stringify({ port }));
      break;
    }

    case 'detect-command': {
      const cmd = detectCommand();
      console.log(JSON.stringify({ command: cmd }));
      break;
    }

    case 'wait-ready': {
      const port = values.port ? parseInt(values.port) : detectPort();
      const url = values.url || `http://localhost:${port}`;
      const timeout = values.timeout ? parseInt(values.timeout) : 30000;
      const ready = await waitForReady(url, timeout);
      console.log(JSON.stringify({ ready, url }));
      if (!ready) process.exit(1);
      break;
    }

    default:
      console.error(`Unknown command: ${command}`);
      console.error('Available commands: start, stop, status, detect-port, detect-command, wait-ready');
      process.exit(1);
  }
}

main();
