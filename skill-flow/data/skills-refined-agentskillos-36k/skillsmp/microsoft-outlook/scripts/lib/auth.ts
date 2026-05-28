/**
 * Microsoft OAuth 2.0 PKCE Authentication
 *
 * Token storage: .claude/microsoft-skill.local.json (project-local)
 * Credentials: ~/.config/microsoft-skill/credentials.json or 1Password
 */

import path from "node:path";
import os from "node:os";
import fs from "node:fs/promises";
import http from "node:http";
import crypto from "node:crypto";
import { execSync, spawn } from "node:child_process";
import * as readline from "node:readline";

// Cross-platform browser open using built-in Node.js
function openBrowser(url: string, browser?: string): void {
  const platform = process.platform;
  let command: string;
  let args: string[];

  if (platform === "darwin") {
    command = "open";
    args = browser ? ["-a", browser, url] : [url];
  } else if (platform === "win32") {
    command = "cmd";
    args = ["/c", "start", "", url];
  } else {
    // Linux and others
    command = "xdg-open";
    args = [url];
  }

  const child = spawn(command, args, {
    detached: true,
    stdio: "ignore",
  });
  child.unref();
}

// ============================================================================ 
// Configuration
// ============================================================================ 

// 1Password references for Microsoft credentials
const OP_CLIENT_ID_REF = "op://Personal/Microsoft Client ID/notesPlain";
const OP_CLIENT_SECRET_REF = "op://Personal/Microsoft Client Secret/notesPlain";

// Global config for OAuth client credentials
export function getGlobalConfigDir(): string {
  const xdgConfig = process.env.XDG_CONFIG_HOME || path.join(os.homedir(), ".config");
  return path.join(xdgConfig, "microsoft-skill");
}

export const GLOBAL_CONFIG_DIR = getGlobalConfigDir();
export const CREDENTIALS_PATH = path.join(GLOBAL_CONFIG_DIR, "credentials.json");

// Project-local token storage
const PROJECT_TOKEN_DIR = ".claude";
const PROJECT_TOKEN_FILE = "microsoft-skill.local.json";

// Global token storage (fallback)
const GLOBAL_TOKEN_FILE = "tokens.json";

export function getProjectTokenPath(): string {
  return path.join(process.cwd(), PROJECT_TOKEN_DIR, PROJECT_TOKEN_FILE);
}

export function getGlobalTokenPath(): string {
  return path.join(GLOBAL_CONFIG_DIR, GLOBAL_TOKEN_FILE);
}

// OAuth endpoints (Microsoft Identity Platform v2.0)
const MS_AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize";
const MS_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token";

// Callback configuration
const CALLBACK_URL = "http://localhost:3000/callback";
const PORT = 3000;

// OAuth scopes
export const SCOPES = [
  "User.Read",
  "Mail.Read",
  "offline_access",
].join(" ");

// ============================================================================ 
// Setup Instructions
// ============================================================================ 

export const SETUP_INSTRUCTIONS = `
═══════════════════════════════════════════════════════════════════════════════
                       MICROSOFT SKILL - FIRST TIME SETUP
═══════════════════════════════════════════════════════════════════════════════

This skill needs Microsoft Graph API credentials to access Outlook/Hotmail.

Run: pnpm tsx scripts/microsoft.ts setup

This will guide you through setting up credentials.

CREDENTIALS STORAGE:
  ${CREDENTIALS_PATH}

TOKENS (per-project):
  .claude/microsoft-skill.local.json

═══════════════════════════════════════════════════════════════════════════════
`;

// ============================================================================ 
// Types
// ============================================================================ 

interface Credentials {
  client_id: string;
  client_secret: string;
}

interface TokenData {
  access_token: string;
  refresh_token: string;
  expires_at: number;
  scope: string;
  token_type: string;
}

// ============================================================================ 
// 1Password Integration
// ============================================================================ 

function is1PasswordAvailable(): boolean {
  try {
    execSync("op --version", { stdio: "pipe" });
    return true;
  } catch {
    return false;
  }
}

function readFrom1Password(reference: string): string | null {
  try {
    const result = execSync(`op read "${reference}"`, {
      stdio: ["pipe", "pipe", "pipe"],
      encoding: "utf-8",
    });
    return result.trim();
  } catch {
    return null;
  }
}

async function loadCredentialsFrom1Password(): Promise<Credentials | null> {
  const clientId = readFrom1Password(OP_CLIENT_ID_REF);
  const clientSecret = readFrom1Password(OP_CLIENT_SECRET_REF);

  if (clientId && clientSecret) {
    return { client_id: clientId, client_secret: clientSecret };
  }
  return null;
}

// ============================================================================ 
// Interactive Setup
// ============================================================================ 

function askQuestion(question: string): Promise<string> {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stderr,
  });

  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

async function credentialsFileExists(): Promise<boolean> {
  try {
    await fs.access(CREDENTIALS_PATH);
    return true;
  } catch {
    return false;
  }
}

export async function performSetup(): Promise<void> {
  console.error(`
═══════════════════════════════════════════════════════════════════════════════
                       MICROSOFT SKILL - CREDENTIAL SETUP
═══════════════════════════════════════════════════════════════════════════════
`);

  if (await credentialsFileExists()) {
    console.error(`Credentials already configured at ${CREDENTIALS_PATH}`);
    const answer = await askQuestion("Overwrite existing credentials? (y/N): ");
    if (answer.toLowerCase() !== "y") {
      console.error("Setup cancelled.");
      return;
    }
  }

  const has1Password = is1PasswordAvailable();

  console.error("How would you like to provide Microsoft API credentials?\n");
  if (has1Password) {
    console.error("  1. Load from 1Password (recommended)");
    console.error("  2. Enter manually");
  } else {
    console.error("  1. Enter manually");
    console.error("  (1Password CLI not detected)");
  }
  console.error("");

  const choice = await askQuestion("Enter choice (1" + (has1Password ? " or 2" : "") + "): ");

  let credentials: Credentials;

  if (has1Password && choice === "1") {
    console.error("\nLoading credentials from 1Password...");
    const opCreds = await loadCredentialsFrom1Password();
    if (!opCreds) {
      console.error("Failed to load credentials from 1Password.");
      console.error(`Ensure you have ${OP_CLIENT_ID_REF} and ${OP_CLIENT_SECRET_REF}`);
      throw new Error("1Password credentials not found");
    }
    credentials = opCreds;
    console.error("✓ Loaded credentials from 1Password");
  } else {
    console.error("\nEnter your Microsoft API credentials:");
    console.error("(Register at https://entra.microsoft.com/)\n");

    const clientId = await askQuestion("Client ID: ");
    const clientSecret = await askQuestion("Client Secret: ");

    if (!clientId || !clientSecret) {
      throw new Error("Both Client ID and Client Secret are required");
    }

    credentials = { client_id: clientId, client_secret: clientSecret };
  }

  await fs.mkdir(GLOBAL_CONFIG_DIR, { recursive: true });
  await fs.writeFile(CREDENTIALS_PATH, JSON.stringify(credentials, null, 2));
  console.error(`\n✓ Credentials saved to ${CREDENTIALS_PATH}`);
  console.error("\nNext step: Run 'pnpm tsx scripts/microsoft.ts auth' to authenticate.");
}

// ============================================================================ 
// Credential & Token Management
// ============================================================================ 

export async function loadCredentials(): Promise<Credentials> {
  try {
    const content = await fs.readFile(CREDENTIALS_PATH, "utf-8");
    const data = JSON.parse(content);
    if (data.client_id && data.client_secret) return data;
  } catch {}

  if (is1PasswordAvailable()) {
    const opCreds = await loadCredentialsFrom1Password();
    if (opCreds) return opCreds;
  }

  throw new Error(
    `No credentials found. Run: pnpm tsx scripts/microsoft.ts setup`
  );
}

export async function findTokenPath(): Promise<string | null> {
  const projectPath = getProjectTokenPath();
  try {
    await fs.access(projectPath);
    return projectPath;
  } catch {}

  const globalPath = getGlobalTokenPath();
  try {
    await fs.access(globalPath);
    return globalPath;
  } catch {}
  
  return null;
}

export async function loadToken(): Promise<TokenData> {
  const tokenPath = await findTokenPath();

  if (!tokenPath) {
    throw new Error(
      `Token not found. Run: pnpm tsx scripts/microsoft.ts auth`
    );
  }

  const content = await fs.readFile(tokenPath, "utf-8");
  return JSON.parse(content) as TokenData;
}

export async function saveToken(tokenData: TokenData, global: boolean = false): Promise<void> {
  const tokenPath = global ? getGlobalTokenPath() : getProjectTokenPath();
  const tokenDir = path.dirname(tokenPath);

  await fs.mkdir(tokenDir, { recursive: true });
  await fs.writeFile(tokenPath, JSON.stringify(tokenData, null, 2));
}

// ============================================================================ 
// PKCE Helpers
// ============================================================================ 

function generateCodeVerifier(): string {
  return crypto.randomBytes(32).toString("base64url");
}

function generateCodeChallenge(verifier: string): string {
  return crypto.createHash("sha256").update(verifier).digest("base64url");
}

function generateState(): string {
  return crypto.randomBytes(16).toString("hex");
}

// ============================================================================ 
// Token Refresh
// ============================================================================ 

async function refreshAccessToken(credentials: Credentials, refreshToken: string, tokenPath: string): Promise<TokenData> {
  const response = await fetch(MS_TOKEN_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      client_id: credentials.client_id,
      client_secret: credentials.client_secret,
      grant_type: "refresh_token",
      refresh_token: refreshToken,
      scope: SCOPES,
    }),
  });

  const data = await response.json() as any;

  if (data.error) {
    throw new Error(`Token refresh failed: ${data.error_description || data.error}`);
  }

  const tokenData: TokenData = {
    access_token: data.access_token,
    refresh_token: data.refresh_token || refreshToken, // Microsoft sometimes rotates, sometimes doesn't
    expires_at: Date.now() + (data.expires_in || 3600) * 1000,
    scope: data.scope || SCOPES,
    token_type: data.token_type || "Bearer",
  };

  const isGlobal = tokenPath === getGlobalTokenPath();
  await saveToken(tokenData, isGlobal);
  return tokenData;
}

// ============================================================================ 
// Get Valid Access Token
// ============================================================================ 

export async function getValidAccessToken(): Promise<string> {
  const credentials = await loadCredentials();
  const tokenPath = await findTokenPath();

  if (!tokenPath) {
    throw new Error(`Token not found. Run: pnpm tsx scripts/microsoft.ts auth`);
  }

  const content = await fs.readFile(tokenPath, "utf-8");
  let tokenData = JSON.parse(content) as TokenData;

  const bufferMs = 5 * 60 * 1000;
  if (tokenData.expires_at < Date.now() + bufferMs) {
    console.error("Token expiring soon, refreshing...");
    tokenData = await refreshAccessToken(credentials, tokenData.refresh_token, tokenPath);
  }

  return tokenData.access_token;
}

// ============================================================================ 
// Gitignore Management
// ============================================================================ 

export async function ensureGitignore(): Promise<void> {
  const gitignorePath = path.join(process.cwd(), ".gitignore");
  const pattern = ".claude/*.local.*";

  try {
    const content = await fs.readFile(gitignorePath, "utf-8");
    if (!content.includes(pattern)) {
      await fs.writeFile(gitignorePath, content + `\n# Microsoft skill tokens\n${pattern}\n`);
      console.error(`✓ Added ${pattern} to .gitignore`);
    }
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") {
      await fs.writeFile(gitignorePath, `# Microsoft skill tokens\n${pattern}\n`);
      console.error(`✓ Created .gitignore with ${pattern}`);
    }
  }
}

// ============================================================================ 
// OAuth Flow
// ============================================================================ 

export async function performAuth(global: boolean = false, browser?: string): Promise<void> {
  const credentials = await loadCredentials();
  const tokenPath = global ? getGlobalTokenPath() : getProjectTokenPath();
  const tokenDir = path.dirname(tokenPath);

  await fs.mkdir(tokenDir, { recursive: true });
  if (!global) await ensureGitignore();

  const codeVerifier = generateCodeVerifier();
  const codeChallenge = generateCodeChallenge(codeVerifier);
  const state = generateState();

  const authUrl = new URL(MS_AUTH_URL);
  authUrl.searchParams.set("client_id", credentials.client_id);
  authUrl.searchParams.set("response_type", "code");
  authUrl.searchParams.set("redirect_uri", CALLBACK_URL);
  authUrl.searchParams.set("response_mode", "query");
  authUrl.searchParams.set("scope", SCOPES);
  authUrl.searchParams.set("state", state);
  authUrl.searchParams.set("code_challenge", codeChallenge);
  authUrl.searchParams.set("code_challenge_method", "S256");

  console.error("\nOpening browser for authentication...");
  console.error("If browser doesn't open, visit:\n", authUrl.toString(), "\n");

  const code = await new Promise<string>((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const url = new URL(req.url!, `http://localhost:${PORT}`);
      const returnedCode = url.searchParams.get("code");
      const returnedState = url.searchParams.get("state");
      const error = url.searchParams.get("error");

      if (error) {
        res.writeHead(400);
        res.end(`Error: ${error}`);
        server.close();
        reject(new Error(error));
        return;
      }

      if (returnedState !== state) {
        res.writeHead(400);
        res.end("Error: State mismatch");
        server.close();
        reject(new Error("State mismatch"));
        return;
      }

      if (returnedCode) {
        res.writeHead(200, { "Content-Type": "text/html" });
        res.end("<h1>Success!</h1><p>You can close this window.</p>");
        server.close();
        resolve(returnedCode);
        return;
      }
      res.writeHead(404);
      res.end();
    });

    server.listen(PORT, () => {
      try { openBrowser(authUrl.toString(), browser); }
      catch { console.error("Could not open browser automatically."); }
    });

    setTimeout(() => {
      server.close();
      reject(new Error("Timeout"));
    }, 300000);
  });

  const response = await fetch(MS_TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: credentials.client_id,
      client_secret: credentials.client_secret,
      code,
      redirect_uri: CALLBACK_URL,
      grant_type: "authorization_code",
      code_verifier: codeVerifier,
    }),
  });

  const data = await response.json() as any;

  if (data.error) {
    throw new Error(`Token exchange failed: ${data.error_description || data.error}`);
  }

  const tokenData: TokenData = {
    access_token: data.access_token,
    refresh_token: data.refresh_token,
    expires_at: Date.now() + (data.expires_in || 3600) * 1000,
    scope: data.scope,
    token_type: data.token_type,
  };

  await saveToken(tokenData, global);
  console.error(`\n✓ Token saved to ${tokenPath}`);
  process.exit(0);
}

export async function checkAuth(): Promise<{ authenticated: boolean; expiresAt?: Date; error?: string }> {
  try {
    const tokenData = await loadToken();
    return {
      authenticated: tokenData.expires_at > Date.now(),
      expiresAt: new Date(tokenData.expires_at),
    };
  } catch (error) {
    return { authenticated: false, error: String(error) };
  }
}
