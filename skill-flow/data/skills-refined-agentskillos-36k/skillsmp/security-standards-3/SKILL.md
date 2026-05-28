---
name: security-standards
description: Security implementation patterns, authentication, authorization, input validation, and security headers for the PMS application. Use for security-related development and audits.
allowed-tools: Read, Grep, Glob
---

# Security Standards for PMS

## Authentication

### JWT Implementation
```typescript
// config/jwt.config.ts
export const jwtConfig = {
  accessToken: {
    secret: process.env.JWT_ACCESS_SECRET!,
    expiresIn: '15m',
  },
  refreshToken: {
    secret: process.env.JWT_REFRESH_SECRET!,
    expiresIn: '7d',
  },
};

// services/auth.service.ts
import jwt from 'jsonwebtoken';
import { jwtConfig } from '../config/jwt.config';

export const generateTokenPair = (userId: string) => {
  const accessToken = jwt.sign(
    { sub: userId, type: 'access' },
    jwtConfig.accessToken.secret,
    { expiresIn: jwtConfig.accessToken.expiresIn }
  );

  const refreshToken = jwt.sign(
    { sub: userId, type: 'refresh' },
    jwtConfig.refreshToken.secret,
    { expiresIn: jwtConfig.refreshToken.expiresIn }
  );

  return { accessToken, refreshToken };
};
```

### Password Hashing
```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

export const hashPassword = async (password: string): Promise<string> => {
  return bcrypt.hash(password, SALT_ROUNDS);
};

export const verifyPassword = async (
  password: string,
  hash: string
): Promise<boolean> => {
  return bcrypt.compare(password, hash);
};
```

## Authorization

### RBAC Implementation
```typescript
// types/permissions.ts
export enum Permission {
  // Project permissions
  PROJECT_CREATE = 'project:create',
  PROJECT_READ = 'project:read',
  PROJECT_UPDATE = 'project:update',
  PROJECT_DELETE = 'project:delete',
  PROJECT_MANAGE_MEMBERS = 'project:manage_members',

  // Task permissions
  TASK_CREATE = 'task:create',
  TASK_READ = 'task:read',
  TASK_UPDATE = 'task:update',
  TASK_DELETE = 'task:delete',
  TASK_ASSIGN = 'task:assign',
}

export const RolePermissions: Record<string, Permission[]> = {
  super_admin: Object.values(Permission),
  org_admin: [
    Permission.PROJECT_CREATE,
    Permission.PROJECT_READ,
    Permission.PROJECT_UPDATE,
    Permission.PROJECT_MANAGE_MEMBERS,
  ],
  project_manager: [
    Permission.PROJECT_READ,
    Permission.PROJECT_UPDATE,
    Permission.TASK_CREATE,
    Permission.TASK_READ,
    Permission.TASK_UPDATE,
    Permission.TASK_DELETE,
    Permission.TASK_ASSIGN,
  ],
  member: [
    Permission.PROJECT_READ,
    Permission.TASK_CREATE,
    Permission.TASK_READ,
    Permission.TASK_UPDATE,
  ],
  viewer: [
    Permission.PROJECT_READ,
    Permission.TASK_READ,
  ],
};

// middleware/authorize.ts
export const authorize = (...requiredPermissions: Permission[]) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const userPermissions = RolePermissions[req.user!.role] || [];

    const hasPermission = requiredPermissions.every(
      perm => userPermissions.includes(perm)
    );

    if (!hasPermission) {
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Insufficient permissions' },
      });
    }

    next();
  };
};
```

## Input Validation

### Validation Schemas
```typescript
// validators/project.validators.ts
import Joi from 'joi';

export const projectSchemas = {
  create: Joi.object({
    name: Joi.string()
      .required()
      .min(3)
      .max(100)
      .trim()
      .pattern(/^[a-zA-Z0-9\s\-_]+$/)
      .messages({
        'string.pattern.base': 'Name can only contain letters, numbers, spaces, hyphens, and underscores',
      }),
    key: Joi.string()
      .required()
      .min(2)
      .max(10)
      .uppercase()
      .pattern(/^[A-Z]+$/)
      .messages({
        'string.pattern.base': 'Key must contain only uppercase letters',
      }),
    description: Joi.string().max(2000).trim().allow(''),
    visibility: Joi.string().valid('private', 'team', 'public'),
  }),

  update: Joi.object({
    name: Joi.string().min(3).max(100).trim(),
    description: Joi.string().max(2000).trim().allow(''),
    status: Joi.string().valid('active', 'on_hold', 'completed', 'archived'),
    visibility: Joi.string().valid('private', 'team', 'public'),
  }).min(1),
};
```

### XSS Prevention
```typescript
// utils/sanitize.ts
import DOMPurify from 'isomorphic-dompurify';

export const sanitizeHtml = (dirty: string): string => {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: ['href', 'target'],
  });
};

export const sanitizeInput = (input: string): string => {
  return input
    .replace(/[<>]/g, '') // Remove angle brackets
    .trim();
};
```

## Security Headers

```typescript
// middleware/security.ts
import helmet from 'helmet';

export const securityHeaders = helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'", process.env.API_URL!],
      fontSrc: ["'self'", 'https://fonts.gstatic.com'],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: true,
  crossOriginResourcePolicy: { policy: 'same-site' },
  dnsPrefetchControl: { allow: false },
  frameguard: { action: 'deny' },
  hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
  ieNoOpen: true,
  noSniff: true,
  originAgentCluster: true,
  permittedCrossDomainPolicies: { permittedPolicies: 'none' },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
  xssFilter: true,
});
```

## Rate Limiting

```typescript
// middleware/rate-limit.ts
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { redisClient } from '../config/redis';

// General API rate limit
export const apiLimiter = rateLimit({
  store: new RedisStore({
    sendCommand: (...args) => redisClient.sendCommand(args),
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  message: {
    success: false,
    error: { code: 'RATE_LIMIT', message: 'Too many requests' },
  },
  standardHeaders: true,
  legacyHeaders: false,
});

// Strict limit for auth endpoints
export const authLimiter = rateLimit({
  store: new RedisStore({
    sendCommand: (...args) => redisClient.sendCommand(args),
  }),
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5,
  message: {
    success: false,
    error: { code: 'AUTH_RATE_LIMIT', message: 'Too many login attempts' },
  },
});
```
