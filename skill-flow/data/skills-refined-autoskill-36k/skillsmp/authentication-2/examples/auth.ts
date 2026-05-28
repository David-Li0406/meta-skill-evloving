import express from 'express';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { v4 as uuidv4 } from 'uuid';
import { storage } from './storage';

const router = express.Router();

function generateKeys() {
  // In test environment, generate keys in-memory and do not write to disk.
  // This avoids filesystem IO and potential blocking on some environments (CI/WSL).
  const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 2048,
    publicKeyEncoding: { type: 'spki', format: 'pem' },
    privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
  });
  return { privateKey, publicKey };
}

const { privateKey, publicKey } = generateKeys();

function sha256Hex(input: string) {
  return crypto.createHash('sha256').update(input).digest('hex');
}

function generateRefreshToken(): { token: string; hash: string } {
  const token = uuidv4() + '.' + crypto.randomBytes(32).toString('hex');
  const hash = sha256Hex(token);
  return { token, hash };
}

function generateAccessToken(payload: object) {
  return jwt.sign(payload, privateKey, { algorithm: 'RS256', expiresIn: '15m' });
}

const DEFAULT_REFRESH_TTL_MS = 7 * 24 * 60 * 60 * 1000; // 7 days

function getRefreshTtlMs(): number {
  const raw = process.env.REFRESH_TOKEN_TTL_MS;
  const n = raw ? Number(raw) : NaN;
  if (!Number.isFinite(n) || n <= 0) return DEFAULT_REFRESH_TTL_MS;
  return n;
}

export function verifyAccessToken(req: express.Request, res: express.Response, next: express.NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'missing token' });
  }
  const token = authHeader.slice(7);
  try {
    const payload = jwt.verify(token, publicKey, { algorithms: ['RS256'] });
    (req as any).user = payload;
    return next();
  } catch (err) {
    return res.status(401).json({ error: 'invalid token' });
  }
}

router.post('/register', async (req, res) => {
  const { username: rawUsername, password } = req.body;
  const username = typeof rawUsername === 'string' ? rawUsername.trim() : rawUsername;
  if (!username || !password) return res.status(400).json({ error: 'username and password required' });
  if (storage.getUserByUsername(username)) return res.status(409).json({ error: 'user exists' });
  const passwordHash = await bcrypt.hash(password, 10);
  const user = storage.createUser({ username, passwordHash });
  return res.status(201).json({ id: user.id, username: user.username });
});

router.post('/login', async (req, res) => {
  const { username: rawUsername, password } = req.body;
  const username = typeof rawUsername === 'string' ? rawUsername.trim() : rawUsername;
  if (!username || !password) return res.status(400).json({ error: 'username and password required' });
  const user = storage.getUserByUsername(username);
  if (!user) return res.status(401).json({ error: 'invalid credentials' });
  const ok = await bcrypt.compare(password, user.passwordHash);
  if (!ok) return res.status(401).json({ error: 'invalid credentials' });

  const accessToken = generateAccessToken({ sub: user.id, username: user.username });
  const { token: refreshToken, hash } = generateRefreshToken();
  const now = Date.now();
  storage.setRefreshToken(user.username, {
    hash,
    issuedAtMs: now,
    expiresAtMs: now + getRefreshTtlMs(),
    lastUsedAtMs: now,
    rotationCount: 0,
  });

  return res.json({ accessToken, refreshToken });
});

router.post('/refresh', (req, res) => {
  const { refreshToken } = req.body;
  if (!refreshToken) return res.status(400).json({ error: 'refreshToken required' });
  const hash = sha256Hex(refreshToken);
  const user = storage.findUserByRefreshHash(hash);
  if (!user) return res.status(401).json({ error: 'invalid refresh token' });

  const now = Date.now();
  const refresh = user.refresh;
  if (!refresh || refresh.expiresAtMs <= now) {
    return res.status(401).json({ error: 'refresh token expired' });
  }

  // rotate
  const { token: newRefreshToken, hash: newHash } = generateRefreshToken();
  storage.setRefreshToken(user.username, {
    hash: newHash,
    issuedAtMs: now,
    expiresAtMs: now + getRefreshTtlMs(),
    lastUsedAtMs: now,
    rotationCount: (refresh.rotationCount || 0) + 1,
  });
  const accessToken = generateAccessToken({ sub: user.id, username: user.username });
  return res.json({ accessToken, refreshToken: newRefreshToken });
});

router.post('/logout', (req, res) => {
  const { username: rawUsername } = req.body;
  const username = typeof rawUsername === 'string' ? rawUsername.trim() : rawUsername;
  if (!username) return res.status(400).json({ error: 'username required' });
  storage.clearRefreshToken(username);
  return res.json({ ok: true });
});

export default router;
