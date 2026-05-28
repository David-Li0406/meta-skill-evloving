---
name: validation
description: Expert validation et sanitization des entrees - Protection contre injections
---

# Validation des Entrees

Tu es expert en **validation et sanitization** des donnees utilisateur.

## Mission

> Toute entree externe est hostile jusqu'a preuve du contraire.

## Principes

1. **Whitelist > Blacklist** : Definir ce qui est autorise, pas ce qui est interdit
2. **Valider puis sanitizer** : Schema d'abord, nettoyage ensuite
3. **Cote serveur obligatoire** : La validation client est cosmetic
4. **Type strict** : Pas de coercion implicite

## Implementation Node.js/TypeScript

### Zod (Recommande)

```typescript
import { z } from 'zod';

// Schema de validation
const UserSchema = z.object({
  email: z.string().email(),
  password: z.string()
    .min(12, 'Password must be at least 12 characters')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/[0-9]/, 'Must contain number')
    .regex(/[^A-Za-z0-9]/, 'Must contain special char'),
  age: z.number().int().min(18).max(120),
  role: z.enum(['user', 'admin', 'moderator']),
});

// Utilisation
function createUser(data: unknown) {
  const result = UserSchema.safeParse(data);

  if (!result.success) {
    throw new ValidationError(result.error.flatten());
  }

  // result.data est type-safe
  return saveUser(result.data);
}
```

### Express Middleware

```typescript
import { z } from 'zod';
import { Request, Response, NextFunction } from 'express';

function validate(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse({
      body: req.body,
      query: req.query,
      params: req.params,
    });

    if (!result.success) {
      return res.status(400).json({
        error: 'Validation failed',
        details: result.error.flatten(),
      });
    }

    req.validated = result.data;
    next();
  };
}

// Usage
const CreatePostSchema = z.object({
  body: z.object({
    title: z.string().min(1).max(200),
    content: z.string().min(1).max(10000),
    tags: z.array(z.string()).max(10).optional(),
  }),
  params: z.object({
    userId: z.string().uuid(),
  }),
});

app.post('/users/:userId/posts',
  validate(CreatePostSchema),
  createPostHandler
);
```

## Sanitization

### HTML (Anti-XSS)

```typescript
import DOMPurify from 'isomorphic-dompurify';

// Sanitize HTML input
function sanitizeHtml(dirty: string): string {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href', 'title'],
    ALLOW_DATA_ATTR: false,
  });
}

// Pour texte pur (pas de HTML)
function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;',
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}
```

### SQL (Parametrage)

```typescript
// JAMAIS de concatenation
// BAD
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD - Requetes parametrees
const result = await db.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);

// Avec ORM (Prisma)
const user = await prisma.user.findUnique({
  where: { id: userId } // Automatiquement parametre
});
```

### Path Traversal

```typescript
import path from 'path';

function safeFilePath(userInput: string, baseDir: string): string {
  // Normaliser et resoudre le chemin
  const resolved = path.resolve(baseDir, userInput);

  // Verifier qu'on reste dans le dossier autorise
  if (!resolved.startsWith(path.resolve(baseDir))) {
    throw new SecurityError('Path traversal attempt detected');
  }

  return resolved;
}

// Usage
const file = safeFilePath(req.params.filename, '/app/uploads');
```

## Patterns de Validation Communs

### Email

```typescript
const EmailSchema = z.string()
  .email()
  .toLowerCase()
  .max(254); // RFC 5321
```

### Phone

```typescript
const PhoneSchema = z.string()
  .regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number (E.164)');
```

### UUID

```typescript
const UuidSchema = z.string().uuid();
```

### URL

```typescript
const UrlSchema = z.string().url().refine(
  (url) => {
    const parsed = new URL(url);
    return ['http:', 'https:'].includes(parsed.protocol);
  },
  'Only HTTP(S) URLs allowed'
);
```

### Fichiers Upload

```typescript
const FileSchema = z.object({
  mimetype: z.enum([
    'image/jpeg',
    'image/png',
    'image/gif',
    'application/pdf'
  ]),
  size: z.number().max(5 * 1024 * 1024), // 5MB max
  originalname: z.string()
    .regex(/^[\w\-. ]+$/, 'Invalid filename characters')
    .max(255),
});
```

## API Validation Complete

```typescript
// schemas/user.ts
import { z } from 'zod';

export const CreateUserSchema = z.object({
  body: z.object({
    email: z.string().email().toLowerCase(),
    password: z.string().min(12),
    name: z.string().min(1).max(100).trim(),
    bio: z.string().max(500).optional(),
  }),
});

export const UpdateUserSchema = z.object({
  params: z.object({
    id: z.string().uuid(),
  }),
  body: z.object({
    name: z.string().min(1).max(100).trim().optional(),
    bio: z.string().max(500).optional(),
  }),
});

export const GetUsersSchema = z.object({
  query: z.object({
    page: z.coerce.number().int().min(1).default(1),
    limit: z.coerce.number().int().min(1).max(100).default(20),
    sort: z.enum(['createdAt', 'name', 'email']).default('createdAt'),
    order: z.enum(['asc', 'desc']).default('desc'),
  }),
});
```

## Rate Limiting Middleware

### Express avec express-rate-limit

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

// Limiter global - 100 requetes par 15 minutes
export const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false,
  message: {
    error: 'Too many requests',
    retryAfter: 15 * 60,
  },
  store: new RedisStore({
    sendCommand: (...args: string[]) => redis.call(...args),
  }),
});

// Limiter strict pour auth - 5 tentatives par heure
export const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 heure
  max: 5,
  message: {
    error: 'Too many login attempts',
    retryAfter: 60 * 60,
  },
  keyGenerator: (req) => {
    // Combiner IP + email pour eviter le blocage d'IP partagees
    return `${req.ip}-${req.body?.email || 'unknown'}`;
  },
  skip: (req) => {
    // Skip pour les requetes de health check
    return req.path === '/health';
  },
  store: new RedisStore({
    sendCommand: (...args: string[]) => redis.call(...args),
  }),
});

// Limiter API - par cle API
export const apiKeyLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 60, // 60 req/min = 1 req/sec average
  keyGenerator: (req) => {
    return req.headers['x-api-key'] as string || req.ip;
  },
  handler: (req, res) => {
    res.status(429).json({
      error: 'Rate limit exceeded',
      limit: 60,
      window: '1 minute',
      retryAfter: res.getHeader('Retry-After'),
    });
  },
});

// Usage
app.use('/api', globalLimiter);
app.use('/auth/login', authLimiter);
app.use('/api/v1', apiKeyLimiter);
```

### Sliding Window avec Redis (Custom)

```typescript
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

interface RateLimitConfig {
  windowMs: number;
  max: number;
  keyPrefix?: string;
}

export function slidingWindowRateLimit(config: RateLimitConfig) {
  const { windowMs, max, keyPrefix = 'rl' } = config;

  return async (req: Request, res: Response, next: NextFunction) => {
    const key = `${keyPrefix}:${req.ip}`;
    const now = Date.now();
    const windowStart = now - windowMs;

    const pipeline = redis.pipeline();

    // Supprimer les anciennes entrees
    pipeline.zremrangebyscore(key, 0, windowStart);
    // Ajouter la requete actuelle
    pipeline.zadd(key, now.toString(), `${now}-${Math.random()}`);
    // Compter les requetes dans la fenetre
    pipeline.zcard(key);
    // Definir TTL
    pipeline.pexpire(key, windowMs);

    const results = await pipeline.exec();
    const requestCount = results?.[2]?.[1] as number || 0;

    // Headers de rate limit
    res.setHeader('X-RateLimit-Limit', max);
    res.setHeader('X-RateLimit-Remaining', Math.max(0, max - requestCount));
    res.setHeader('X-RateLimit-Reset', Math.ceil((now + windowMs) / 1000));

    if (requestCount > max) {
      res.setHeader('Retry-After', Math.ceil(windowMs / 1000));
      return res.status(429).json({
        error: 'Rate limit exceeded',
        retryAfter: Math.ceil(windowMs / 1000),
      });
    }

    next();
  };
}
```

### Token Bucket Algorithm

```typescript
interface TokenBucketConfig {
  capacity: number;      // Max tokens
  refillRate: number;    // Tokens per second
  keyPrefix?: string;
}

export function tokenBucketRateLimit(config: TokenBucketConfig) {
  const { capacity, refillRate, keyPrefix = 'tb' } = config;

  return async (req: Request, res: Response, next: NextFunction) => {
    const key = `${keyPrefix}:${req.ip}`;
    const now = Date.now();

    // Lua script for atomic token bucket
    const script = `
      local key = KEYS[1]
      local capacity = tonumber(ARGV[1])
      local refillRate = tonumber(ARGV[2])
      local now = tonumber(ARGV[3])
      local requested = tonumber(ARGV[4])

      local bucket = redis.call('HMGET', key, 'tokens', 'lastRefill')
      local tokens = tonumber(bucket[1]) or capacity
      local lastRefill = tonumber(bucket[2]) or now

      -- Refill tokens based on time elapsed
      local elapsed = (now - lastRefill) / 1000
      local refill = elapsed * refillRate
      tokens = math.min(capacity, tokens + refill)

      if tokens >= requested then
        tokens = tokens - requested
        redis.call('HMSET', key, 'tokens', tokens, 'lastRefill', now)
        redis.call('PEXPIRE', key, 3600000) -- 1 hour TTL
        return {1, tokens}
      else
        return {0, tokens}
      end
    `;

    const result = await redis.eval(
      script, 1, key, capacity, refillRate, now, 1
    ) as [number, number];

    const [allowed, remainingTokens] = result;

    res.setHeader('X-RateLimit-Limit', capacity);
    res.setHeader('X-RateLimit-Remaining', Math.floor(remainingTokens));

    if (!allowed) {
      const waitTime = Math.ceil((1 - remainingTokens) / refillRate);
      res.setHeader('Retry-After', waitTime);
      return res.status(429).json({
        error: 'Rate limit exceeded',
        retryAfter: waitTime,
      });
    }

    next();
  };
}

// Usage: 10 tokens capacity, 2 tokens/second refill
app.use('/api/expensive', tokenBucketRateLimit({
  capacity: 10,
  refillRate: 2,
}));
```

### Rate Limiting par Tier (API Plans)

```typescript
interface RateLimitTier {
  name: string;
  requestsPerMinute: number;
  requestsPerDay: number;
}

const TIERS: Record<string, RateLimitTier> = {
  free: { name: 'Free', requestsPerMinute: 10, requestsPerDay: 1000 },
  pro: { name: 'Pro', requestsPerMinute: 60, requestsPerDay: 10000 },
  enterprise: { name: 'Enterprise', requestsPerMinute: 1000, requestsPerDay: 100000 },
};

export function tieredRateLimit() {
  return async (req: Request, res: Response, next: NextFunction) => {
    const apiKey = req.headers['x-api-key'] as string;
    const tier = await getUserTier(apiKey) || 'free';
    const limits = TIERS[tier];

    const minuteKey = `rl:min:${apiKey}`;
    const dayKey = `rl:day:${apiKey}`;

    const pipeline = redis.pipeline();
    pipeline.incr(minuteKey);
    pipeline.expire(minuteKey, 60);
    pipeline.incr(dayKey);
    pipeline.expire(dayKey, 86400);

    const results = await pipeline.exec();
    const minuteCount = results?.[0]?.[1] as number;
    const dayCount = results?.[2]?.[1] as number;

    res.setHeader('X-RateLimit-Tier', limits.name);
    res.setHeader('X-RateLimit-Limit-Minute', limits.requestsPerMinute);
    res.setHeader('X-RateLimit-Remaining-Minute',
      Math.max(0, limits.requestsPerMinute - minuteCount));
    res.setHeader('X-RateLimit-Limit-Day', limits.requestsPerDay);
    res.setHeader('X-RateLimit-Remaining-Day',
      Math.max(0, limits.requestsPerDay - dayCount));

    if (minuteCount > limits.requestsPerMinute) {
      return res.status(429).json({
        error: 'Minute rate limit exceeded',
        tier: limits.name,
        upgrade: tier !== 'enterprise' ? 'Upgrade for higher limits' : undefined,
      });
    }

    if (dayCount > limits.requestsPerDay) {
      return res.status(429).json({
        error: 'Daily rate limit exceeded',
        tier: limits.name,
        upgrade: tier !== 'enterprise' ? 'Upgrade for higher limits' : undefined,
      });
    }

    next();
  };
}
```

### Next.js API Route Rate Limiting

```typescript
// lib/rateLimit.ts
import { NextRequest, NextResponse } from 'next/server';
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'), // 10 requests per 10 seconds
  analytics: true,
});

export async function rateLimitMiddleware(
  request: NextRequest,
  identifier?: string
) {
  const ip = request.ip ?? '127.0.0.1';
  const key = identifier || ip;

  const { success, limit, remaining, reset } = await ratelimit.limit(key);

  if (!success) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      {
        status: 429,
        headers: {
          'X-RateLimit-Limit': limit.toString(),
          'X-RateLimit-Remaining': remaining.toString(),
          'X-RateLimit-Reset': reset.toString(),
          'Retry-After': Math.ceil((reset - Date.now()) / 1000).toString(),
        },
      }
    );
  }

  return null; // Continue
}

// app/api/route.ts
export async function POST(request: NextRequest) {
  const rateLimitResponse = await rateLimitMiddleware(request);
  if (rateLimitResponse) return rateLimitResponse;

  // Handle request...
}
```

## Anti-Patterns a Eviter

| Pattern | Probleme | Solution |
|---------|----------|----------|
| `eval(userInput)` | Code injection | Ne jamais utiliser eval |
| `new Function(userInput)` | Code injection | Idem |
| `${userInput}` dans SQL | SQL injection | Requetes parametrees |
| `innerHTML = userInput` | XSS | textContent ou DOMPurify |
| `fs.readFile(userInput)` | Path traversal | Whitelist + validation |
| No rate limiting | DoS, brute force | Implementer rate limiting |
| IP-only rate limiting | Shared IPs blocked | Combiner IP + user identifier |
| In-memory rate limiting | Perte au restart, pas scalable | Utiliser Redis |

## Voir Aussi

- `secure-coding/authentication` pour auth
- `penetration/web-vulnerabilities` pour tester
- `appsec/sast` pour detection automatique
