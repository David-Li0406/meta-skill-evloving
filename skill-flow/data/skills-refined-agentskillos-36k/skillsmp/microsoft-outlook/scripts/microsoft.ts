#!/usr/bin/env npx tsx
/**
 * Microsoft Skill CLI - Microsoft Graph API integration
 */

import fs from "node:fs/promises";
import path from "node:path";
import {
  performAuth,
  performSetup,
  checkAuth,
  getValidAccessToken,
  getProjectTokenPath,
  getGlobalTokenPath,
} from "./lib/auth.js";
import { output, fail } from "./lib/output.js";
import type { MicrosoftUser, MessageListResponse, Message } from "./lib/types.js";

const GRAPH_API_BASE = "https://graph.microsoft.com/v1.0";

// ============================================================================
// API Client
// ============================================================================

async function graphRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  isBinary: boolean = false
): Promise<T> {
  const token = await getValidAccessToken();
  const url = endpoint.startsWith("http") ? endpoint : `${GRAPH_API_BASE}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    let message = `API request failed: ${response.status} ${response.statusText}`;
    try {
      const errorData = await response.json() as any;
      if (errorData.error?.message) {
        message += ` - ${errorData.error.message}`;
      }
    } catch {}
    throw new Error(message);
  }

  if (isBinary) {
    return response.arrayBuffer() as unknown as T;
  }

  return response.json() as Promise<T>;
}

// ============================================================================
// User Commands
// ============================================================================

async function getMe(): Promise<MicrosoftUser> {
  return graphRequest<MicrosoftUser>("/me");
}

// ============================================================================
// Email Commands
// ============================================================================

async function listMessages(limit: number = 10): Promise<Message[]> {
  const response = await graphRequest<MessageListResponse>(
    `/me/messages?$top=${limit}&$select=subject,receivedDateTime,from,isRead,id,hasAttachments`
  );
  return response.value;
}

async function readMessage(messageId: string): Promise<Message> {
  return graphRequest<Message>(`/me/messages/${messageId}`);
}

async function downloadMessage(messageId: string, outputDir: string = "downloads"): Promise<string> {
  const buffer = await graphRequest<ArrayBuffer>(`/me/messages/${messageId}/$value`, {}, true);
  
  // Get message details for filename
  const message = await graphRequest<Message>(`/me/messages/${messageId}?$select=subject`);
  const safeSubject = (message.subject || "No Subject").replace(/[^a-z0-9]/gi, "_").substring(0, 50);
  const filename = `${safeSubject}_${messageId.substring(0, 8)}.eml`;
  const filePath = path.join(outputDir, filename);

  await fs.mkdir(outputDir, { recursive: true });
  await fs.writeFile(filePath, Buffer.from(buffer));
  
  return filePath;
}

async function downloadAllMessages(limit: number = 10, outputDir: string = "downloads"): Promise<string[]> {
  const messages = await listMessages(limit);
  const files: string[] = [];

  console.error(`Found ${messages.length} messages. Downloading...`);
  
  for (const msg of messages) {
    try {
      console.error(`Downloading: ${msg.subject || "No Subject"}`);
      const file = await downloadMessage(msg.id, outputDir);
      files.push(file);
    } catch (err) {
      console.error(`Failed to download message ${msg.id}:`, err);
    }
  }
  
  return files;
}

// ============================================================================
// CLI
// ============================================================================

function printUsage(): void {
  console.log(`
Microsoft Skill CLI

Usage:
  pnpm tsx scripts/microsoft.ts <command> [options]

Commands:
  setup                             Configure API credentials
  auth [--global] [--browser name]  Authenticate with Microsoft
  check                             Check authentication status
  
  me                                Get user profile
  
  messages [--limit 10]             List recent messages
  read <id>                         Get full message details (JSON)
  download <id>                     Download .eml file
  download-all [--limit 10]         Download recent messages
`);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === "help" || command === "--help") {
    printUsage();
    process.exit(0);
  }

  try {
    switch (command) {
      case "auth": {
        const globalFlag = args.includes("--global");
        const browserIdx = args.indexOf("--browser");
        const browser = browserIdx !== -1 ? args[browserIdx + 1] : undefined;
        await performAuth(globalFlag, browser);
        const tokenPath = globalFlag ? getGlobalTokenPath() : getProjectTokenPath();
        output({ authenticated: true, tokenPath });
        break;
      }
      
      case "check": {
        const status = await checkAuth();
        output(status);
        break;
      }

      case "setup": {
        await performSetup();
        output({ setup: true });
        break;
      }

      case "me": {
        const user = await getMe();
        output(user);
        break;
      }

      case "messages": {
        const limitIdx = args.indexOf("--limit");
        const limit = limitIdx !== -1 ? parseInt(args[limitIdx + 1], 10) : 10;
        const messages = await listMessages(limit);
        output(messages);
        break;
      }

      case "read": {
        const id = args[1];
        if (!id) fail("Usage: read <id>");
        const message = await readMessage(id);
        output(message);
        break;
      }

      case "download": {
        const id = args[1];
        if (!id) fail("Usage: download <id>");
        const filePath = await downloadMessage(id);
        output({ file: filePath });
        break;
      }

      case "download-all": {
        const limitIdx = args.indexOf("--limit");
        const limit = limitIdx !== -1 ? parseInt(args[limitIdx + 1], 10) : 10;
        const files = await downloadAllMessages(limit);
        output({ files });
        break;
      }

      default:
        console.error(`Unknown command: ${command}`);
        printUsage();
        process.exit(1);
    }
  } catch (error) {
    fail(error instanceof Error ? error.message : String(error));
  }
}

main();
