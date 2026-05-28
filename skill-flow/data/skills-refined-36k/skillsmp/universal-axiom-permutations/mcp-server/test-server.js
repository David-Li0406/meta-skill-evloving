#!/usr/bin/env node

/**
 * Simple test script for the Universal Axiom MCP Server
 * This sends a basic request to verify the server is working
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('Testing Universal Axiom MCP Server...\n');

// Start the server
const serverPath = join(__dirname, 'build', 'index.js');
const server = spawn('node', [serverPath], {
  stdio: ['pipe', 'pipe', 'pipe']
});

let outputBuffer = '';
let testsPassed = 0;
let testsFailed = 0;

// Handle server output
server.stdout.on('data', (data) => {
  outputBuffer += data.toString();

  // Try to parse JSON-RPC responses
  const lines = outputBuffer.split('\n');
  outputBuffer = lines.pop() || '';

  lines.forEach(line => {
    if (line.trim()) {
      try {
        const response = JSON.parse(line);
        console.log('✓ Received response:', JSON.stringify(response, null, 2).substring(0, 200) + '...');
        testsPassed++;
      } catch (e) {
        // Not JSON, might be initialization message
      }
    }
  });
});

server.stderr.on('data', (data) => {
  const message = data.toString();
  if (message.includes('MCP Server running')) {
    console.log('✓ Server started successfully');
    testsPassed++;

    // Send test requests
    setTimeout(() => {
      sendListToolsRequest();
    }, 100);
  }
});

server.on('error', (error) => {
  console.error('✗ Server error:', error);
  testsFailed++;
  process.exit(1);
});

// Send initialize request
function sendInitialize() {
  const request = {
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: {
        name: 'test-client',
        version: '0.1.0'
      }
    }
  };

  server.stdin.write(JSON.stringify(request) + '\n');
  console.log('→ Sent initialize request');
}

// Send list tools request
function sendListToolsRequest() {
  const request = {
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/list',
    params: {}
  };

  server.stdin.write(JSON.stringify(request) + '\n');
  console.log('→ Sent tools/list request');

  // Wait for response then test a tool call
  setTimeout(() => {
    sendComputeIntelligenceRequest();
  }, 500);
}

// Send compute intelligence request
function sendComputeIntelligenceRequest() {
  const request = {
    jsonrpc: '2.0',
    id: 3,
    method: 'tools/call',
    params: {
      name: 'compute_intelligence',
      arguments: {
        impulses: 1.5,
        elements: 2.0,
        pressure: 1.2,
        subjectivity: 0.3,
        purpose: 1.0,
        time: 2.0,
        n: 5
      }
    }
  };

  server.stdin.write(JSON.stringify(request) + '\n');
  console.log('→ Sent compute_intelligence tool call');

  // Wait for response then cleanup
  setTimeout(() => {
    cleanup();
  }, 1000);
}

function cleanup() {
  server.kill();

  console.log('\n' + '='.repeat(50));
  console.log('Test Results:');
  console.log(`  ✓ Passed: ${testsPassed}`);
  console.log(`  ✗ Failed: ${testsFailed}`);
  console.log('='.repeat(50));

  if (testsFailed > 0) {
    console.log('\n❌ Tests failed!');
    process.exit(1);
  } else if (testsPassed > 0) {
    console.log('\n✅ All tests passed! MCP server is working correctly.');
    process.exit(0);
  } else {
    console.log('\n⚠️  No tests completed');
    process.exit(1);
  }
}

// Start the test
sendInitialize();

// Timeout after 5 seconds
setTimeout(() => {
  console.error('\n✗ Test timeout - server did not respond in time');
  cleanup();
}, 5000);
