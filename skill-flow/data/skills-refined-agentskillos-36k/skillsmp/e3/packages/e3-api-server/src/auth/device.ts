/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * OAuth2 Device Authorization Grant (RFC 8628) implementation.
 */

import * as crypto from 'node:crypto';
import { Hono } from 'hono';
import type { KeyPair, JwtPayload } from './keys.js';
import { signJwt } from './keys.js';

/**
 * Pending device authorization.
 */
interface PendingAuth {
  userCode: string;
  approved: boolean;
  expiresAt: number;
}

/**
 * Device flow configuration.
 */
export interface DeviceFlowConfig {
  /** Server base URL (e.g., http://localhost:3000) */
  baseUrl: string;
  /** RSA keypair for signing tokens */
  keys: KeyPair;
  /** Access token expiry in seconds (default: 3600 = 1 hour) */
  accessTokenExpiry: number;
  /** Refresh token expiry in seconds (default: 7776000 = 90 days) */
  refreshTokenExpiry: number;
  /** Auto-approve device codes (for CI testing) */
  autoApprove: boolean;
}

// In-memory pending authorizations
const pendingAuths = new Map<string, PendingAuth>();

// Clean up expired authorizations periodically
// Use unref() so this timer doesn't prevent process exit
const cleanupInterval = setInterval(() => {
  const now = Date.now();
  for (const [deviceCode, auth] of pendingAuths) {
    if (auth.expiresAt < now) {
      pendingAuths.delete(deviceCode);
    }
  }
}, 60000); // Every minute
cleanupInterval.unref();

/**
 * Generate a random device code.
 */
function generateDeviceCode(): string {
  return crypto.randomBytes(32).toString('hex');
}

/**
 * Generate a user-friendly code (e.g., ABCD-1234).
 */
function generateUserCode(): string {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // Exclude confusing chars
  let code = '';
  for (let i = 0; i < 8; i++) {
    if (i === 4) code += '-';
    code += chars[crypto.randomInt(chars.length)];
  }
  return code;
}

/**
 * Create device flow routes.
 */
export function createDeviceRoutes(config: DeviceFlowConfig): Hono {
  const app = new Hono();

  // POST /oauth2/device_authorization - Start device flow
  app.post('/oauth2/device_authorization', (c) => {
    const deviceCode = generateDeviceCode();
    const userCode = generateUserCode();
    const expiresIn = 300; // 5 minutes

    pendingAuths.set(deviceCode, {
      userCode,
      approved: config.autoApprove, // Auto-approve in CI mode
      expiresAt: Date.now() + expiresIn * 1000,
    });

    return c.json({
      device_code: deviceCode,
      user_code: userCode,
      verification_uri: `${config.baseUrl}/device`,
      verification_uri_complete: `${config.baseUrl}/device?user_code=${userCode}`,
      expires_in: expiresIn,
      interval: 1, // Poll every 1 second (fast for dev)
    });
  });

  // GET /device - HTML approval page
  app.get('/device', (c) => {
    const userCode = c.req.query('user_code') || '';
    const autoApproveScript = config.autoApprove
      ? `<script>setTimeout(() => document.forms[0].submit(), 500);</script>`
      : '';

    return c.html(`<!DOCTYPE html>
<html>
<head>
  <title>e3 Device Login</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
    h1 { color: #333; }
    .code { font-size: 2em; font-family: monospace; letter-spacing: 0.1em; background: #f0f0f0; padding: 10px 20px; border-radius: 4px; }
    button { background: #0066cc; color: white; border: none; padding: 12px 24px; font-size: 1em; border-radius: 4px; cursor: pointer; margin-top: 20px; }
    button:hover { background: #0055aa; }
    .auto { color: #666; font-style: italic; margin-top: 10px; }
  </style>
</head>
<body>
  <h1>e3 Device Login</h1>
  <p>Confirm this code matches what's shown in your terminal:</p>
  <div class="code">${userCode || '(no code)'}</div>
  <form method="POST" action="/device/approve">
    <input type="hidden" name="user_code" value="${userCode}">
    <button type="submit">Approve</button>
  </form>
  ${config.autoApprove ? '<p class="auto">Auto-approving in CI mode...</p>' : ''}
  ${autoApproveScript}
</body>
</html>`);
  });

  // POST /device/approve - Approve device code
  app.post('/device/approve', async (c) => {
    const body = await c.req.parseBody();
    const userCode = String(body['user_code'] || '');

    // Find the pending auth with this user code
    for (const [_deviceCode, auth] of pendingAuths) {
      if (auth.userCode === userCode && auth.expiresAt > Date.now()) {
        auth.approved = true;
        return c.html(`<!DOCTYPE html>
<html>
<head>
  <title>e3 Device Login</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
    h1 { color: #22aa22; }
  </style>
</head>
<body>
  <h1>✓ Approved</h1>
  <p>You can close this window and return to your terminal.</p>
</body>
</html>`);
      }
    }

    return c.html(`<!DOCTYPE html>
<html>
<head>
  <title>e3 Device Login</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
    h1 { color: #cc0000; }
  </style>
</head>
<body>
  <h1>✗ Invalid or Expired Code</h1>
  <p>The code may have expired. Please try again.</p>
</body>
</html>`, 400);
  });

  // POST /oauth2/token - Exchange device code for tokens OR refresh tokens
  app.post('/oauth2/token', async (c) => {
    const body = await c.req.parseBody();
    const grantType = String(body['grant_type'] || '');

    // Device code grant
    if (grantType === 'urn:ietf:params:oauth:grant-type:device_code') {
      const deviceCode = String(body['device_code'] || '');
      const auth = pendingAuths.get(deviceCode);

      if (!auth || auth.expiresAt < Date.now()) {
        return c.json({ error: 'expired_token' }, 400);
      }

      if (!auth.approved) {
        return c.json({ error: 'authorization_pending' }, 400);
      }

      // Delete the pending auth
      pendingAuths.delete(deviceCode);

      // Generate tokens
      const now = Math.floor(Date.now() / 1000);
      const accessPayload: JwtPayload = {
        sub: 'dev-user',
        iss: config.baseUrl,
        aud: config.baseUrl,
        iat: now,
        nbf: now,
        exp: now + config.accessTokenExpiry,
        token_type: 'access',
      };
      const refreshPayload: JwtPayload = {
        sub: 'dev-user',
        iss: config.baseUrl,
        aud: config.baseUrl,
        iat: now,
        nbf: now,
        exp: now + config.refreshTokenExpiry,
        token_type: 'refresh',
      };

      return c.json({
        access_token: signJwt(accessPayload, config.keys),
        refresh_token: signJwt(refreshPayload, config.keys),
        token_type: 'Bearer',
        expires_in: config.accessTokenExpiry,
      });
    }

    // Refresh token grant
    if (grantType === 'refresh_token') {
      const refreshToken = String(body['refresh_token'] || '');

      try {
        // Import verifyJwt dynamically to avoid circular dependency
        const { verifyJwt } = await import('./keys.js');
        const payload = verifyJwt(refreshToken, config.keys);

        if (payload.token_type !== 'refresh') {
          return c.json({ error: 'invalid_grant', error_description: 'Not a refresh token' }, 400);
        }

        // Generate new access token
        const now = Math.floor(Date.now() / 1000);
        const accessPayload: JwtPayload = {
          sub: payload.sub,
          iss: config.baseUrl,
          aud: config.baseUrl,
          iat: now,
          nbf: now,
          exp: now + config.accessTokenExpiry,
          token_type: 'access',
        };

        // Also issue a new refresh token (rotation)
        const newRefreshPayload: JwtPayload = {
          sub: payload.sub,
          iss: config.baseUrl,
          aud: config.baseUrl,
          iat: now,
          nbf: now,
          exp: now + config.refreshTokenExpiry,
          token_type: 'refresh',
        };

        return c.json({
          access_token: signJwt(accessPayload, config.keys),
          refresh_token: signJwt(newRefreshPayload, config.keys),
          token_type: 'Bearer',
          expires_in: config.accessTokenExpiry,
        });
      } catch {
        return c.json({ error: 'invalid_grant', error_description: 'Invalid refresh token' }, 400);
      }
    }

    return c.json({ error: 'unsupported_grant_type' }, 400);
  });

  return app;
}
