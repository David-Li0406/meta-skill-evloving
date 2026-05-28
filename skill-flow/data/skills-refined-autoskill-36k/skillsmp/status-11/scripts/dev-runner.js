#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

let yaml = null;
try { yaml = require('js-yaml'); } catch (e) { yaml = null; }

function loadLocalConfig() {
  try {
    const cfgPath = path.join(process.cwd(), '.gengine', 'config.yaml');
    if (!fs.existsSync(cfgPath)) return {};
    const raw = fs.readFileSync(cfgPath, 'utf8');
    if (yaml) {
      const parsed = yaml.load(raw) || {};
      const norm = {};
      Object.keys(parsed).forEach(k => { norm[String(k).toUpperCase()] = parsed[k]; });
      console.log(`[dev-runner] Loaded local config from ${cfgPath}`);
      return norm;
    }
    const out = {};
    raw.split(/\r?\n/).forEach(line => {
      const t = line.trim();
      if (!t || t.startsWith('#')) return;
      const m = t.match(/^([A-Za-z0-9_\-\.]+)\s*:\s*(.*)$/);
      if (m) out[String(m[1]).toUpperCase()] = m[2];
    });
    console.log(`[dev-runner] Loaded local config (fallback parser) from ${cfgPath}`);
    return out;
  } catch (e) {
    return {};
  }
}

const localCfg = loadLocalConfig();

const endpoint = process.env.GENGINE_AI_ENDPOINT || localCfg.GENGINE_AI_ENDPOINT || 'https://your-endpoint.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview';
const proxyPort = process.env.GENGINE_CORS_PROXY_PORT || localCfg.GENGINE_CORS_PROXY_PORT || '8010';
const demoPort = process.env.DEMO_PORT || localCfg.DEMO_PORT || '8080';
const verbose = (process.env.GENGINE_CORS_PROXY_VERBOSE === 'true' || localCfg.GENGINE_CORS_PROXY_VERBOSE === 'true');

function spawnProcess(command, args, name) {
  const ps = spawn(command, args, { stdio: 'inherit', shell: false, env: process.env });
  ps.on('exit', (code, sig) => {
    console.log(`[dev-runner] Process ${name} exited with code=${code} signal=${sig}`);
    process.exit(code || 0);
  });
  ps.on('error', (err) => {
    console.error(`[dev-runner] Failed to start ${name}: ${err.message}`);
    process.exit(1);
  });
  return ps;
}

console.log('[dev-runner] Starting dev runner');
console.log(`[dev-runner] Demo port: ${demoPort}`);
console.log(`[dev-runner] Proxy target: ${endpoint}`);
console.log(`[dev-runner] Proxy port: ${proxyPort}`);

// Start http-server via npx so it's available without global install
const httpArgs = ['http-server', 'web', '--port', String(demoPort)];
const httpProc = spawnProcess('npx', httpArgs, 'http-server');

// Start cors-proxy with target and port
const proxyArgs = ['scripts/cors-proxy.js', '--target=' + endpoint, '--port=' + String(proxyPort)];
if (verbose) proxyArgs.push('--verbose');
const proxyProc = spawnProcess('node', proxyArgs, 'cors-proxy');

// ensure child processes are killed when parent exits
function shutdown() {
  try { httpProc.kill(); } catch (e) {}
  try { proxyProc.kill(); } catch (e) {}
}
process.on('SIGINT', () => { shutdown(); process.exit(0); });
process.on('SIGTERM', () => { shutdown(); process.exit(0); });
