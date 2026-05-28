---
name: security-review
description: Security audit guidelines covering OWASP Top 10 vulnerabilities, secure coding practices, authentication patterns, and code review checklists
version: 1.0.0
priority: 25
tags:
  - security
  - audit
  - owasp
  - review
  - builtin
triggers:
  - type: keyword
    pattern: security
  - type: keyword
    pattern: audit
  - type: keyword
    pattern: vulnerability
  - type: keyword
    pattern: owasp
  - type: glob
    pattern: "**/auth/**"
  - type: glob
    pattern: "**/security/**"
globs:
  - "**/auth/**/*.ts"
  - "**/security/**/*.ts"
  - "**/middleware/**/*.ts"
---

# Security Review

Comprehensive security guidelines for identifying and preventing vulnerabilities.

## Rules

- **Input Validation**: Validate and sanitize ALL user input at system boundaries
- **Output Encoding**: Encode output appropriate to context (HTML, URL, JS, SQL)
- **Authentication**: Use established libraries; never roll your own crypto
- **Authorization**: Check permissions on every protected operation
- **Secrets Management**: Never hardcode secrets; use environment variables or vaults
- **Least Privilege**: Grant minimum permissions required for functionality
- **Defense in Depth**: Multiple security layers; don't rely on single control
- **Fail Secure**: On error, deny access rather than grant it
- **Audit Logging**: Log security events with sufficient detail for investigation

## Patterns

### Input Validation

```typescript
import { z } from "zod";
import DOMPurify from "isomorphic-dompurify";

// Schema validation at API boundary
const userInputSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).regex(/^[\w\s-]+$/),
  bio: z.string().max(1000).optional(),
  age: z.number().int().min(13).max(150).optional(),
});

// Sanitize HTML content
function sanitizeHtml(dirty: string): string {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "p"],
    ALLOWED_ATTR: ["href"],
  });
}

// Path traversal prevention
function safePath(basePath: string, userPath: string): string {
  const resolved = path.resolve(basePath, userPath);
  if (!resolved.startsWith(path.resolve(basePath))) {
    throw new Error("Path traversal attempt detected");
  }
  return resolved;
}

// SQL parameterization (never string concat)
const user = await db.query(
  "SELECT * FROM users WHERE id = $1 AND status = $2",
  [userId, "active"]
);
```markdown

### Authentication Patterns

```typescript
import { hash, verify } from "@node-rs/argon2";
import { SignJWT, jwtVerify } from "jose";

// Password hashing with Argon2id
async function hashPassword(password: string): Promise<string> {
  return hash(password, {
    memoryCost: 65536,  // 64 MB
    timeCost: 3,        // 3 iterations
    parallelism: 4,
  });
}

async function verifyPassword(hash: string, password: string): Promise<boolean> {
  try {
    return await verify(hash, password);
  } catch {
    return false;
  }
}

// JWT with proper configuration
const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET);

async function createToken(payload: JWTPayload): Promise<string> {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256", typ: "JWT" })
    .setIssuedAt()
    .setExpirationTime("1h")
    .setNotBefore("0s")
    .setJti(crypto.randomUUID())
    .sign(JWT_SECRET);
}

async function verifyToken(token: string): Promise<JWTPayload> {
  const { payload } = await jwtVerify(token, JWT_SECRET, {
    algorithms: ["HS256"],
    clockTolerance: 30, // seconds
  });
  return payload as JWTPayload;
}

// Secure session configuration
const sessionConfig = {
  name: "__Host-session",  // Secure prefix
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    secure: true,  // HTTPS only
    sameSite: "strict" as const,
    maxAge: 3600000,  // 1 hour
    path: "/",
  },
};
```markdown

### Authorization Middleware

```typescript
import type { Request, Response, NextFunction } from "express";

interface Permission {
  resource: string;
  action: "read" | "write" | "delete" | "admin";
}

// Role-based access control
const ROLE_PERMISSIONS: Record<string, Permission[]> = {
  user: [
    { resource: "profile", action: "read" },
    { resource: "profile", action: "write" },
  ],
  admin: [
    { resource: "*", action: "admin" },
  ],
};

function hasPermission(
  userRole: string,
  resource: string,
  action: Permission["action"]
): boolean {
  const permissions = ROLE_PERMISSIONS[userRole] ?? [];
  return permissions.some(
    (p) =>
      (p.resource === resource || p.resource === "*") &&
      (p.action === action || p.action === "admin")
  );
}

// Authorization middleware
function authorize(resource: string, action: Permission["action"]) {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;

    if (!user) {
      return res.status(401).json({
        error: { code: "UNAUTHENTICATED", message: "Authentication required" },
      });
    }

    if (!hasPermission(user.role, resource, action)) {
      // Log authorization failure
      logger.warn("Authorization failed", {
        userId: user.id,
        resource,
        action,
        ip: req.ip,
      });

      return res.status(403).json({
        error: { code: "FORBIDDEN", message: "Insufficient permissions" },
      });
    }

    next();
  };
}

// Resource ownership check
async function authorizeOwnership(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const resourceId = req.params.id;
  const resource = await db.findById(resourceId);

  if (!resource) {
    return res.status(404).json({
      error: { code: "NOT_FOUND", message: "Resource not found" },
    });
  }

  // Admin can access any resource
  if (req.user?.role === "admin") {
    return next();
  }

  // Owner check
  if (resource.ownerId !== req.user?.id) {
    return res.status(403).json({
      error: { code: "FORBIDDEN", message: "Access denied" },
    });
  }

  next();
}
```markdown

### Security Headers

```typescript
import helmet from "helmet";

// Comprehensive security headers
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", "data:", "https:"],
        connectSrc: ["'self'"],
        fontSrc: ["'self'"],
        objectSrc: ["'none'"],
        mediaSrc: ["'self'"],
        frameSrc: ["'none'"],
        baseUri: ["'self'"],
        formAction: ["'self'"],
        frameAncestors: ["'none'"],
        upgradeInsecureRequests: [],
      },
    },
    crossOriginEmbedderPolicy: true,
    crossOriginOpenerPolicy: { policy: "same-origin" },
    crossOriginResourcePolicy: { policy: "same-origin" },
    dnsPrefetchControl: { allow: false },
    hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
    noSniff: true,
    originAgentCluster: true,
    permittedCrossDomainPolicies: { permittedPolicies: "none" },
    referrerPolicy: { policy: "strict-origin-when-cross-origin" },
    xssFilter: true,
  })
);

// CORS with specific origins
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(",") ?? [],
  credentials: true,
  methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
  maxAge: 86400,
}));
```markdown

### Secrets Management

```typescript
// Environment-based configuration
const config = {
  database: {
    host: process.env.DB_HOST ?? "localhost",
    password: process.env.DB_PASSWORD,  // Never default secrets
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    issuer: process.env.JWT_ISSUER ?? "app",
  },
  encryption: {
    key: process.env.ENCRYPTION_KEY,
  },
};

// Validate required secrets at startup
function validateSecrets(): void {
  const required = ["DB_PASSWORD", "JWT_SECRET", "ENCRYPTION_KEY"];
  const missing = required.filter((key) => !process.env[key]);

  if (missing.length > 0) {
    throw new Error(`Missing required secrets: ${missing.join(", ")}`);
  }
}

// Secret rotation support
interface SecretManager {
  getSecret(name: string): Promise<string>;
  rotateSecret(name: string): Promise<void>;
}

// Never log secrets
function redactSecrets(obj: unknown): unknown {
  const sensitiveKeys = /password|secret|token|key|auth|credential/i;

  if (typeof obj !== "object" || obj === null) {
    return obj;
  }

  return Object.fromEntries(
    Object.entries(obj).map(([key, value]) => [
      key,
      sensitiveKeys.test(key) ? "[REDACTED]" : redactSecrets(value),
    ])
  );
}
```markdown

## Anti-Patterns

```typescript
// ❌ SQL Injection
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// ✅ Parameterized queries
const query = "SELECT * FROM users WHERE id = $1";
await db.query(query, [userId]);

// ❌ Hardcoded secrets
const API_KEY = "sk_live_abc123";

// ✅ Environment variables
const API_KEY = process.env.API_KEY;

// ❌ Weak password hashing
const hash = crypto.createHash("md5").update(password).digest("hex");

// ✅ Strong password hashing (Argon2, bcrypt)
const hash = await argon2.hash(password);

// ❌ JWT without expiration
const token = jwt.sign({ userId }, secret);

// ✅ JWT with expiration and audience
const token = jwt.sign({ userId }, secret, { expiresIn: "1h", audience: "api" });

// ❌ Trusting user input for paths
const file = fs.readFileSync(`/uploads/${req.params.filename}`);

// ✅ Validate and sanitize paths
const safeName = path.basename(req.params.filename);
const filePath = path.join(UPLOADS_DIR, safeName);

// ❌ Exposing stack traces
res.status(500).json({ error: error.stack });

// ✅ Generic error to client, detailed logging
logger.error("Operation failed", { error, requestId: req.id });
res.status(500).json({ error: { code: "INTERNAL_ERROR", requestId: req.id } });

// ❌ Using eval or Function constructor
eval(userInput);
new Function(userCode)();

// ✅ Never execute user-provided code
throw new Error("Code execution not allowed");
```markdown

## Examples

### Security Review Checklist

```markdown
## Input Handling
- [ ] All user input validated against strict schemas
- [ ] File uploads restricted by type, size, and scanned for malware
- [ ] URLs validated against allowlist (prevent SSRF)
- [ ] HTML content sanitized before rendering

## Authentication
- [ ] Passwords hashed with Argon2id or bcrypt
- [ ] Multi-factor authentication available
- [ ] Account lockout after failed attempts
- [ ] Secure password reset flow

## Session Management
- [ ] Session tokens are cryptographically random
- [ ] Sessions expire after inactivity
- [ ] Sessions invalidated on logout
- [ ] Cookies use Secure, HttpOnly, SameSite flags

## Authorization
- [ ] Every endpoint checks permissions
- [ ] Resource ownership verified
- [ ] Principle of least privilege applied
- [ ] Admin functions protected

## Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] TLS 1.3 for data in transit
- [ ] PII minimized and retention policies defined
- [ ] Secrets stored in vault, not code

## Error Handling
- [ ] Generic errors returned to clients
- [ ] Detailed errors logged server-side
- [ ] Stack traces never exposed
- [ ] Failed auth attempts logged

## Headers & CORS
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] CORS restricted to known origins
- [ ] X-Frame-Options prevents clickjacking

## Dependencies
- [ ] Dependencies audited (`npm audit`)
- [ ] No known vulnerabilities
- [ ] Automated security updates enabled
```markdown

### Audit Logging

```typescript
interface AuditEvent {
  timestamp: Date;
  eventType: string;
  userId?: string;
  resourceType: string;
  resourceId: string;
  action: string;
  outcome: "success" | "failure";
  ipAddress: string;
  userAgent: string;
  details?: Record<string, unknown>;
}

class AuditLogger {
  async log(event: AuditEvent): Promise<void> {
    // Immutable audit log
    await this.store.append({
      ...event,
      id: crypto.randomUUID(),
      timestamp: new Date(),
    });
  }

  // Common events
  async logAuth(type: "login" | "logout" | "failed", userId: string, req: Request) {
    await this.log({
      timestamp: new Date(),
      eventType: `auth.${type}`,
      userId,
      resourceType: "session",
      resourceId: req.sessionID ?? "",
      action: type,
      outcome: type === "failed" ? "failure" : "success",
      ipAddress: req.ip ?? "",
      userAgent: req.get("user-agent") ?? "",
    });
  }

  async logDataAccess(
    userId: string,
    resourceType: string,
    resourceId: string,
    action: string,
    req: Request
  ) {
    await this.log({
      timestamp: new Date(),
      eventType: "data.access",
      userId,
      resourceType,
      resourceId,
      action,
      outcome: "success",
      ipAddress: req.ip ?? "",
      userAgent: req.get("user-agent") ?? "",
    });
  }
}
```

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
