# Security Owasp - Sharp Edges

## Idor

### **Id**
idor
### **Summary**
Insecure Direct Object Reference
### **Severity**
critical
### **Situation**
  API endpoint /api/users/123 returns user data. Change to /api/users/124.
  Get someone else's data. No check if current user should access that ID.
  Attackers iterate through all IDs and download your entire database.
  
### **Why**
  Endpoints often take resource IDs from URL/body without verifying the
  requester has permission to access that specific resource. Easy to
  implement, easy to forget the authorization check.
  
### **Solution**
  # ALWAYS VERIFY RESOURCE ACCESS
  
  // WRONG: Just fetch by ID
  app.get('/api/orders/:id', async (req, res) => {
    const order = await db.order.findUnique({
      where: { id: req.params.id }
    });
    res.json(order);  // Anyone can access any order!
  });
  
  
  // RIGHT: Verify ownership
  app.get('/api/orders/:id', async (req, res) => {
    const order = await db.order.findUnique({
      where: {
        id: req.params.id,
        userId: req.user.id,  // Must belong to current user
      }
    });
  
    if (!order) {
      return res.status(404).json({ error: 'Not found' });
    }
  
    res.json(order);
  });
  
  
  // RIGHT: Role-based with organization scope
  app.get('/api/orders/:id', async (req, res) => {
    const order = await db.order.findUnique({
      where: { id: req.params.id }
    });
  
    if (!order) {
      return res.status(404).json({ error: 'Not found' });
    }
  
    // Check permission
    const canAccess =
      order.userId === req.user.id ||  // Owner
      (req.user.role === 'admin' &&
       order.orgId === req.user.orgId);  // Org admin
  
    if (!canAccess) {
      return res.status(403).json({ error: 'Forbidden' });
    }
  
    res.json(order);
  });
  
  
  // Use UUIDs instead of sequential IDs
  // Harder to guess, but still need auth!
  
### **Symptoms**
  - Can access other users' data by changing IDs
  - No authorization check on resources
  - Sequential IDs easy to enumerate
### **Detection Pattern**
params\\.(id|userId)(?![\\s\\S]*user\\.id)

## Mass Assignment

### **Id**
mass-assignment
### **Summary**
Uncontrolled property assignment
### **Severity**
critical
### **Situation**
  User registration accepts { name, email, password }. Attacker sends
  { name, email, password, role: 'admin', verified: true }. Server
  blindly spreads input into database. Attacker is now admin.
  
### **Why**
  Spreading request body directly into database operations allows
  attackers to set fields they shouldn't control. ORMs make this
  easy with { ...req.body }.
  
### **Solution**
  # EXPLICITLY PICK ALLOWED FIELDS
  
  // WRONG: Spread everything
  app.post('/api/users', async (req, res) => {
    const user = await db.user.create({
      data: req.body,  // Attacker can set any field!
    });
  });
  
  
  // RIGHT: Explicit allowlist
  app.post('/api/users', async (req, res) => {
    const { name, email, password } = req.body;
  
    const user = await db.user.create({
      data: {
        name,
        email,
        passwordHash: await hash(password),
        role: 'user',      // Server controls this
        verified: false,   // Server controls this
      },
    });
  });
  
  
  // RIGHT: Use validation schema
  const createUserSchema = z.object({
    name: z.string().min(1).max(100),
    email: z.string().email(),
    password: z.string().min(12),
  });
  
  app.post('/api/users', async (req, res) => {
    const data = createUserSchema.parse(req.body);
    // Only validated fields exist in `data`
  });
  
  
  // For updates, separate schemas per role
  const userUpdateSchema = z.object({
    name: z.string().optional(),
    email: z.string().email().optional(),
  });
  
  const adminUpdateSchema = userUpdateSchema.extend({
    role: z.enum(['user', 'admin']).optional(),
    verified: z.boolean().optional(),
  });
  
### **Symptoms**
  - Attackers can set role/admin flags
  - Hidden fields can be manipulated
  - "...req.body" in database operations
### **Detection Pattern**
\\.create\\(.*req\\.body|update\\(.*\\.\\.\\.req

## Jwt None Algorithm

### **Id**
jwt-none-algorithm
### **Summary**
JWT accepts 'none' algorithm
### **Severity**
critical
### **Situation**
  Your JWT library accepts the 'none' algorithm. Attacker creates a
  token with algorithm: 'none', no signature needed. Token validates.
  Attacker is now any user they want.
  
### **Why**
  JWT spec includes 'none' algorithm for testing. Some libraries accept
  it by default. If you don't explicitly require specific algorithms,
  attackers can forge valid tokens without the secret.
  
### **Solution**
  # ALWAYS SPECIFY ALLOWED ALGORITHMS
  
  import jwt from 'jsonwebtoken';
  
  // WRONG: No algorithm specified
  const decoded = jwt.verify(token, secret);
  
  
  // RIGHT: Explicit algorithm
  const decoded = jwt.verify(token, secret, {
    algorithms: ['HS256'],  // Only accept this
  });
  
  
  // For RS256 (asymmetric)
  const decoded = jwt.verify(token, publicKey, {
    algorithms: ['RS256'],
  });
  
  
  // jose library (recommended)
  import { jwtVerify } from 'jose';
  
  const { payload } = await jwtVerify(
    token,
    secret,
    {
      algorithms: ['HS256'],
      issuer: 'https://your-app.com',
      audience: 'your-app',
    }
  );
  
  
  // Also validate claims
  if (payload.exp < Date.now() / 1000) {
    throw new Error('Token expired');
  }
  if (payload.iss !== 'https://your-app.com') {
    throw new Error('Invalid issuer');
  }
  
### **Symptoms**
  - Tokens with no signature accepted
  - No algorithm validation
  - "alg: none" works
### **Detection Pattern**
jwt\\.verify\\([^,]+,[^,]+\\)$

## Timing Attacks

### **Id**
timing-attacks
### **Summary**
Password comparison leaks info via timing
### **Severity**
high
### **Situation**
  Password check uses ===. Attacker measures response time. Wrong first
  character: fast. Wrong last character: slower. Attacker determines
  password character by character through timing.
  
### **Why**
  String comparison (===) returns immediately on first difference.
  Attackers can measure tiny timing differences to determine how much
  of their guess was correct.
  
### **Solution**
  # USE CONSTANT-TIME COMPARISON
  
  import { timingSafeEqual } from 'crypto';
  
  // WRONG: Regular comparison
  if (inputPassword === storedPassword) {
    // Vulnerable to timing attack
  }
  
  
  // RIGHT: Constant-time comparison
  function safeCompare(a: string, b: string): boolean {
    const bufA = Buffer.from(a);
    const bufB = Buffer.from(b);
  
    // Must be same length for timingSafeEqual
    if (bufA.length !== bufB.length) {
      // Still do comparison to maintain constant time
      timingSafeEqual(bufA, bufA);
      return false;
    }
  
    return timingSafeEqual(bufA, bufB);
  }
  
  
  // For passwords, use proper hashing library
  // bcrypt.compare and argon2.verify are timing-safe
  import { verify } from '@node-rs/argon2';
  
  const isValid = await verify(storedHash, inputPassword);
  
  
  // For HMAC comparison
  import { createHmac, timingSafeEqual } from 'crypto';
  
  function verifyHmac(data: string, signature: string, key: string): boolean {
    const expected = createHmac('sha256', key).update(data).digest();
    const received = Buffer.from(signature, 'hex');
  
    if (expected.length !== received.length) {
      return false;
    }
  
    return timingSafeEqual(expected, received);
  }
  
### **Symptoms**
  - Response time varies with input
  - Using === for secrets
  - Not using crypto library comparison
### **Detection Pattern**
(password|secret|token|key)\\s*===\\s*

## Ssrf

### **Id**
ssrf
### **Summary**
Server-Side Request Forgery
### **Severity**
high
### **Situation**
  Feature: "Preview URL" - user provides URL, server fetches it. Attacker
  provides http://169.254.169.254/latest/meta-data/. Server fetches
  AWS metadata, returns instance credentials. Game over.
  
### **Why**
  Server-side HTTP requests to user-controlled URLs can access internal
  services, cloud metadata endpoints, or internal network. The server
  becomes a proxy for the attacker.
  
### **Solution**
  # VALIDATE AND RESTRICT URLS
  
  import { URL } from 'url';
  
  const BLOCKED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '169.254.169.254',  // AWS metadata
    'metadata.google.internal',  // GCP
    '10.',  // Private networks
    '172.16.', '172.17.', '172.18.', // ...
    '192.168.',
  ];
  
  function isUrlAllowed(urlString: string): boolean {
    try {
      const url = new URL(urlString);
  
      // Only allow http(s)
      if (!['http:', 'https:'].includes(url.protocol)) {
        return false;
      }
  
      // Check against blocklist
      const host = url.hostname.toLowerCase();
      for (const blocked of BLOCKED_HOSTS) {
        if (host === blocked || host.startsWith(blocked)) {
          return false;
        }
      }
  
      // Resolve DNS and check IP (prevent DNS rebinding)
      const ips = await dns.resolve(host);
      for (const ip of ips) {
        if (isPrivateIp(ip)) {
          return false;
        }
      }
  
      return true;
    } catch {
      return false;
    }
  }
  
  
  // Use allowlist when possible
  const ALLOWED_DOMAINS = ['example.com', 'api.trusted.com'];
  
  function isAllowedDomain(url: URL): boolean {
    return ALLOWED_DOMAINS.some(
      domain => url.hostname === domain ||
                url.hostname.endsWith('.' + domain)
    );
  }
  
  
  // Limit what the fetched content can do
  const response = await fetch(url, {
    redirect: 'error',  // Don't follow redirects
    timeout: 5000,      // Prevent slow loris
  });
  
  // Validate content type
  if (!response.headers.get('content-type')?.includes('text/html')) {
    throw new Error('Invalid content type');
  }
  
### **Symptoms**
  - User-provided URLs fetched server-side
  - No URL validation
  - Access to internal services
### **Detection Pattern**
fetch\\(.*req\\.(body|query)|axios\\(.*input

## Secrets In Logs

### **Id**
secrets-in-logs
### **Summary**
Logging sensitive data
### **Severity**
high
### **Situation**
  You log request bodies for debugging. Password resets, API keys,
  personal data all go to logs. Logs go to log aggregator. Now
  everyone with log access sees credentials.
  
### **Why**
  Logs are often less secured than databases. They're shared for
  debugging, sent to third parties, kept longer than needed. Logging
  sensitive data creates copies of secrets everywhere.
  
### **Solution**
  # REDACT SENSITIVE FIELDS
  
  const SENSITIVE_FIELDS = [
    'password', 'token', 'secret', 'apiKey', 'api_key',
    'authorization', 'cookie', 'ssn', 'creditCard',
  ];
  
  function redactSensitive(obj: unknown, seen = new WeakSet()): unknown {
    if (obj === null || typeof obj !== 'object') {
      return obj;
    }
  
    if (seen.has(obj)) return '[Circular]';
    seen.add(obj);
  
    if (Array.isArray(obj)) {
      return obj.map(item => redactSensitive(item, seen));
    }
  
    const result: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(obj)) {
      if (SENSITIVE_FIELDS.some(f =>
        key.toLowerCase().includes(f.toLowerCase())
      )) {
        result[key] = '[REDACTED]';
      } else {
        result[key] = redactSensitive(value, seen);
      }
    }
    return result;
  }
  
  // Use in logging
  logger.info('Request', redactSensitive(req.body));
  
  
  // Or use a logging library with redaction
  import pino from 'pino';
  
  const logger = pino({
    redact: {
      paths: [
        'req.headers.authorization',
        'req.headers.cookie',
        '*.password',
        '*.token',
        '*.apiKey',
      ],
      censor: '[REDACTED]',
    },
  });
  
### **Symptoms**
  - Passwords in log files
  - API keys in error messages
  - PII in debug logs
### **Detection Pattern**
console\\.log.*password|logger\\.(info|debug).*token

## Path Traversal

### **Id**
path-traversal
### **Summary**
Directory traversal attacks
### **Severity**
high
### **Situation**
  File download: /files?name=report.pdf. Attacker sends
  /files?name=../../../etc/passwd. Server reads system files.
  Or /files?name=../config/.env. Attacker gets your secrets.
  
### **Why**
  When user input is used to construct file paths without validation,
  attackers can use ../ sequences to escape the intended directory
  and access any file the server can read.
  
### **Solution**
  # VALIDATE AND RESOLVE PATHS
  
  import path from 'path';
  import fs from 'fs/promises';
  
  const UPLOAD_DIR = '/app/uploads';
  
  async function getFile(filename: string): Promise<Buffer> {
    // Remove any path components
    const safeName = path.basename(filename);
  
    // Resolve full path
    const fullPath = path.resolve(UPLOAD_DIR, safeName);
  
    // Verify it's still in allowed directory
    if (!fullPath.startsWith(UPLOAD_DIR)) {
      throw new Error('Invalid path');
    }
  
    // Check file exists
    try {
      await fs.access(fullPath);
    } catch {
      throw new Error('File not found');
    }
  
    return fs.readFile(fullPath);
  }
  
  
  // For user-facing filenames, use IDs
  app.get('/files/:id', async (req, res) => {
    // Look up file by ID in database
    const file = await db.file.findUnique({
      where: { id: req.params.id }
    });
  
    if (!file || file.userId !== req.user.id) {
      return res.status(404).send();
    }
  
    // Path stored in database, not from user
    res.sendFile(file.path);
  });
  
  
  // Validate filename characters
  function isSafeFilename(name: string): boolean {
    return /^[a-zA-Z0-9_.-]+$/.test(name) &&
           !name.includes('..') &&
           name.length < 255;
  }
  
### **Symptoms**
  - "../" in file paths works
  - User input in file operations
  - Can read files outside upload directory
### **Detection Pattern**
readFile.*req\\.(params|query|body)