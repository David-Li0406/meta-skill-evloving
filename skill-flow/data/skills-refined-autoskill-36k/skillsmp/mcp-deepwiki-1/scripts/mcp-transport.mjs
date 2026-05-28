#!/usr/bin/env node
/**
 * MCP Transport - Shared transport layer for MCP clients
 *
 * Zero-dependency Node.js module supporting stdio and HTTP/SSE transports.
 *
 * ⚠️  AUTO-GENERATED FILE - DO NOT EDIT
 * This file is managed by mcp-skill-generator and will be overwritten
 * when the skill is updated. Any manual changes will be lost.
 *
 * Source: https://github.com/anthropics/claude-code → skills/mcp-skill-generator
 */

import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import * as http from "node:http";
import * as https from "node:https";

const DEFAULT_TIMEOUT = 30000;

// ============================================================================
// Environment Variable Substitution
// ============================================================================

// Special symbol to indicate a value should be removed (env var not set)
export const REMOVE_VALUE = Symbol("REMOVE_VALUE");

/**
 * Replace ${VAR_NAME} patterns with environment variable values.
 *
 * Options:
 * - required (default: true): If true, throws error when env var is missing.
 *   If false, returns REMOVE_VALUE symbol when env var is missing and the
 *   entire value is just ${VAR_NAME}.
 */
export function substituteEnvVars(value, options = {}) {
  if (typeof value !== "string") return value;

  const { required = true } = options;
  const pattern = /\$\{([^}]+)\}/g;
  const missing = [];

  // Check if the entire value is just a single env var reference
  const singleVarMatch = value.match(/^\$\{([^}]+)\}$/);
  if (singleVarMatch) {
    const varName = singleVarMatch[1];
    const envValue = process.env[varName];
    if (envValue === undefined || envValue === "") {
      if (required) {
        throw new Error(
          `Missing environment variable: ${varName}\n` +
            `Set it with: export ${varName}=your_value`
        );
      }
      return REMOVE_VALUE;
    }
    return envValue;
  }

  // For mixed strings, replace all patterns
  const result = value.replace(pattern, (match, varName) => {
    const envValue = process.env[varName];
    if (envValue === undefined || envValue === "") {
      missing.push(varName);
      return match; // Keep original for error message
    }
    return envValue;
  });

  if (missing.length > 0) {
    if (required) {
      const vars = missing.join(", ");
      throw new Error(
        `Missing environment variable(s): ${vars}\n` +
          `Set them with: export ${missing[0]}=your_value`
      );
    }
    // Optional: remove the entire value if any env var is missing
    return REMOVE_VALUE;
  }

  return result;
}

/**
 * Recursively substitute env vars in an object.
 *
 * @param obj - The object to process
 * @param isOptional - Whether current context allows optional env vars
 */
export function substituteEnvVarsInObject(obj, isOptional = false) {
  // Top-level keys where env vars are optional (don't error if not set)
  const optionalSections = ["headers", "env"];

  if (typeof obj === "string") {
    return substituteEnvVars(obj, { required: !isOptional });
  }
  if (Array.isArray(obj)) {
    return obj
      .map((item) => substituteEnvVarsInObject(item, isOptional))
      .filter((item) => item !== REMOVE_VALUE);
  }
  if (obj && typeof obj === "object") {
    const result = {};
    for (const [key, value] of Object.entries(obj)) {
      // Check if this key starts an optional section
      const keyIsOptional = isOptional || optionalSections.includes(key);
      const substituted = substituteEnvVarsInObject(value, keyIsOptional);
      // Skip entries that should be removed (env var not set)
      if (substituted !== REMOVE_VALUE) {
        result[key] = substituted;
      }
    }
    return result;
  }
  return obj;
}

// ============================================================================
// JSON-RPC Helpers
// ============================================================================

let messageId = 0;

export function createRequest(method, params = {}) {
  return {
    jsonrpc: "2.0",
    id: ++messageId,
    method,
    params,
  };
}

export function createNotification(method, params = {}) {
  return {
    jsonrpc: "2.0",
    method,
    ...(Object.keys(params).length > 0 ? { params } : {}),
  };
}

// ============================================================================
// stdio Transport
// ============================================================================

export class StdioTransport {
  constructor(commandOrConfig) {
    // Support both string command and config object
    if (typeof commandOrConfig === "string") {
      this.command = commandOrConfig;
      this.args = null;
      this.env = process.env;
    } else {
      this.command = commandOrConfig.command;
      this.args = commandOrConfig.args || [];
      this.env = { ...process.env, ...commandOrConfig.env };
    }
    this.process = null;
    this.rl = null;
    this.pendingRequests = new Map();
  }

  async connect() {
    let cmd, args;

    if (this.args !== null) {
      // Config object mode
      cmd = this.command;
      args = this.args;
    } else {
      // String command mode - parse it
      const parts = this.command.match(/(?:[^\s"]+|"[^"]*")+/g) || [];
      cmd = parts[0];
      args = parts.slice(1).map((arg) => arg.replace(/^"|"$/g, ""));
    }

    this.process = spawn(cmd, args, {
      stdio: ["pipe", "pipe", "pipe"],
      env: this.env,
    });

    this.rl = createInterface({
      input: this.process.stdout,
      crlfDelay: Infinity,
    });

    this.rl.on("line", (line) => {
      this.handleLine(line);
    });

    this.process.stderr.on("data", () => {
      // Log stderr for debugging but don't fail
    });

    return new Promise((resolve, reject) => {
      this.process.on("error", (err) => {
        reject(new Error(`Failed to spawn process: ${err.message}`));
      });

      this.process.on("close", (code) => {
        for (const [, { reject: rej }] of this.pendingRequests) {
          rej(new Error(`Process closed with code ${code}`));
        }
        this.pendingRequests.clear();
      });

      // Give the process a moment to start
      setTimeout(() => {
        if (this.process.killed) {
          reject(new Error("Process terminated unexpectedly"));
        } else {
          resolve();
        }
      }, 100);
    });
  }

  handleLine(line) {
    if (!line.trim()) return;

    try {
      const message = JSON.parse(line);

      if (message.id !== undefined && this.pendingRequests.has(message.id)) {
        const { resolve, reject } = this.pendingRequests.get(message.id);
        this.pendingRequests.delete(message.id);

        if (message.error) {
          reject(
            new Error(
              `JSON-RPC Error: ${message.error.message || JSON.stringify(message.error)}`
            )
          );
        } else {
          resolve(message.result);
        }
      }
    } catch {
      // Ignore non-JSON lines
    }
  }

  sendRaw(message) {
    if (!this.process || this.process.killed) {
      throw new Error("Process not running");
    }
    const json = JSON.stringify(message);
    this.process.stdin.write(json + "\n");
  }

  async request(method, params = {}, timeout = DEFAULT_TIMEOUT) {
    const request = createRequest(method, params);

    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pendingRequests.delete(request.id);
        reject(new Error(`Request timeout: ${method}`));
      }, timeout);

      this.pendingRequests.set(request.id, {
        resolve: (result) => {
          clearTimeout(timer);
          resolve(result);
        },
        reject: (err) => {
          clearTimeout(timer);
          reject(err);
        },
      });

      this.sendRaw(request);
    });
  }

  async send(message) {
    // For compatibility with mcp-caller style usage
    if (message.id !== undefined) {
      return new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
          this.pendingRequests.delete(message.id);
          reject(new Error(`Request timeout: ${message.method}`));
        }, DEFAULT_TIMEOUT);

        this.pendingRequests.set(message.id, {
          resolve: (result) => {
            clearTimeout(timer);
            resolve({ jsonrpc: "2.0", id: message.id, result });
          },
          reject: (err) => {
            clearTimeout(timer);
            reject(err);
          },
        });

        this.sendRaw(message);
      });
    } else {
      this.sendRaw(message);
      return null;
    }
  }

  notify(method, params = {}) {
    this.sendRaw(createNotification(method, params));
  }

  async close() {
    if (this.rl) {
      this.rl.close();
    }
    if (this.process && !this.process.killed) {
      this.process.stdin.end();
      this.process.kill();
    }
  }
}

// ============================================================================
// HTTP Transport
// ============================================================================

export class HttpTransport {
  constructor(urlOrConfig) {
    // Support both string URL and config object
    if (typeof urlOrConfig === "string") {
      this.url = new URL(urlOrConfig);
      this.headers = {};
    } else {
      this.url = new URL(urlOrConfig.url);
      this.headers = urlOrConfig.headers || {};
    }
    this.sessionId = null;
  }

  async connect() {
    // HTTP transport doesn't need explicit connection
  }

  // Parse SSE response format: extract JSON from "event: message\ndata: {...}"
  parseSSEResponse(text) {
    const lines = text.split("\n");
    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const data = line.slice(6).trim();
        if (data && data !== "ping") {
          try {
            return JSON.parse(data);
          } catch {
            // Not JSON, continue
          }
        }
      }
    }
    return null;
  }

  async request(method, params = {}, timeout = DEFAULT_TIMEOUT) {
    const request = createRequest(method, params);

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout);

    try {
      const headers = {
        "Content-Type": "application/json",
        Accept: "application/json, text/event-stream",
        ...this.headers,
      };

      if (this.sessionId) {
        headers["Mcp-Session-Id"] = this.sessionId;
      }

      const response = await fetch(this.url.toString(), {
        method: "POST",
        headers,
        body: JSON.stringify(request),
        signal: controller.signal,
      });

      const newSessionId = response.headers.get("Mcp-Session-Id");
      if (newSessionId) {
        this.sessionId = newSessionId;
      }

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const contentType = response.headers.get("Content-Type") || "";
      let result;

      if (contentType.includes("text/event-stream")) {
        const text = await response.text();
        result = this.parseSSEResponse(text);
        if (!result) {
          throw new Error("Failed to parse SSE response");
        }
      } else {
        result = await response.json();
      }

      if (result.error) {
        throw new Error(
          `JSON-RPC Error: ${result.error.message || JSON.stringify(result.error)}`
        );
      }

      return result.result;
    } finally {
      clearTimeout(timer);
    }
  }

  async send(message) {
    // For compatibility with mcp-caller style usage (uses Node.js http/https)
    const isHttps = this.url.protocol === "https:";
    const httpModule = isHttps ? https : http;

    const postData = JSON.stringify(message);
    const headers = {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(postData),
      Accept: "application/json, text/event-stream",
      ...this.headers,
    };

    if (this.sessionId) {
      headers["Mcp-Session-Id"] = this.sessionId;
    }

    return new Promise((resolve, reject) => {
      const req = httpModule.request(
        {
          hostname: this.url.hostname,
          port: this.url.port || (isHttps ? 443 : 80),
          path: this.url.pathname + this.url.search,
          method: "POST",
          headers,
        },
        (res) => {
          if (res.headers["mcp-session-id"]) {
            this.sessionId = res.headers["mcp-session-id"];
          }

          let body = "";
          res.on("data", (chunk) => {
            body += chunk;
          });
          res.on("end", () => {
            if (res.statusCode >= 400) {
              reject(new Error(`HTTP ${res.statusCode}: ${body}`));
              return;
            }

            if (message.id === undefined) {
              resolve(null);
              return;
            }

            const contentType = res.headers["content-type"] || "";

            if (contentType.includes("text/event-stream")) {
              const result = this.parseSSEResponse(body);
              if (result) {
                resolve(result);
              } else {
                reject(new Error(`Failed to parse SSE response: ${body}`));
              }
            } else {
              try {
                resolve(JSON.parse(body));
              } catch (e) {
                reject(new Error(`Invalid JSON response: ${body}`));
              }
            }
          });
        }
      );

      req.on("error", (err) => {
        reject(new Error(`HTTP request failed: ${err.message}`));
      });

      req.write(postData);
      req.end();
    });
  }

  notify(method, params = {}) {
    const notification = createNotification(method, params);
    const headers = {
      "Content-Type": "application/json",
      Accept: "application/json, text/event-stream",
      ...this.headers,
    };

    if (this.sessionId) {
      headers["Mcp-Session-Id"] = this.sessionId;
    }

    fetch(this.url.toString(), {
      method: "POST",
      headers,
      body: JSON.stringify(notification),
    }).catch(() => {
      // Ignore notification errors
    });
  }

  async close() {
    // HTTP transport doesn't need cleanup
  }
}

// ============================================================================
// MCP Client Base
// ============================================================================

export class McpClient {
  constructor(transport) {
    this.transport = transport;
    this.serverInfo = null;
    this.capabilities = null;
  }

  async initialize() {
    const result = await this.transport.request("initialize", {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: {
        name: "mcp-skill-generator",
        version: "1.0.0",
      },
    });

    this.serverInfo = result.serverInfo;
    this.capabilities = result.capabilities;

    this.transport.notify("initialized");

    await new Promise((resolve) => setTimeout(resolve, 100));

    return result;
  }

  async listTools() {
    try {
      const result = await this.transport.request("tools/list");
      return result.tools || [];
    } catch (err) {
      if (
        err.message.includes("Method not found") ||
        err.message.includes("-32601")
      ) {
        return [];
      }
      throw err;
    }
  }

  async listResources() {
    try {
      const result = await this.transport.request("resources/list");
      return result.resources || [];
    } catch (err) {
      if (
        err.message.includes("Method not found") ||
        err.message.includes("-32601")
      ) {
        return [];
      }
      throw err;
    }
  }

  async listPrompts() {
    try {
      const result = await this.transport.request("prompts/list");
      return result.prompts || [];
    } catch (err) {
      if (
        err.message.includes("Method not found") ||
        err.message.includes("-32601")
      ) {
        return [];
      }
      throw err;
    }
  }

  async close() {
    await this.transport.close();
  }
}

// ============================================================================
// Factory
// ============================================================================

export function createTransport(config) {
  // Substitute environment variables in config
  const resolvedConfig = substituteEnvVarsInObject(config);

  if (resolvedConfig.transport === "stdio") {
    return new StdioTransport(resolvedConfig);
  } else if (resolvedConfig.transport === "http") {
    return new HttpTransport(resolvedConfig);
  } else {
    throw new Error(`Unknown transport: ${resolvedConfig.transport}`);
  }
}
