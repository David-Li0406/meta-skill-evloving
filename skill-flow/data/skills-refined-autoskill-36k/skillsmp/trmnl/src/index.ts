#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { TRMNLClient } from "./api.js";

const API_KEY = process.env.TRMNL_API_KEY;

if (!API_KEY) {
  console.error("Error: TRMNL_API_KEY environment variable is required");
  process.exit(1);
}

const client = new TRMNLClient(API_KEY);

const server = new Server(
  {
    name: "trmnl-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "trmnl_list_devices",
        description: "List all your TRMNL devices with their status (battery, signal strength, etc.)",
        inputSchema: {
          type: "object" as const,
          properties: {},
        },
      },
      {
        name: "trmnl_get_device",
        description: "Get detailed information about a specific TRMNL device",
        inputSchema: {
          type: "object" as const,
          properties: {
            device_id: {
              type: "number",
              description: "The device ID",
            },
          },
          required: ["device_id"],
        },
      },
      {
        name: "trmnl_update_device",
        description: "Update device settings like sleep mode",
        inputSchema: {
          type: "object" as const,
          properties: {
            device_id: {
              type: "number",
              description: "The device ID",
            },
            sleep_mode_enabled: {
              type: "boolean",
              description: "Enable or disable sleep mode",
            },
            sleep_start_time: {
              type: "string",
              description: "Sleep start time (HH:MM format)",
            },
            sleep_end_time: {
              type: "string",
              description: "Sleep end time (HH:MM format)",
            },
          },
          required: ["device_id"],
        },
      },
      {
        name: "trmnl_get_current_screen",
        description: "Get the currently displayed screen on a device (requires device API key)",
        inputSchema: {
          type: "object" as const,
          properties: {
            device_api_key: {
              type: "string",
              description: "The device-specific API key (found in device settings)",
            },
          },
          required: ["device_api_key"],
        },
      },
      {
        name: "trmnl_advance_screen",
        description: "Advance to the next screen in the playlist (requires device API key)",
        inputSchema: {
          type: "object" as const,
          properties: {
            device_api_key: {
              type: "string",
              description: "The device-specific API key (found in device settings)",
            },
          },
          required: ["device_api_key"],
        },
      },
      {
        name: "trmnl_list_playlist",
        description: "List all items in your TRMNL playlist",
        inputSchema: {
          type: "object" as const,
          properties: {},
        },
      },
      {
        name: "trmnl_toggle_playlist_item",
        description: "Show or hide a playlist item",
        inputSchema: {
          type: "object" as const,
          properties: {
            item_id: {
              type: "number",
              description: "The playlist item ID",
            },
            visible: {
              type: "boolean",
              description: "Whether the item should be visible",
            },
          },
          required: ["item_id", "visible"],
        },
      },
      {
        name: "trmnl_list_plugins",
        description: "List all plugin settings/instances",
        inputSchema: {
          type: "object" as const,
          properties: {
            plugin_id: {
              type: "number",
              description: "Optional: filter by plugin ID",
            },
          },
        },
      },
      {
        name: "trmnl_get_plugin_data",
        description: "Get the current data/variables for a plugin instance",
        inputSchema: {
          type: "object" as const,
          properties: {
            plugin_setting_id: {
              type: "number",
              description: "The plugin setting ID",
            },
          },
          required: ["plugin_setting_id"],
        },
      },
      {
        name: "trmnl_update_plugin_data",
        description: "Update the merge variables for a plugin instance",
        inputSchema: {
          type: "object" as const,
          properties: {
            plugin_setting_id: {
              type: "number",
              description: "The plugin setting ID",
            },
            merge_variables: {
              type: "object",
              description: "The data to merge into the plugin",
            },
          },
          required: ["plugin_setting_id", "merge_variables"],
        },
      },
      {
        name: "trmnl_push_webhook",
        description: "Push custom content to a private plugin via webhook",
        inputSchema: {
          type: "object" as const,
          properties: {
            uuid: {
              type: "string",
              description: "The plugin webhook UUID (found in plugin settings)",
            },
            merge_variables: {
              type: "object",
              description: "The data to display on the screen",
            },
            merge_strategy: {
              type: "string",
              enum: ["deep_merge", "stream"],
              description: "Optional: how to merge the data (deep_merge or stream)",
            },
            stream_limit: {
              type: "number",
              description: "Optional: max items when using stream strategy",
            },
          },
          required: ["uuid", "merge_variables"],
        },
      },
      {
        name: "trmnl_get_webhook_content",
        description: "Get the current content of a webhook plugin",
        inputSchema: {
          type: "object" as const,
          properties: {
            uuid: {
              type: "string",
              description: "The plugin webhook UUID",
            },
          },
          required: ["uuid"],
        },
      },
      {
        name: "trmnl_get_account",
        description: "Get your TRMNL account information",
        inputSchema: {
          type: "object" as const,
          properties: {},
        },
      },
      {
        name: "trmnl_delete_plugin",
        description: "Delete a plugin setting/instance",
        inputSchema: {
          type: "object" as const,
          properties: {
            plugin_setting_id: {
              type: "number",
              description: "The plugin setting ID to delete",
            },
          },
          required: ["plugin_setting_id"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "trmnl_list_devices": {
        const result = await client.listDevices();
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_get_device": {
        const { device_id } = args as { device_id: number };
        const result = await client.getDevice(device_id);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_update_device": {
        const { device_id, sleep_mode_enabled, sleep_start_time, sleep_end_time } =
          args as {
            device_id: number;
            sleep_mode_enabled?: boolean;
            sleep_start_time?: string;
            sleep_end_time?: string;
          };
        const updates: Record<string, unknown> = {};
        if (sleep_mode_enabled !== undefined)
          updates.sleep_mode_enabled = sleep_mode_enabled;
        if (sleep_start_time) updates.sleep_start_time = sleep_start_time;
        if (sleep_end_time) updates.sleep_end_time = sleep_end_time;
        const result = await client.updateDevice(device_id, updates);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_get_current_screen": {
        const { device_api_key } = args as { device_api_key: string };
        const result = await client.getCurrentScreen(device_api_key);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_advance_screen": {
        const { device_api_key } = args as { device_api_key: string };
        const result = await client.advanceScreen(device_api_key);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_list_playlist": {
        const result = await client.listPlaylistItems();
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_toggle_playlist_item": {
        const { item_id, visible } = args as { item_id: number; visible: boolean };
        const result = await client.updatePlaylistItem(item_id, visible);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_list_plugins": {
        const { plugin_id } = args as { plugin_id?: number };
        const result = await client.listPluginSettings(plugin_id);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_get_plugin_data": {
        const { plugin_setting_id } = args as { plugin_setting_id: number };
        const result = await client.getPluginData(plugin_setting_id);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_update_plugin_data": {
        const { plugin_setting_id, merge_variables } = args as {
          plugin_setting_id: number;
          merge_variables: Record<string, unknown>;
        };
        const result = await client.updatePluginData(plugin_setting_id, merge_variables);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_push_webhook": {
        const { uuid, merge_variables, merge_strategy, stream_limit } = args as {
          uuid: string;
          merge_variables: Record<string, unknown>;
          merge_strategy?: "deep_merge" | "stream";
          stream_limit?: number;
        };
        const result = await client.pushWebhookContent(
          uuid,
          merge_variables,
          merge_strategy,
          stream_limit
        );
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_get_webhook_content": {
        const { uuid } = args as { uuid: string };
        const result = await client.getWebhookContent(uuid);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_get_account": {
        const result = await client.getAccount();
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "trmnl_delete_plugin": {
        const { plugin_setting_id } = args as { plugin_setting_id: number };
        await client.deletePluginSetting(plugin_setting_id);
        return {
          content: [
            {
              type: "text" as const,
              text: `Plugin setting ${plugin_setting_id} deleted successfully`,
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      content: [
        {
          type: "text" as const,
          text: `Error: ${message}`,
        },
      ],
      isError: true,
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("TRMNL MCP server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
