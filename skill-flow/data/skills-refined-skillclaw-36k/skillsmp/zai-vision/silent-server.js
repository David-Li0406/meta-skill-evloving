#!/usr/bin/env node
/**
 * Silent wrapper for MCP server - suppresses all logs, only outputs JSON results
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Read config
const configPath = path.join(__dirname, 'mcp-config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// Spawn MCP server with suppressed output
const server = spawn(config.command, config.args, {
  env: { ...process.env, ...config.env },
  stdio: ['pipe', 'pipe', 'ignore']  // stdin=pipe, stdout=pipe, stderr=ignore (completely suppress)
});

// Forward stdin
process.stdin.pipe(server.stdin);

// Forward stdout (this is the MCP protocol communication)
server.stdout.on('data', (data) => {
  process.stdout.write(data);
});

// Handle errors
server.on('error', (err) => {
  process.exit(1);
});

server.on('exit', (code) => {
  process.exit(code || 0);
});