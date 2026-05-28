# Node.js Security Best Practices

Security guidelines for Node.js applications.

## Dependency Security

### Audit Dependencies

```bash
# Check for vulnerabilities
npm audit

# Fix automatically where possible
npm audit fix

# Check production dependencies only
npm audit --omit=dev
```

### Lock Files

Always commit lock files (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`) to ensure reproducible builds and prevent supply chain attacks.

```json
// package.json - pin versions for security-critical deps
{
  "dependencies": {
    "express": "4.18.2",
    "helmet": "7.1.0"
  }
}
```

### Dependency Monitoring

- Enable Dependabot or Snyk for automated vulnerability alerts
- Review new dependencies before adding (check npm scores, maintenance, downloads)
- Prefer well-maintained packages with security policies

## Input Validation

### Validate All Input

```javascript
import Joi from 'joi';

const userSchema = Joi.object({
  username: Joi.string().alphanum().min(3).max(30).required(),
  email: Joi.string().email().required(),
  age: Joi.number().integer().min(0).max(150),
});

function validateUser(data) {
  const { error, value } = userSchema.validate(data);
  if (error) {
    throw new ValidationError(error.details[0].message);
  }
  return value;
}
```

### Path Traversal Prevention

```javascript
import path from 'path';

function safeReadFile(userPath) {
  const basePath = '/app/uploads';
  const resolvedPath = path.resolve(basePath, userPath);

  // Ensure resolved path is within base directory
  if (!resolvedPath.startsWith(basePath)) {
    throw new Error('Path traversal attempt detected');
  }

  return fs.readFileSync(resolvedPath);
}
```

### SQL Injection Prevention

```javascript
// NEVER interpolate user input into queries
// BAD
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD: Use parameterized queries
const result = await db.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);

// With ORMs, use built-in escaping
const user = await User.findOne({ where: { id: userId } });
```

## Authentication & Sessions

### Password Handling

```javascript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

async function hashPassword(password) {
  return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password, hash) {
  return bcrypt.compare(password, hash);
}
```

### Session Security

```javascript
import session from 'express-session';

app.use(session({
  secret: process.env.SESSION_SECRET,
  name: 'sessionId',  // Change from default 'connect.sid'
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,      // HTTPS only
    httpOnly: true,    // No JavaScript access
    sameSite: 'strict', // CSRF protection
    maxAge: 3600000,   // 1 hour
  },
}));
```

### JWT Best Practices

```javascript
import jwt from 'jsonwebtoken';

// Use strong secrets (256+ bits)
const SECRET = process.env.JWT_SECRET;

// Sign with expiration
function createToken(payload) {
  return jwt.sign(payload, SECRET, {
    expiresIn: '1h',
    algorithm: 'HS256',
  });
}

// Verify with options
function verifyToken(token) {
  return jwt.verify(token, SECRET, {
    algorithms: ['HS256'],  // Prevent algorithm switching attacks
  });
}
```

## HTTP Security Headers

### Using Helmet

```javascript
import helmet from 'helmet';

app.use(helmet());

// Or configure individually
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
}));
```

### CORS Configuration

```javascript
import cors from 'cors';

// Restrictive CORS
app.use(cors({
  origin: ['https://example.com', 'https://app.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400,
}));
```

## Rate Limiting

```javascript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                   // 100 requests per window
  message: 'Too many requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', limiter);

// Stricter limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,  // 1 hour
  max: 5,                     // 5 attempts
  skipSuccessfulRequests: true,
});

app.use('/api/auth/login', authLimiter);
```

## Error Handling

### Don't Leak Information

```javascript
// BAD: Exposes internal details
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.stack });
});

// GOOD: Generic message in production
app.use((err, req, res, next) => {
  console.error(err);  // Log full error internally

  const message = process.env.NODE_ENV === 'production'
    ? 'Internal server error'
    : err.message;

  res.status(err.status || 500).json({ error: message });
});
```

### Validate Error Origins

```javascript
// Only handle expected error types
if (err instanceof ValidationError) {
  return res.status(400).json({ error: err.message });
}
if (err instanceof AuthenticationError) {
  return res.status(401).json({ error: 'Unauthorized' });
}
// Unknown errors - log and return generic message
console.error('Unexpected error:', err);
res.status(500).json({ error: 'Internal server error' });
```

## Environment Variables

### Never Commit Secrets

```bash
# .gitignore
.env
.env.*
!.env.example
```

```javascript
// .env.example (commit this)
DATABASE_URL=postgres://user:password@localhost:5432/db
JWT_SECRET=your-secret-here
API_KEY=your-api-key

// Validate required env vars at startup
const required = ['DATABASE_URL', 'JWT_SECRET'];
for (const key of required) {
  if (!process.env[key]) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
}
```

## File Uploads

### Secure File Handling

```javascript
import multer from 'multer';
import path from 'path';

const upload = multer({
  storage: multer.diskStorage({
    destination: '/app/uploads',
    filename: (req, file, cb) => {
      // Generate safe filename
      const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
      cb(null, uniqueSuffix + path.extname(file.originalname));
    },
  }),
  limits: {
    fileSize: 5 * 1024 * 1024,  // 5MB limit
  },
  fileFilter: (req, file, cb) => {
    const allowed = ['.jpg', '.jpeg', '.png', '.pdf'];
    const ext = path.extname(file.originalname).toLowerCase();
    if (allowed.includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'));
    }
  },
});
```

## Process Security

### Handle Uncaught Errors

```javascript
process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  // Perform cleanup
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});
```

### Run with Least Privilege

```dockerfile
# Don't run as root
FROM node:20-alpine
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs
WORKDIR /app
COPY --chown=nodejs:nodejs . .
CMD ["node", "server.js"]
```

## Security Checklist

- [ ] Dependencies audited and up to date
- [ ] Lock files committed
- [ ] All user input validated
- [ ] Parameterized database queries
- [ ] Passwords hashed with bcrypt (cost >= 12)
- [ ] Sessions configured securely
- [ ] Security headers enabled (Helmet)
- [ ] CORS restricted to allowed origins
- [ ] Rate limiting on sensitive endpoints
- [ ] Errors don't leak internal details
- [ ] Secrets in environment variables, not code
- [ ] File uploads validated and sanitized
- [ ] Running as non-root user
- [ ] HTTPS enforced in production
