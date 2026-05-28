/**
 * MCP Client - Base utility for calling MCP tools
 *
 * This client wraps MCP tool calls into typed TypeScript functions.
 * It handles the protocol details so tool wrappers can be simple.
 *
 * Configuration:
 *   - MCP_CONFIG_PATH: Path to .mcp.json configuration file
 *   - MCP_MOCK_MODE: Set to "true" for development/testing without actual servers
 *   - MCP_SERVER_URL: Override server URL for HTTP-based MCP servers
 */

import * as fs from 'fs';
import * as path from 'path';

// Types
export interface MCPToolCall {
  tool: string;
  input: Record<string, unknown>;
}

export interface MCPToolResult<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface MCPServerConfig {
  command?: string;
  args?: string[];
  url?: string;
  env?: Record<string, string>;
}

export interface MCPConfig {
  mcpServers: Record<string, MCPServerConfig>;
}

// Configuration
const MCP_CONFIG_PATH = process.env.MCP_CONFIG_PATH || path.join(process.cwd(), '.mcp.json');
const MCP_MOCK_MODE = process.env.MCP_MOCK_MODE === 'true';

let mcpConfig: MCPConfig | null = null;

/**
 * Load MCP configuration from .mcp.json
 */
function loadConfig(): MCPConfig {
  if (mcpConfig) return mcpConfig;

  try {
    if (fs.existsSync(MCP_CONFIG_PATH)) {
      const content = fs.readFileSync(MCP_CONFIG_PATH, 'utf-8');
      mcpConfig = JSON.parse(content);
      return mcpConfig!;
    }
  } catch (error) {
    console.warn(`[MCP] Warning: Could not load config from ${MCP_CONFIG_PATH}`);
  }

  // Return empty config if not found
  mcpConfig = { mcpServers: {} };
  return mcpConfig;
}

/**
 * Parse tool name into server and tool components
 * Format: "server_name__tool_name" or "server-name__tool-name"
 */
function parseToolName(toolName: string): { server: string; tool: string } {
  const parts = toolName.split('__');
  if (parts.length !== 2) {
    throw new Error(`Invalid tool name format: ${toolName}. Expected: server__tool`);
  }
  return { server: parts[0], tool: parts[1] };
}

/**
 * Mock implementation for development/testing
 */
async function mockToolCall<T>(
  toolName: string,
  input: Record<string, unknown>
): Promise<T> {
  console.log(`[MCP MOCK] Tool: ${toolName}`);
  console.log(`[MCP MOCK] Input: ${JSON.stringify(input, null, 2)}`);

  // Return mock data based on common patterns
  const { tool } = parseToolName(toolName);

  // Generic mock responses
  const mockResponses: Record<string, unknown> = {
    fetch_data: { items: [], total: 0, message: "Mock data returned" },
    get_document: { content: "Mock document content", id: input.id || "mock-id" },
    list_items: { items: [], count: 0 },
    write_results: { success: true, recordsWritten: 0 },
    process_items: { processed: 0, results: [] },
    search: { results: [], total: 0 },
  };

  // Find matching mock or return generic
  const mockKey = Object.keys(mockResponses).find(k => tool.includes(k));
  const mockData = mockKey ? mockResponses[mockKey] : { success: true, data: null };

  console.log(`[MCP MOCK] Response: ${JSON.stringify(mockData)}`);
  return mockData as T;
}

/**
 * Make HTTP call to MCP server (for HTTP-based servers)
 */
async function httpToolCall<T>(
  serverUrl: string,
  toolName: string,
  input: Record<string, unknown>
): Promise<T> {
  const { tool } = parseToolName(toolName);

  const response = await fetch(`${serverUrl}/tools/${tool}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(input),
  });

  if (!response.ok) {
    throw new Error(`MCP HTTP error: ${response.status} ${response.statusText}`);
  }

  const result = await response.json();
  return result as T;
}

/**
 * Call an MCP tool and return typed result
 *
 * @param toolName - The full tool name (server__tool format)
 * @param input - Tool input parameters
 * @returns Typed tool result
 *
 * @example
 * // Fetch data from Google Drive
 * const doc = await callMCPTool<DocumentResponse>(
 *   'google_drive__get_document',
 *   { documentId: 'abc123' }
 * );
 *
 * @example
 * // Query database
 * const results = await callMCPTool<QueryResponse>(
 *   'postgres__query',
 *   { sql: 'SELECT * FROM users LIMIT 10' }
 * );
 */
export async function callMCPTool<T>(
  toolName: string,
  input: Record<string, unknown>
): Promise<T> {
  // Use mock mode for development/testing
  if (MCP_MOCK_MODE) {
    return mockToolCall<T>(toolName, input);
  }

  const config = loadConfig();
  const { server, tool } = parseToolName(toolName);

  // Check if server is configured
  const serverConfig = config.mcpServers[server];

  // If server URL is provided (HTTP-based MCP server)
  if (serverConfig?.url || process.env.MCP_SERVER_URL) {
    const url = serverConfig?.url || process.env.MCP_SERVER_URL!;
    return httpToolCall<T>(url, toolName, input);
  }

  // For stdio-based servers, we need to use a different approach
  // In Claude Code context, the MCP servers are already running
  // and tools are called through the Claude interface

  console.log(`[MCP] Calling tool: ${toolName}`);
  console.log(`[MCP] Server: ${server}`);
  console.log(`[MCP] Input: ${JSON.stringify(input)}`);

  // When running in Claude Code context, this would be handled by the runtime
  // For standalone execution, we fall back to mock mode with a warning
  console.warn(`[MCP] Warning: No server URL configured for '${server}'.`);
  console.warn(`[MCP] Set MCP_MOCK_MODE=true for development or configure server URL.`);

  return mockToolCall<T>(toolName, input);
}

/**
 * Batch call multiple MCP tools efficiently
 *
 * @param calls - Array of tool calls
 * @returns Array of results in same order
 *
 * @example
 * const results = await batchCallMCPTools<UserData>([
 *   { tool: 'users__get', input: { id: '1' } },
 *   { tool: 'users__get', input: { id: '2' } },
 *   { tool: 'users__get', input: { id: '3' } },
 * ]);
 */
export async function batchCallMCPTools<T>(
  calls: MCPToolCall[]
): Promise<T[]> {
  // Execute calls in parallel for efficiency
  return Promise.all(
    calls.map(call => callMCPTool<T>(call.tool, call.input))
  );
}

/**
 * List available tools from an MCP server
 *
 * @param serverName - Name of the MCP server
 * @returns List of available tool names
 *
 * @example
 * const tools = await listServerTools('google_drive');
 * console.log(tools); // ['get_document', 'list_files', 'create_document', ...]
 */
export async function listServerTools(serverName: string): Promise<string[]> {
  const config = loadConfig();
  const serverConfig = config.mcpServers[serverName];

  if (!serverConfig) {
    console.warn(`[MCP] Server '${serverName}' not found in configuration.`);
    return [];
  }

  // For HTTP-based servers, query the tools endpoint
  if (serverConfig.url) {
    try {
      const response = await fetch(`${serverConfig.url}/tools`);
      if (response.ok) {
        const tools = await response.json();
        return Array.isArray(tools) ? tools : tools.tools || [];
      }
    } catch (error) {
      console.warn(`[MCP] Could not list tools for '${serverName}': ${error}`);
    }
  }

  // Return empty list if we can't discover tools
  console.log(`[MCP] Tool discovery not available for '${serverName}'.`);
  console.log(`[MCP] Check the server documentation for available tools.`);
  return [];
}

/**
 * Check if an MCP server is available and responding
 *
 * @param serverName - Name of the MCP server
 * @returns True if server is available
 */
export async function checkServerHealth(serverName: string): Promise<boolean> {
  const config = loadConfig();
  const serverConfig = config.mcpServers[serverName];

  if (!serverConfig?.url) {
    return false;
  }

  try {
    const response = await fetch(`${serverConfig.url}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000), // 5 second timeout
    });
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Get configuration for a specific MCP server
 *
 * @param serverName - Name of the MCP server
 * @returns Server configuration or undefined
 */
export function getServerConfig(serverName: string): MCPServerConfig | undefined {
  const config = loadConfig();
  return config.mcpServers[serverName];
}

// Export types for use in tool wrappers
export type { MCPConfig, MCPServerConfig };
