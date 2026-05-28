---
name: authentication
description: Expert authentification securisee - JWT, OAuth2, sessions, MFA
---

# Authentification Securisee

Tu es expert en **mecanismes d'authentification** securises.

## Mission

> Verifier l'identite des utilisateurs de maniere fiable et securisee.

## Methodes d'Authentification

| Methode | Use Case | Securite |
|---------|----------|----------|
| Session + Cookie | Web apps traditionnelles | Haute |
| JWT | APIs, SPAs, mobile | Haute si bien impl |
| OAuth 2.0 / OIDC | SSO, third-party auth | Haute |
| API Keys | Machine-to-machine | Moyenne |
| MFA | Toute app sensible | Tres haute |

## Implementation JWT

### Generation Securisee

```typescript
import jwt from 'jsonwebtoken';

interface TokenPayload {
  userId: string;
  email: string;
  role: string;
}

const JWT_SECRET = process.env.JWT_SECRET!; // Min 256 bits
const ACCESS_TOKEN_EXPIRY = '15m';
const REFRESH_TOKEN_EXPIRY = '7d';

function generateAccessToken(payload: TokenPayload): string {
  return jwt.sign(payload, JWT_SECRET, {
    expiresIn: ACCESS_TOKEN_EXPIRY,
    algorithm: 'HS256',
    issuer: 'myapp',
    audience: 'myapp-users',
  });
}

function generateRefreshToken(userId: string): string {
  return jwt.sign(
    { userId, type: 'refresh' },
    JWT_SECRET,
    { expiresIn: REFRESH_TOKEN_EXPIRY }
  );
}
```

### Verification

```typescript
function verifyAccessToken(token: string): TokenPayload {
  try {
    const decoded = jwt.verify(token, JWT_SECRET, {
      algorithms: ['HS256'],
      issuer: 'myapp',
      audience: 'myapp-users',
    }) as TokenPayload;

    return decoded;
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      throw new AuthError('Token expired');
    }
    if (error instanceof jwt.JsonWebTokenError) {
      throw new AuthError('Invalid token');
    }
    throw error;
  }
}

// Middleware Express
function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing authorization header' });
  }

  const token = authHeader.slice(7);

  try {
    req.user = verifyAccessToken(token);
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
}
```

## Implementation Session

```typescript
import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

const redisClient = createClient({ url: process.env.REDIS_URL });

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET!,
  name: 'sid', // Pas 'connect.sid' (fingerprinting)
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production', // HTTPS only
    httpOnly: true, // Pas accessible en JS
    sameSite: 'strict', // CSRF protection
    maxAge: 24 * 60 * 60 * 1000, // 24h
    domain: '.example.com', // Specifique au domaine
  },
}));
```

## Hachage de Passwords

### Avec bcrypt

```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12; // Ajuster selon CPU

async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// Login
async function login(email: string, password: string) {
  const user = await db.user.findUnique({ where: { email } });

  if (!user) {
    // Timing attack prevention: toujours hasher
    await bcrypt.hash(password, SALT_ROUNDS);
    throw new AuthError('Invalid credentials');
  }

  const valid = await verifyPassword(password, user.passwordHash);

  if (!valid) {
    throw new AuthError('Invalid credentials');
  }

  return user;
}
```

### Avec Argon2 (Recommande)

```typescript
import argon2 from 'argon2';

async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, {
    type: argon2.argon2id, // Resistant GPU + side-channel
    memoryCost: 65536, // 64MB
    timeCost: 3,
    parallelism: 4,
  });
}

async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return argon2.verify(hash, password);
}
```

## OAuth 2.0 / OIDC

### Passport.js + Google

```typescript
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';

passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  callbackURL: '/auth/google/callback',
}, async (accessToken, refreshToken, profile, done) => {
  try {
    let user = await db.user.findUnique({
      where: { googleId: profile.id }
    });

    if (!user) {
      user = await db.user.create({
        data: {
          googleId: profile.id,
          email: profile.emails?.[0]?.value,
          name: profile.displayName,
        }
      });
    }

    done(null, user);
  } catch (error) {
    done(error);
  }
}));

// Routes
app.get('/auth/google', passport.authenticate('google', {
  scope: ['profile', 'email']
}));

app.get('/auth/google/callback',
  passport.authenticate('google', { failureRedirect: '/login' }),
  (req, res) => {
    res.redirect('/dashboard');
  }
);
```

## MFA / 2FA

### TOTP (Google Authenticator)

```typescript
import speakeasy from 'speakeasy';
import QRCode from 'qrcode';

// Setup MFA
async function setupMfa(userId: string) {
  const secret = speakeasy.generateSecret({
    name: `MyApp (${user.email})`,
    issuer: 'MyApp',
  });

  // Stocker temporairement (pas encore verifie)
  await db.user.update({
    where: { id: userId },
    data: { mfaSecret: secret.base32, mfaEnabled: false }
  });

  // Generer QR code
  const qrCodeUrl = await QRCode.toDataURL(secret.otpauth_url!);

  return { qrCodeUrl, secret: secret.base32 };
}

// Verification MFA
function verifyMfaToken(secret: string, token: string): boolean {
  return speakeasy.totp.verify({
    secret,
    encoding: 'base32',
    token,
    window: 1, // Tolerance de 30s
  });
}
```

## Bonnes Pratiques

### Password Policy

```typescript
const PasswordSchema = z.string()
  .min(12, 'Minimum 12 characters')
  .max(128, 'Maximum 128 characters')
  .regex(/[A-Z]/, 'Must contain uppercase')
  .regex(/[a-z]/, 'Must contain lowercase')
  .regex(/[0-9]/, 'Must contain number')
  .refine(
    (pwd) => !commonPasswords.includes(pwd.toLowerCase()),
    'Password is too common'
  );
```

### Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 min
  max: 5, // 5 tentatives
  message: 'Too many login attempts, try again later',
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => req.ip + req.body.email,
});

app.post('/login', loginLimiter, loginHandler);
```

### Account Lockout

```typescript
const MAX_ATTEMPTS = 5;
const LOCKOUT_DURATION = 15 * 60 * 1000; // 15 min

async function handleFailedLogin(email: string) {
  const key = `login:failed:${email}`;
  const attempts = await redis.incr(key);

  if (attempts === 1) {
    await redis.expire(key, LOCKOUT_DURATION / 1000);
  }

  if (attempts >= MAX_ATTEMPTS) {
    throw new AuthError('Account locked. Try again later.');
  }
}

async function handleSuccessfulLogin(email: string) {
  await redis.del(`login:failed:${email}`);
}
```

## Anti-Patterns

| Pattern | Risque | Solution |
|---------|--------|----------|
| MD5/SHA1 pour passwords | Rainbow tables | bcrypt/argon2 |
| JWT dans localStorage | XSS vol de token | httpOnly cookie |
| JWT sans expiration | Token eternel | Courte expiration + refresh |
| Password en clair dans logs | Fuite | Sanitiser les logs |
| Email comme seul identifiant | Enumeration | Rate limit + message generique |

## Voir Aussi

- `secure-coding/authorization` pour permissions
- `secure-coding/cryptography` pour crypto
- `penetration/owasp-top10` A07 Auth Failures
