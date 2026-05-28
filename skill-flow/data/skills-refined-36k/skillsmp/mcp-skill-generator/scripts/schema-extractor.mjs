#!/usr/bin/env node
/**
 * schema-extractor.mjs
 *
 * Extract schema from MCP servers. Supports stdio and HTTP transports.
 *
 * Usage:
 *   node schema-extractor.mjs --stdio "npx @modelcontextprotocol/server-filesystem /tmp"
 *   node schema-extractor.mjs --http "http://localhost:3000/mcp"
 */

import { StdioTransport, HttpTransport, McpClient } from "./mcp-transport.mjs";

function printUsage() {
  console.error(`Usage:
  node schema-extractor.mjs --stdio "<command>"
  node schema-extractor.mjs --http "<url>" [--header "Key: Value"]...

Examples:
  node schema-extractor.mjs --stdio "npx @modelcontextprotocol/server-filesystem /tmp"
  node schema-extractor.mjs --http "https://mcp.deepwiki.com/mcp"
  node schema-extractor.mjs --http "https://api.example.com/mcp" --header "Authorization: Bearer TOKEN"
`);
  process.exit(1);
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    printUsage();
  }

  const mode = args[0];
  const target = args[1];

  // Parse optional headers for HTTP mode
  const headers = {};
  for (let i = 2; i < args.length; i++) {
    if (args[i] === "--header" && i + 1 < args.length) {
      const headerValue = args[i + 1];
      const colonIndex = headerValue.indexOf(":");
      if (colonIndex > 0) {
        const key = headerValue.substring(0, colonIndex).trim();
        const value = headerValue.substring(colonIndex + 1).trim();
        headers[key] = value;
      }
      i++; // Skip the header value
    }
  }

  let transport;

  if (mode === "--stdio") {
    transport = new StdioTransport(target);
  } else if (mode === "--http") {
    transport = new HttpTransport({ url: target, headers });
  } else {
    printUsage();
  }

  const client = new McpClient(transport);

  try {
    await transport.connect();
    await client.initialize();

    const [tools, resources, prompts] = await Promise.all([
      client.listTools(),
      client.listResources(),
      client.listPrompts(),
    ]);

    const schema = {
      serverInfo: client.serverInfo,
      tools,
      resources,
      prompts,
    };

    console.log(JSON.stringify(schema, null, 2));
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  } finally {
    await client.close();
  }
}

main();
