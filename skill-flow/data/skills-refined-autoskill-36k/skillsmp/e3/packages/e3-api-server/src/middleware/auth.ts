/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as fs from 'node:fs/promises';
import * as crypto from 'node:crypto';
import type { MiddlewareHandler } from 'hono';
import type { KeyPair } from '../auth/keys.js';

/**
 * JWT authentication configuration.
 *
 * Supports three modes:
 * 1. publicKeyPath - Load key from PEM file
 * 2. jwksUrl - Fetch keys from JWKS endpoint (for Cognito/external providers)
 * 3. _internalKeys - Use provided KeyPair directly (for built-in OIDC provider)
 */
export interface AuthConfig {
  /** Path to public key file (PEM format) for RS256 signature verification */
  publicKeyPath?: string;
  /** URL to JWKS endpoint for fetching public keys */
  jwksUrl?: string;
  /** Expected issuer claim (iss) */
  issuer: string;
  /** Expected audience claim (aud) */
  audience: string;
  /** Internal: direct KeyPair for built-in OIDC provider (avoids self-fetch) */
  _internalKeys?: KeyPair;
}

/**
 * JWT payload claims.
 */
interface JwtPayload {
  /** Subject - typically user ID */
  sub?: string;
  /** User email */
  email?: string;
  /** User roles */
  roles?: string[];
  /** Issuer */
  iss?: string;
  /** Audience */
  aud?: string;
  /** Expiration time (Unix timestamp) */
  exp?: number;
  /** Not before time (Unix timestamp) */
  nbf?: number;
  /** Issued at time (Unix timestamp) */
  iat?: number;
}

/**
 * Identity information extracted from JWT and set on context.
 */
export interface Identity {
  /** Subject - typically user ID */
  sub: string;
  /** User email (if present in token) */
  email?: string;
  /** User roles (if present in token) */
  roles: string[];
}

/**
 * JWKS key entry.
 */
interface JwksKey {
  kid: string;
  kty: string;
  alg: string;
  use?: string;
  n: string;
  e: string;
}

/**
 * JWKS response structure.
 */
interface JwksResponse {
  keys: JwksKey[];
}

/**
 * Cached JWKS keys.
 */
interface JwksCache {
  keys: Map<string, crypto.KeyObject>;
  fetchedAt: number;
}

// Cache JWKS for 5 minutes
const JWKS_CACHE_TTL = 5 * 60 * 1000;

/**
 * Create JWT authentication middleware.
 *
 * The middleware:
 * 1. Extracts Bearer token from Authorization header
 * 2. Verifies RS256 signature using the configured public key
 * 3. Validates exp, nbf, iss, and aud claims
 * 4. Sets identity on Hono context (accessible via c.get('identity'))
 *
 * @param config - Authentication configuration
 * @returns Hono middleware handler
 */
export async function createAuthMiddleware(config: AuthConfig): Promise<MiddlewareHandler> {
  // Determine key source
  let getPublicKey: (kid?: string) => Promise<crypto.KeyObject>;

  if (config._internalKeys) {
    // Use provided KeyPair directly (built-in OIDC provider)
    const keys = config._internalKeys;
    getPublicKey = () => Promise.resolve(keys.publicKey);
  } else if (config.publicKeyPath) {
    // Load public key from file at startup
    const publicKeyPem = await fs.readFile(config.publicKeyPath, 'utf8');
    const publicKey = crypto.createPublicKey(publicKeyPem);
    getPublicKey = () => Promise.resolve(publicKey);
  } else if (config.jwksUrl) {
    // Fetch keys from JWKS endpoint
    let cache: JwksCache | null = null;

    getPublicKey = async (kid?: string) => {
      // Check cache
      if (cache && Date.now() - cache.fetchedAt < JWKS_CACHE_TTL) {
        if (kid && cache.keys.has(kid)) {
          return cache.keys.get(kid)!;
        }
        // If no kid specified, return first key
        if (!kid && cache.keys.size > 0) {
          return cache.keys.values().next().value!;
        }
      }

      // Fetch JWKS
      const response = await fetch(config.jwksUrl!);
      if (!response.ok) {
        throw new Error(`Failed to fetch JWKS: ${response.status}`);
      }
      const jwks = await response.json() as JwksResponse;

      // Parse keys
      const keys = new Map<string, crypto.KeyObject>();
      for (const key of jwks.keys) {
        if (key.kty === 'RSA' && key.alg === 'RS256') {
          const publicKey = crypto.createPublicKey({
            key: {
              kty: key.kty,
              n: key.n,
              e: key.e,
            },
            format: 'jwk',
          });
          keys.set(key.kid, publicKey);
        }
      }

      cache = { keys, fetchedAt: Date.now() };

      if (kid && keys.has(kid)) {
        return keys.get(kid)!;
      }
      if (!kid && keys.size > 0) {
        return keys.values().next().value!;
      }
      throw new Error(`Key not found: ${kid ?? 'no keys available'}`);
    };
  } else {
    throw new Error('AuthConfig must specify publicKeyPath, jwksUrl, or _internalKeys');
  }

  return async (c, next) => {
    const authHeader = c.req.header('authorization');
    if (!authHeader?.startsWith('Bearer ')) {
      return new Response('Unauthorized: Missing Bearer token', { status: 401 });
    }

    const token = authHeader.slice(7);
    try {
      // Extract kid from token header
      const headerB64 = token.split('.')[0];
      const header = JSON.parse(Buffer.from(headerB64, 'base64url').toString()) as { kid?: string };

      const publicKey = await getPublicKey(header.kid);
      const payload = verifyJwt(token, publicKey, config.issuer, config.audience);

      // Set identity on context for handlers
      const identity: Identity = {
        sub: payload.sub ?? 'unknown',
        email: payload.email,
        roles: payload.roles ?? [],
      };
      c.set('identity', identity);

      await next();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Invalid token';
      return new Response(`Unauthorized: ${message}`, { status: 401 });
    }
  };
}

/**
 * Verify JWT token and return payload.
 *
 * @param token - Raw JWT string
 * @param publicKey - RSA public key for signature verification
 * @param expectedIssuer - Expected iss claim
 * @param expectedAudience - Expected aud claim
 * @returns Decoded JWT payload
 * @throws Error if verification fails
 */
function verifyJwt(
  token: string,
  publicKey: crypto.KeyObject,
  expectedIssuer: string,
  expectedAudience: string
): JwtPayload {
  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Malformed JWT: expected 3 parts');
  }

  const [headerB64, payloadB64, signatureB64] = parts;

  // Decode header and verify algorithm
  const header = JSON.parse(Buffer.from(headerB64, 'base64url').toString()) as { alg?: string };
  if (header.alg !== 'RS256') {
    throw new Error(`Unsupported algorithm: ${header.alg}`);
  }

  // Verify signature
  const verify = crypto.createVerify('RSA-SHA256');
  verify.update(`${headerB64}.${payloadB64}`);
  const signature = Buffer.from(signatureB64, 'base64url');
  if (!verify.verify(publicKey, signature)) {
    throw new Error('Invalid signature');
  }

  // Decode payload
  const payload = JSON.parse(Buffer.from(payloadB64, 'base64url').toString()) as JwtPayload;

  // Verify time-based claims
  const now = Math.floor(Date.now() / 1000);
  if (payload.exp !== undefined && payload.exp < now) {
    throw new Error('Token expired');
  }
  if (payload.nbf !== undefined && payload.nbf > now) {
    throw new Error('Token not yet valid');
  }

  // Verify issuer
  if (payload.iss !== expectedIssuer) {
    throw new Error(`Invalid issuer: expected ${expectedIssuer}, got ${payload.iss}`);
  }

  // Verify audience
  if (payload.aud !== expectedAudience) {
    throw new Error(`Invalid audience: expected ${expectedAudience}, got ${payload.aud}`);
  }

  return payload;
}
