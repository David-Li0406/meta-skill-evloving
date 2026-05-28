/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * OIDC Discovery endpoint (/.well-known/openid-configuration).
 */

import { Hono } from 'hono';
import type { KeyPair } from './keys.js';
import { publicKeyToJwk } from './keys.js';

/**
 * Discovery configuration.
 */
export interface DiscoveryConfig {
  /** Server base URL (e.g., http://localhost:3000) */
  baseUrl: string;
  /** RSA keypair for JWKS */
  keys: KeyPair;
}

/**
 * Create discovery routes.
 */
export function createDiscoveryRoutes(config: DiscoveryConfig): Hono {
  const app = new Hono();

  // GET /.well-known/openid-configuration - OIDC Discovery
  app.get('/.well-known/openid-configuration', (c) => {
    return c.json({
      issuer: config.baseUrl,
      device_authorization_endpoint: `${config.baseUrl}/oauth2/device_authorization`,
      token_endpoint: `${config.baseUrl}/oauth2/token`,
      jwks_uri: `${config.baseUrl}/.well-known/jwks.json`,
      response_types_supported: ['token'],
      grant_types_supported: [
        'urn:ietf:params:oauth:grant-type:device_code',
        'refresh_token',
      ],
      subject_types_supported: ['public'],
      id_token_signing_alg_values_supported: ['RS256'],
      token_endpoint_auth_methods_supported: ['none'],
    });
  });

  // GET /.well-known/jwks.json - JSON Web Key Set
  app.get('/.well-known/jwks.json', (c) => {
    return c.json({
      keys: [publicKeyToJwk(config.keys)],
    });
  });

  return app;
}
