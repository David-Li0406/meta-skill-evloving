#!/usr/bin/env node
// Lightweight telemetry receiver prototype
// Accepts POST JSON events and appends director_decision events to events.ndjson

const http = require('http');
const fs = require('fs');
const path = require('path');
const ndjsonBackend = require('../telemetry/backend-ndjson')

const PORT = process.env.PORT ? Number(process.env.PORT) : 4005;
const DATA_DIR = path.resolve(__dirname);
const OUTFILE = path.join(DATA_DIR, 'events.ndjson');

function isDirectorDecision(payload) {
  if (!payload || typeof payload !== 'object') return false;
  // Accept several possible fields that indicate event type
  const t = payload.type || payload.event_type || (payload.event && payload.event.type) || null;
  return t === 'director_decision';
}

const server = http.createServer((req, res) => {
  if (req.method !== 'POST' || req.url !== '/') {
    res.statusCode = 404;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Not found' }));
    return;
  }

  let body = '';
  req.on('data', (chunk) => { body += chunk; });
  req.on('end', () => {
    let payload;
    try {
      payload = JSON.parse(body || '{}');
    } catch (err) {
      res.statusCode = 400;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Invalid JSON' }));
      return;
    }

    if (!isDirectorDecision(payload)) {
      res.statusCode = 400;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Invalid or unsupported event type' }));
      return;
    }

    const event = { received_at: new Date().toISOString(), payload };
    // write via simple ndjson backend (appends to events.ndjson)
    try {
      ndjsonBackend.emit(event);
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ ok: true }));
    } catch (err) {
      console.error('Failed to persist event', err);
      res.statusCode = 500;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Failed to persist event' }));
    }
  });

  req.on('error', (err) => {
    console.error('Request error', err);
    res.statusCode = 400;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Bad request' }));
  });
});

// Ensure data directory exists (it does) and touch outfile
try {
  fs.mkdirSync(DATA_DIR, { recursive: true });
  fs.openSync(OUTFILE, 'a');
} catch (err) {
  console.error('Failed to prepare storage file:', err);
  process.exit(1);
}

server.listen(PORT, () => {
  console.log(`Telemetry receiver listening on http://localhost:${PORT}/`);
  console.log(`Persisting director_decision events to ${OUTFILE}`);
});

module.exports = server; // for testing
