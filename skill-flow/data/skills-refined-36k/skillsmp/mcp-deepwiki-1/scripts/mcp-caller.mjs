#!/usr/bin/env node
/**
 * MCP Caller - Call MCP tools at runtime
 *
 * Usage:
 *   node mcp-caller.mjs call <tool-name> '<json-arguments>'
 *   node mcp-caller.mjs resource <uri>
 *   node mcp-caller.mjs prompt <name> '<json-arguments>'
 *   node mcp-caller.mjs list
 *
 * Configuration: Reads from ../config.toml relative to script location
 *
 * ⚠️  AUTO-GENERATED FILE - DO NOT EDIT
 * This file is managed by mcp-skill-generator and will be overwritten
 * when the skill is updated. Any manual changes will be lost.
 *
 * Source: https://github.com/anthropics/claude-code → skills/mcp-skill-generator
 */

import { readFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  createTransport,
  createRequest,
  createNotification,
} from "./mcp-transport.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// ============================================================================
// Simple TOML Parser (handles our config format with sections)
// ============================================================================

export function parseTOML(content) {
  const result = {};
  const lines = content.split("\n");
  let currentSection = null;

  for (let line of lines) {
    line = line.trim();
    if (!line || line.startsWith("#")) continue;

    // Check for section header [section]
    const sectionMatch = line.match(/^\[([^\]]+)\]$/);
    if (sectionMatch) {
      currentSection = sectionMatch[1];
      result[currentSection] = result[currentSection] || {};
      continue;
    }

    const eqIdx = line.indexOf("=");
    if (eqIdx === -1) continue;

    const key = line.slice(0, eqIdx).trim();
    let value = line.slice(eqIdx + 1).trim();

    // Parse value
    let parsedValue;
    if (value.startsWith('"') && value.endsWith('"')) {
      parsedValue = value.slice(1, -1);
    } else if (value.startsWith("[") && value.endsWith("]")) {
      parsedValue = JSON.parse(value);
    } else if (value === "true") {
      parsedValue = true;
    } else if (value === "false") {
      parsedValue = false;
    } else if (!isNaN(Number(value))) {
      parsedValue = Number(value);
    } else {
      parsedValue = value;
    }

    // Assign to current section or root
    if (currentSection) {
      result[currentSection][key] = parsedValue;
    } else {
      result[key] = parsedValue;
    }
  }

  return result;
}

// ============================================================================
// Configuration
// ============================================================================

function loadConfig() {
  const tomlPath = join(__dirname, "..", "config.toml");
  const jsonPath = join(__dirname, "..", "config.json");

  let configPath = tomlPath;
  let isToml = true;

  if (!existsSync(tomlPath)) {
    if (existsSync(jsonPath)) {
      configPath = jsonPath;
      isToml = false;
    } else {
      console.error(`Error: Config file not found at ${tomlPath}`);
      console.error("Please create config.toml with transport configuration.");
      console.error("\nExample (stdio):");
      console.error(`transport = "stdio"
command = "npx"
args = ["@modelcontextprotocol/server-filesystem@0.6.2", "/tmp"]
version = "0.6.2"
versionLockedAt = "2026-01-20"`);
      console.error("\nExample (HTTP):");
      console.error(`transport = "http"
url = "http://localhost:3000/mcp"`);
      process.exit(1);
    }
  }

  try {
    const content = readFileSync(configPath, "utf-8");
    return isToml ? parseTOML(content) : JSON.parse(content);
  } catch (err) {
    console.error(`Error reading config: ${err.message}`);
    process.exit(1);
  }
}

// ============================================================================
// MCP Caller Client (extends base functionality)
// ============================================================================

class McpCallerClient {
  constructor(config) {
    this.config = config;
    this.transport = null;
    this.serverInfo = null;
    this.capabilities = null;
  }

  async connect() {
    this.transport = createTransport(this.config);
    await this.transport.connect();

    const initRequest = createRequest("initialize", {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: {
        name: "mcp-caller",
        version: "1.0.0",
      },
    });

    const response = await this.transport.send(initRequest);

    if (response.error) {
      throw new Error(`Initialize failed: ${response.error.message}`);
    }

    this.serverInfo = response.result.serverInfo;
    this.capabilities = response.result.capabilities;

    await this.transport.send(createNotification("notifications/initialized"));
  }

  async listTools() {
    const response = await this.transport.send(createRequest("tools/list"));
    if (response.error) {
      throw new Error(`tools/list failed: ${response.error.message}`);
    }
    return response.result.tools || [];
  }

  async callTool(name, args) {
    const response = await this.transport.send(
      createRequest("tools/call", {
        name,
        arguments: args,
      })
    );

    if (response.error) {
      if (response.error.code === -32601) {
        const tools = await this.listTools();
        const toolNames = tools.map((t) => t.name).join(", ");
        throw new Error(
          `Tool "${name}" not found. Available tools: ${toolNames}`
        );
      }
      throw new Error(`tools/call failed: ${response.error.message}`);
    }

    return response.result;
  }

  async readResource(uri) {
    const response = await this.transport.send(
      createRequest("resources/read", { uri })
    );

    if (response.error) {
      throw new Error(`resources/read failed: ${response.error.message}`);
    }

    return response.result;
  }

  async getPrompt(name, args) {
    const response = await this.transport.send(
      createRequest("prompts/get", {
        name,
        arguments: args,
      })
    );

    if (response.error) {
      throw new Error(`prompts/get failed: ${response.error.message}`);
    }

    return response.result;
  }

  async close() {
    if (this.transport) {
      await this.transport.close();
    }
  }
}

// ============================================================================
// CLI
// ============================================================================

function printUsage() {
  console.log(`
MCP Caller - Call MCP tools at runtime

Usage:
  node mcp-caller.mjs call <tool-name> '<json-arguments>'   Call a tool
  node mcp-caller.mjs resource <uri>                        Read a resource
  node mcp-caller.mjs prompt <name> '<json-arguments>'      Get a prompt
  node mcp-caller.mjs list                                  List available tools

Configuration:
  Reads from ../config.toml relative to script location.

Examples:
  node mcp-caller.mjs list
  node mcp-caller.mjs call read_file '{"path": "/tmp/test.txt"}'
  node mcp-caller.mjs resource 'file:///tmp/test.txt'
  node mcp-caller.mjs prompt code_review '{"code": "function foo() {}"}'
`.trim());
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    printUsage();
    process.exit(1);
  }

  const command = args[0];
  const config = loadConfig();
  const client = new McpCallerClient(config);

  try {
    await client.connect();

    switch (command) {
      case "list": {
        const tools = await client.listTools();
        console.log(JSON.stringify({ tools }, null, 2));
        break;
      }

      case "call": {
        if (args.length < 2) {
          console.error("Error: Missing tool name");
          console.error(
            "Usage: node mcp-caller.mjs call <tool-name> '<json-arguments>'"
          );
          process.exit(1);
        }
        const toolName = args[1];
        let toolArgs = {};
        if (args[2]) {
          try {
            toolArgs = JSON.parse(args[2]);
          } catch (e) {
            console.error(`Error: Invalid JSON arguments: ${e.message}`);
            const tools = await client.listTools();
            const tool = tools.find((t) => t.name === toolName);
            if (tool && tool.inputSchema) {
              console.error("\nExpected schema:");
              console.error(JSON.stringify(tool.inputSchema, null, 2));
            }
            process.exit(1);
          }
        }
        const result = await client.callTool(toolName, toolArgs);
        console.log(JSON.stringify(result, null, 2));
        break;
      }

      case "resource": {
        if (args.length < 2) {
          console.error("Error: Missing resource URI");
          console.error("Usage: node mcp-caller.mjs resource <uri>");
          process.exit(1);
        }
        const uri = args[1];
        const result = await client.readResource(uri);
        console.log(JSON.stringify(result, null, 2));
        break;
      }

      case "prompt": {
        if (args.length < 2) {
          console.error("Error: Missing prompt name");
          console.error(
            "Usage: node mcp-caller.mjs prompt <name> '<json-arguments>'"
          );
          process.exit(1);
        }
        const promptName = args[1];
        let promptArgs = {};
        if (args[2]) {
          try {
            promptArgs = JSON.parse(args[2]);
          } catch (e) {
            console.error(`Error: Invalid JSON arguments: ${e.message}`);
            process.exit(1);
          }
        }
        const result = await client.getPrompt(promptName, promptArgs);
        console.log(JSON.stringify(result, null, 2));
        break;
      }

      default:
        console.error(`Error: Unknown command "${command}"`);
        printUsage();
        process.exit(1);
    }
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  } finally {
    await client.close();
  }
}

// Only run when executed directly (not when imported)
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
