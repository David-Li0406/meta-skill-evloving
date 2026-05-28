/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * OIDC authentication provider for e3-api-server.
 *
 * Provides OAuth2 Device Flow (RFC 8628) with JWT tokens,
 * compatible with AWS Cognito for cloud deployment.
 */

import { Hono } from 'hono';
import { generateKeyPair, type KeyPair } from './keys.js';
import { createDeviceRoutes, type DeviceFlowConfig } from './device.js';
import { createDiscoveryRoutes } from './discovery.js';

export { generateKeyPair, verifyJwt, type KeyPair, type JwtPayload } from './keys.js';

/**
 * Parse duration string to seconds.
 * Supports: "5s", "15m", "1h", "24h", "90d"
 */
export function parseDuration(duration: string): number {
  const match = duration.match(/^(\d+)(s|m|h|d)$/);
  if (!match) {
    throw new Error(`Invalid duration format: ${duration}. Use format like "5s", "15m", "1h", "90d"`);
  }

  const value = parseInt(match[1], 10);
  const unit = match[2];

  switch (unit) {
    case 's': return value;
    case 'm': return value * 60;
    case 'h': return value * 60 * 60;
    case 'd': return value * 60 * 60 * 24;
    default: throw new Error(`Unknown duration unit: ${unit}`);
  }
}

/**
 * OIDC provider configuration.
 */
export interface OidcConfig {
  /** Server base URL (e.g., http://localhost:3000) */
  baseUrl: string;
  /** Access token expiry duration (default: "1h") */
  tokenExpiry?: string;
  /** Refresh token expiry duration (default: "90d") */
  refreshTokenExpiry?: string;
  /** Auto-approve device codes (for CI testing) */
  autoApprove?: boolean;
}

/**
 * OIDC provider instance.
 */
export interface OidcProvider {
  /** Hono app with all auth routes */
  routes: Hono;
  /** RSA keypair (for validating tokens) */
  keys: KeyPair;
  /** Server base URL */
  baseUrl: string;
  /** Access token expiry in seconds */
  accessTokenExpiry: number;
}

/**
 * Create an OIDC provider for the e3-api-server.
 *
 * This provides:
 * - /.well-known/openid-configuration (discovery)
 * - /.well-known/jwks.json (public keys)
 * - /oauth2/device_authorization (start device flow)
 * - /device (approval page)
 * - /oauth2/token (exchange codes and refresh tokens)
 */
export function createOidcProvider(config: OidcConfig): OidcProvider {
  const keys = generateKeyPair();
  const accessTokenExpiry = parseDuration(config.tokenExpiry ?? '1h');
  const refreshTokenExpiry = parseDuration(config.refreshTokenExpiry ?? '90d');
  const autoApprove = config.autoApprove ?? process.env.E3_AUTH_AUTO_APPROVE === '1';

  const deviceConfig: DeviceFlowConfig = {
    baseUrl: config.baseUrl,
    keys,
    accessTokenExpiry,
    refreshTokenExpiry,
    autoApprove,
  };

  const app = new Hono();

  // Mount discovery routes (/.well-known/*)
  app.route('/', createDiscoveryRoutes({ baseUrl: config.baseUrl, keys }));

  // Mount device flow routes (/oauth2/*, /device)
  app.route('/', createDeviceRoutes(deviceConfig));

  return {
    routes: app,
    keys,
    baseUrl: config.baseUrl,
    accessTokenExpiry,
  };
}
