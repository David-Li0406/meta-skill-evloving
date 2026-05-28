#!/usr/bin/env node
/**
 * MCP API - Simple, AI-friendly API for calling MCP tools
 *
 * Usage:
 *   import { callTool, listTools } from './scripts/api.mjs';
 *
 *   // Single call
 *   const result = await callTool('searchGitHub', { query: 'react hooks' });
 *
 *   // Parallel calls
 *   const results = await Promise.all([
 *     callTool('tool1', { arg: 'value1' }),
 *     callTool('tool2', { arg: 'value2' }),
 *   ]);
 *
 * ⚠️  AUTO-GENERATED FILE - DO NOT EDIT
 * This file is managed by mcp-skill-generator and will be overwritten
 * when the skill is updated. Any manual changes will be lost.
 */

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  createTransport,
  createRequest,
  createNotification,
} from "./mcp-transport.mjs";
import { parseTOML } from "./mcp-caller.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Lazy-initialized shared client
let _client = null;

async function getClient() {
  if (_client) return _client;

  const configPath = join(__dirname, "..", "config.toml");
  const config = parseTOML(readFileSync(configPath, "utf-8"));

  const transport = createTransport(config);
  await transport.connect();

  // Initialize MCP handshake
  const initResponse = await transport.send(
    createRequest("initialize", {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: { name: "mcp-api", version: "1.0.0" },
    })
  );

  if (initResponse.error) {
    throw new Error(`Initialize failed: ${initResponse.error.message}`);
  }

  await transport.send(createNotification("notifications/initialized"));

  _client = {
    transport,
    serverInfo: initResponse.result?.serverInfo,
    capabilities: initResponse.result?.capabilities,
  };

  return _client;
}

/**
 * Call an MCP tool
 * @param {string} name - Tool name
 * @param {object} args - Tool arguments
 * @returns {Promise<object>} - Tool result
 */
export async function callTool(name, args = {}) {
  const { transport } = await getClient();

  const response = await transport.send(
    createRequest("tools/call", { name, arguments: args })
  );

  if (response.error) {
    throw new Error(`Tool "${name}" failed: ${response.error.message}`);
  }

  return response.result;
}

/**
 * List available tools
 * @returns {Promise<Array>} - Array of tool definitions
 */
export async function listTools() {
  const { transport } = await getClient();

  const response = await transport.send(createRequest("tools/list"));

  if (response.error) {
    throw new Error(`listTools failed: ${response.error.message}`);
  }

  return response.result?.tools || [];
}

/**
 * Read a resource
 * @param {string} uri - Resource URI
 * @returns {Promise<object>} - Resource content
 */
export async function readResource(uri) {
  const { transport } = await getClient();

  const response = await transport.send(
    createRequest("resources/read", { uri })
  );

  if (response.error) {
    throw new Error(`readResource failed: ${response.error.message}`);
  }

  return response.result;
}

/**
 * List available resources
 * @returns {Promise<Array>} - Array of resource definitions
 */
export async function listResources() {
  const { transport } = await getClient();

  const response = await transport.send(createRequest("resources/list"));

  if (response.error) {
    throw new Error(`listResources failed: ${response.error.message}`);
  }

  return response.result?.resources || [];
}

/**
 * Get a prompt
 * @param {string} name - Prompt name
 * @param {object} args - Prompt arguments
 * @returns {Promise<object>} - Prompt result
 */
export async function getPrompt(name, args = {}) {
  const { transport } = await getClient();

  const response = await transport.send(
    createRequest("prompts/get", { name, arguments: args })
  );

  if (response.error) {
    throw new Error(`getPrompt failed: ${response.error.message}`);
  }

  return response.result;
}

/**
 * List available prompts
 * @returns {Promise<Array>} - Array of prompt definitions
 */
export async function listPrompts() {
  const { transport } = await getClient();

  const response = await transport.send(createRequest("prompts/list"));

  if (response.error) {
    throw new Error(`listPrompts failed: ${response.error.message}`);
  }

  return response.result?.prompts || [];
}

/**
 * Close the connection (optional - for cleanup)
 */
export async function close() {
  if (_client) {
    await _client.transport.close();
    _client = null;
  }
}
