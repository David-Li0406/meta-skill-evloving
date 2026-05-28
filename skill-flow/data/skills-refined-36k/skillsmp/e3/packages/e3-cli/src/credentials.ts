/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Credential storage for e3 CLI.
 *
 * Stores access and refresh tokens for authenticated servers
 * in ~/.e3/credentials.json.
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import * as os from 'node:os';

/**
 * Single credential entry for a server.
 */
export interface CredentialEntry {
  /** JWT access token */
  accessToken: string;
  /** JWT refresh token */
  refreshToken: string;
  /** Access token expiration (ISO 8601) */
  expiresAt: string;
}

/**
 * Credentials file structure.
 */
export interface CredentialsFile {
  /** File format version */
  version: 1;
  /** Credentials keyed by server URL (normalized, no trailing slash) */
  credentials: Record<string, CredentialEntry>;
}

/**
 * OIDC Discovery document.
 */
export interface OidcDiscovery {
  issuer: string;
  device_authorization_endpoint: string;
  token_endpoint: string;
  jwks_uri: string;
}

/**
 * Device authorization response.
 */
export interface DeviceAuthResponse {
  device_code: string;
  user_code: string;
  verification_uri: string;
  verification_uri_complete: string;
  expires_in: number;
  interval: number;
}

/**
 * Token response from OAuth2 token endpoint.
 */
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

/**
 * Token error response.
 */
export interface TokenErrorResponse {
  error: string;
  error_description?: string;
}

/**
 * Get path to credentials file.
 * Uses E3_CREDENTIALS_PATH env var if set, otherwise ~/.e3/credentials.json.
 */
function getCredentialsPath(): string {
  return process.env.E3_CREDENTIALS_PATH ?? path.join(os.homedir(), '.e3', 'credentials.json');
}

/**
 * Normalize server URL (remove trailing slash).
 */
export function normalizeServerUrl(url: string): string {
  return url.replace(/\/+$/, '');
}

/**
 * Load credentials file.
 */
export function loadCredentials(): CredentialsFile {
  try {
    const content = fs.readFileSync(getCredentialsPath(), 'utf8');
    return JSON.parse(content) as CredentialsFile;
  } catch {
    return { version: 1, credentials: {} };
  }
}

/**
 * Save credentials file.
 */
export function saveCredentials(file: CredentialsFile): void {
  const credPath = getCredentialsPath();
  const dir = path.dirname(credPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  }
  fs.writeFileSync(credPath, JSON.stringify(file, null, 2), { mode: 0o600 });
}

/**
 * Get credential for a server.
 */
export function getCredential(serverUrl: string): CredentialEntry | null {
  const file = loadCredentials();
  return file.credentials[normalizeServerUrl(serverUrl)] ?? null;
}

/**
 * Set credential for a server.
 */
export function setCredential(serverUrl: string, entry: CredentialEntry): void {
  const file = loadCredentials();
  file.credentials[normalizeServerUrl(serverUrl)] = entry;
  saveCredentials(file);
}

/**
 * Remove credential for a server.
 */
export function removeCredential(serverUrl: string): boolean {
  const file = loadCredentials();
  const key = normalizeServerUrl(serverUrl);
  if (key in file.credentials) {
    delete file.credentials[key];
    saveCredentials(file);
    return true;
  }
  return false;
}

/**
 * List all saved credentials.
 */
export function listCredentials(): Array<{ server: string; expiresAt: string }> {
  const file = loadCredentials();
  return Object.entries(file.credentials).map(([server, entry]) => ({
    server,
    expiresAt: entry.expiresAt,
  }));
}

/**
 * Check if a token expiration time has passed.
 */
export function isExpired(expiresAt: string): boolean {
  return new Date(expiresAt).getTime() < Date.now();
}

/**
 * Fetch OIDC discovery document.
 */
export async function fetchDiscovery(serverUrl: string): Promise<OidcDiscovery> {
  const url = `${normalizeServerUrl(serverUrl)}/.well-known/openid-configuration`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch OIDC discovery: ${response.status}`);
  }
  return response.json() as Promise<OidcDiscovery>;
}

/**
 * Start device authorization flow.
 */
export async function startDeviceAuth(discovery: OidcDiscovery): Promise<DeviceAuthResponse> {
  const response = await fetch(discovery.device_authorization_endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ client_id: 'e3-cli' }),
  });
  if (!response.ok) {
    throw new Error(`Failed to start device authorization: ${response.status}`);
  }
  return response.json() as Promise<DeviceAuthResponse>;
}

/**
 * Poll for device code approval.
 */
export async function pollForTokens(
  discovery: OidcDiscovery,
  deviceCode: string,
  interval: number,
  expiresIn: number
): Promise<TokenResponse> {
  const deadline = Date.now() + expiresIn * 1000;

  while (Date.now() < deadline) {
    await new Promise((resolve) => setTimeout(resolve, interval * 1000));

    const response = await fetch(discovery.token_endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
        device_code: deviceCode,
        client_id: 'e3-cli',
      }),
    });

    if (response.ok) {
      return response.json() as Promise<TokenResponse>;
    }

    const error = await response.json() as TokenErrorResponse;
    if (error.error === 'authorization_pending') {
      continue; // Keep polling
    }
    if (error.error === 'slow_down') {
      interval += 1; // Slow down as requested
      continue;
    }
    throw new Error(`Token exchange failed: ${error.error} - ${error.error_description ?? ''}`);
  }

  throw new Error('Device authorization timed out');
}

/**
 * Refresh an access token using a refresh token.
 */
export async function refreshAccessToken(
  serverUrl: string,
  refreshToken: string
): Promise<TokenResponse> {
  const discovery = await fetchDiscovery(serverUrl);
  const response = await fetch(discovery.token_endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
      client_id: 'e3-cli',
    }),
  });

  if (!response.ok) {
    const error = await response.json() as TokenErrorResponse;
    throw new Error(`Token refresh failed: ${error.error} - ${error.error_description ?? ''}`);
  }

  return response.json() as Promise<TokenResponse>;
}

/**
 * Get a valid access token for a server.
 *
 * If the current token is expired, attempts to refresh it.
 * Throws if not logged in or refresh fails.
 */
export async function getValidToken(serverUrl: string): Promise<string> {
  const creds = getCredential(serverUrl);
  if (!creds) {
    throw new Error(`Not logged in to ${serverUrl}. Run: e3 login ${serverUrl}`);
  }

  // Return existing token if not expired
  if (!isExpired(creds.expiresAt)) {
    return creds.accessToken;
  }

  // Attempt to refresh
  try {
    const tokens = await refreshAccessToken(serverUrl, creds.refreshToken);
    const newEntry: CredentialEntry = {
      accessToken: tokens.access_token,
      refreshToken: tokens.refresh_token,
      expiresAt: new Date(Date.now() + tokens.expires_in * 1000).toISOString(),
    };
    setCredential(serverUrl, newEntry);
    return tokens.access_token;
  } catch (err) {
    // Refresh failed, need to re-login
    removeCredential(serverUrl);
    const message = err instanceof Error ? err.message : 'unknown error';
    throw new Error(`Session expired and refresh failed: ${message}. Run: e3 login ${serverUrl}`);
  }
}

/**
 * Decode JWT payload without verification (for display purposes only).
 */
export function decodeJwtPayload(token: string): Record<string, unknown> {
  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Invalid JWT format');
  }
  return JSON.parse(Buffer.from(parts[1], 'base64url').toString()) as Record<string, unknown>;
}
