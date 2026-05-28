/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * RSA keypair generation and JWT signing for OIDC provider.
 */

import * as crypto from 'node:crypto';

/**
 * RSA keypair for JWT signing.
 */
export interface KeyPair {
  privateKey: crypto.KeyObject;
  publicKey: crypto.KeyObject;
  /** Key ID for JWKS */
  kid: string;
}

/**
 * JWT payload claims.
 */
export interface JwtPayload {
  /** Subject - user identifier */
  sub: string;
  /** Issuer */
  iss: string;
  /** Audience */
  aud: string;
  /** Expiration time (Unix timestamp) */
  exp: number;
  /** Issued at time (Unix timestamp) */
  iat: number;
  /** Not before time (Unix timestamp) */
  nbf: number;
  /** Token type (access or refresh) */
  token_type?: 'access' | 'refresh';
}

/**
 * Generate an RSA keypair for JWT signing.
 * Keys are generated in-memory on server startup.
 */
export function generateKeyPair(): KeyPair {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 2048,
  });

  // Generate a random key ID
  const kid = crypto.randomBytes(8).toString('hex');

  return { privateKey, publicKey, kid };
}

/**
 * Sign a JWT payload with the private key.
 */
export function signJwt(payload: JwtPayload, keys: KeyPair): string {
  const header = {
    alg: 'RS256',
    typ: 'JWT',
    kid: keys.kid,
  };

  const headerB64 = Buffer.from(JSON.stringify(header)).toString('base64url');
  const payloadB64 = Buffer.from(JSON.stringify(payload)).toString('base64url');

  const sign = crypto.createSign('RSA-SHA256');
  sign.update(`${headerB64}.${payloadB64}`);
  const signature = sign.sign(keys.privateKey);
  const signatureB64 = signature.toString('base64url');

  return `${headerB64}.${payloadB64}.${signatureB64}`;
}

/**
 * Verify a JWT and return the payload.
 * @throws Error if verification fails
 */
export function verifyJwt(token: string, keys: KeyPair): JwtPayload {
  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Malformed JWT: expected 3 parts');
  }

  const [headerB64, payloadB64, signatureB64] = parts;

  // Verify signature
  const verify = crypto.createVerify('RSA-SHA256');
  verify.update(`${headerB64}.${payloadB64}`);
  const signature = Buffer.from(signatureB64, 'base64url');
  if (!verify.verify(keys.publicKey, signature)) {
    throw new Error('Invalid JWT signature');
  }

  // Decode and validate payload
  const payload = JSON.parse(Buffer.from(payloadB64, 'base64url').toString()) as JwtPayload;

  const now = Math.floor(Date.now() / 1000);
  if (payload.exp !== undefined && payload.exp < now) {
    throw new Error('Token expired');
  }
  if (payload.nbf !== undefined && payload.nbf > now) {
    throw new Error('Token not yet valid');
  }

  return payload;
}

/**
 * Export public key in JWK format for JWKS endpoint.
 */
export function publicKeyToJwk(keys: KeyPair): object {
  const publicKeyJwk = keys.publicKey.export({ format: 'jwk' });
  return {
    ...publicKeyJwk,
    kid: keys.kid,
    use: 'sig',
    alg: 'RS256',
  };
}
