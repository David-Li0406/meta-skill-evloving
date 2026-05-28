#!/usr/bin/env node
"use strict";

const fs = require('fs');
const path = require('path');
const http = require("http");
const https = require("https");
const { URL } = require("url");

let yamlParser = null;
try {
  yamlParser = require('js-yaml');
} catch (e) {
  // js-yaml is optional; if missing we will still support minimal key=value style in .gengine/config.yaml
  yamlParser = null;
}

function loadLocalConfig() {
  try {
    const cfgDir = path.join(process.cwd(), '.gengine');
    const cfgPath = path.join(cfgDir, 'config.yaml');
    if (!fs.existsSync(cfgPath)) return {};
    const raw = fs.readFileSync(cfgPath, 'utf8');
    if (yamlParser) {
      try {
        const parsed = yamlParser.load(raw) || {};
        // Normalize keys to upper-case environment-like strings for easy lookup
        const norm = {};
        Object.keys(parsed).forEach(k => { norm[String(k).toUpperCase()] = parsed[k]; });
        console.log(`[cors-proxy] Loaded local config from ${cfgPath}`);
        return norm;
      } catch (e) {
        console.error(`[cors-proxy] Failed to parse ${cfgPath}: ${e.message}`);
        return {};
      }
    }

    // Fallback simple parser: lines of KEY: value or key: value
    const out = {};
    raw.split(/\r?\n/).forEach(line => {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) return;
      const m = trimmed.match(/^([A-Za-z0-9_\-\.]+)\s*:\s*(.*)$/);
      if (m) {
        out[String(m[1]).toUpperCase()] = m[2];
      }
    });
    console.log(`[cors-proxy] Loaded local config (fallback parser) from ${cfgPath}`);
    return out;
  } catch (e) {
    return {};
  }
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (!token.startsWith("-")) {
      continue;
    }

    const isLong = token.startsWith("--");
    const keyPart = isLong ? token.slice(2) : token.slice(1);
    const [key, inlineValue] = keyPart.split("=");

    if (inlineValue !== undefined) {
      args[key] = inlineValue;
      continue;
    }

    const next = argv[i + 1];
    if (next && !next.startsWith("-")) {
      args[key] = next;
      i += 1;
    } else {
      args[key] = true;
    }
  }
  return args;
}

const rawArgs = parseArgs(process.argv.slice(2));
const localCfg = loadLocalConfig();

const targetArg = rawArgs.target || rawArgs.t || process.env.GENGINE_AI_ENDPOINT || process.env.TARGET_URL || localCfg.GENGINE_AI_ENDPOINT;
const portArg = rawArgs.port || rawArgs.p || process.env.GENGINE_CORS_PROXY_PORT || localCfg.GENGINE_CORS_PROXY_PORT || "8010";
const verbose = Boolean(rawArgs.verbose || rawArgs.v || process.env.GENGINE_CORS_PROXY_VERBOSE === 'true' || process.env.GENGINE_CORS_PROXY_VERBOSE === '1' || localCfg.GENGINE_CORS_PROXY_VERBOSE === 'true' || localCfg.GENGINE_CORS_PROXY_VERBOSE === true);

if (!targetArg) {
  console.error("[cors-proxy] Missing required --target <url> argument or GENGINE_AI_ENDPOINT/TARGET_URL env or .gengine/config.yaml");
  console.error("Example: node scripts/cors-proxy.js --target https://example.azure.com");
  process.exit(1);
}

let targetBase;
try {
  targetBase = new URL(targetArg);
} catch (err) {
  console.error(`[cors-proxy] Invalid target URL: ${err.message}`);
  process.exit(1);
}

if (targetBase.protocol !== "http:" && targetBase.protocol !== "https:") {
  console.error("[cors-proxy] Target URL must use http or https protocol");
  process.exit(1);
}

const targetOrigin = `${targetBase.protocol}//${targetBase.host}`;
const targetClient = targetBase.protocol === "https:" ? https : http;
const port = Number(portArg);

if (Number.isNaN(port)) {
  console.error(`[cors-proxy] Invalid port: ${portArg}`);
  process.exit(1);
}

// Backwards-compatible: if original PORT env is set, prefer it for dev:demo flows that still use PORT
if (!process.env.PORT && localCfg.PORT) {
  // localCfg.PORT may exist if user used older example; set process.env.PORT for downstream tools
  process.env.PORT = String(localCfg.PORT);
}
function log(...messages) {
  if (verbose) {
    console.log(...messages);
  }
}

const server = http.createServer((req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,PUT,PATCH,DELETE,OPTIONS");
  res.setHeader(
    "Access-Control-Allow-Headers",
    req.headers["access-control-request-headers"] || "Content-Type, Authorization, api-key"
  );
  res.setHeader("Access-Control-Expose-Headers", "*");

  if (req.method === "OPTIONS") {
    res.writeHead(200);
    res.end();
    return;
  }

  const forwardUrl = new URL(req.url, targetOrigin);
  const headers = { ...req.headers };
  delete headers.host;
  delete headers.origin;
  delete headers.referer;
  headers.host = forwardUrl.host;

  const options = {
    protocol: forwardUrl.protocol,
    hostname: forwardUrl.hostname,
    port: forwardUrl.port || (forwardUrl.protocol === "https:" ? 443 : 80),
    path: forwardUrl.pathname + forwardUrl.search,
    method: req.method,
    headers
  };

  log(`[cors-proxy] ${req.method} ${req.url} -> ${forwardUrl.href}`);

  const proxyReq = (forwardUrl.protocol === "https:" ? https : http).request(
    options,
    (proxyRes) => {
      const responseHeaders = { ...proxyRes.headers };
      responseHeaders["access-control-allow-origin"] = "*";
      responseHeaders["access-control-expose-headers"] = "*";
      res.writeHead(proxyRes.statusCode || 502, responseHeaders);
      proxyRes.pipe(res);
    }
  );

  proxyReq.on("error", (err) => {
    console.error(`[cors-proxy] Upstream error: ${err.message}`);
    if (!res.headersSent) {
      res.writeHead(502, { "content-type": "application/json" });
    }
    res.end(
      JSON.stringify({
        error: "proxy_error",
        message: err.message
      })
    );
  });

  req.pipe(proxyReq);
});

server.on("error", (err) => {
  console.error(`[cors-proxy] Server error: ${err.message}`);
  process.exit(1);
});

server.listen(port, () => {
  console.log(`[cors-proxy] Proxy listening on http://localhost:${port}`);
  console.log(`[cors-proxy] Forwarding to ${targetOrigin}`);
  if (targetBase.pathname && targetBase.pathname !== "/") {
    console.log(`[cors-proxy] Note: base path ${targetBase.pathname} is ignored; use request URL paths`);
  }
  if (!verbose) {
    console.log("[cors-proxy] Run with --verbose for per-request logs");
  }
});
