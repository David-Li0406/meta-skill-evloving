# MCP Security Best Practices

Comprehensive security guidelines for Model Context Protocol server development and deployment.

## Security Principles

**Defense in Depth**: Multiple security layers
**Least Privilege**: Minimal necessary permissions
**Fail Secure**: Errors default to denial
**Input Validation**: Trust no user input
**Output Encoding**: Sanitize all outputs
**Audit Logging**: Track security-relevant events

## Input Validation

### Validate All Inputs

**Required for:**
- Tool parameters
- Resource URIs
- Prompt arguments
- Client-provided data

**TypeScript Example:**
```typescript
import Ajv from "ajv";
const ajv = new Ajv();

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  // Schema validation
  const tool = tools.find((t) => t.name === name);
  const validate = ajv.compile(tool.inputSchema);

  if (!validate(args)) {
    throw new Error(`Invalid inputs: ${ajv.errorsText(validate.errors)}`);
  }

  // Type validation
  if (typeof args.param !== "string") {
    throw new Error("param must be string");
  }

  // Range validation
  if (args.count < 1 || args.count > 100) {
    throw new Error("count must be 1-100");
  }

  // Execute tool
});
```

**Python Example:**
```python
from jsonschema import validate, ValidationError

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    tool = next((t for t in tools if t.name == name), None)

    # Schema validation
    try:
        validate(instance=arguments, schema=tool["inputSchema"])
    except ValidationError as e:
        raise ValueError(f"Invalid inputs: {e.message}")

    # Type validation
    if not isinstance(arguments.get("param"), str):
        raise TypeError("param must be string")

    # Range validation
    count = arguments.get("count", 0)
    if not 1 <= count <= 100:
        raise ValueError("count must be 1-100")

    # Execute tool
```

### Path Validation

Prevent path traversal attacks.

**Bad:**
```typescript
// Vulnerable to path traversal
const filePath = args.path;
const content = fs.readFileSync(filePath);
```

**Good:**
```typescript
import path from "path";

// Validate and normalize path
const basePath = "/allowed/directory";
const requestedPath = path.normalize(args.path);
const absolutePath = path.resolve(basePath, requestedPath);

// Ensure within allowed directory
if (!absolutePath.startsWith(basePath)) {
  throw new Error("Path outside allowed directory");
}

// Check path components
if (requestedPath.includes("..")) {
  throw new Error("Path traversal not allowed");
}

const content = fs.readFileSync(absolutePath);
```

**Python:**
```python
import os
from pathlib import Path

# Validate and normalize path
base_path = Path("/allowed/directory").resolve()
requested_path = Path(args["path"]).resolve()

# Ensure within allowed directory
if not requested_path.is_relative_to(base_path):
    raise ValueError("Path outside allowed directory")

# Check for traversal
if ".." in args["path"]:
    raise ValueError("Path traversal not allowed")

content = requested_path.read_text()
```

### SQL Injection Prevention

Use parameterized queries, never string concatenation.

**Bad:**
```typescript
// Vulnerable to SQL injection
const query = `SELECT * FROM users WHERE id = ${args.userId}`;
const result = db.query(query);
```

**Good:**
```typescript
// Parameterized query
const query = "SELECT * FROM users WHERE id = ?";
const result = db.query(query, [args.userId]);

// Or with named parameters
const query = "SELECT * FROM users WHERE id = :userId";
const result = db.query(query, { userId: args.userId });
```

**Python:**
```python
# Bad - SQL injection vulnerable
query = f"SELECT * FROM users WHERE id = {args['userId']}"
cursor.execute(query)

# Good - Parameterized
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (args['userId'],))

# Or with named parameters
query = "SELECT * FROM users WHERE id = :userId"
cursor.execute(query, {"userId": args['userId']})
```

### Command Injection Prevention

Avoid shell execution with user input.

**Bad:**
```typescript
// Vulnerable to command injection
const { exec } = require("child_process");
exec(`ls ${args.directory}`, (error, stdout) => {
  // Process output
});
```

**Good:**
```typescript
// Use spawn with argument array (no shell)
const { spawn } = require("child_process");
const ls = spawn("ls", [args.directory]);

// Or validate whitelist
const allowedDirs = ["/dir1", "/dir2"];
if (!allowedDirs.includes(args.directory)) {
  throw new Error("Directory not allowed");
}
```

**Python:**
```python
import subprocess

# Bad - Shell injection vulnerable
subprocess.run(f"ls {args['directory']}", shell=True)

# Good - No shell, argument array
subprocess.run(["ls", args['directory']])

# Or validate whitelist
allowed_dirs = ["/dir1", "/dir2"]
if args['directory'] not in allowed_dirs:
    raise ValueError("Directory not allowed")
```

## Authentication and Authorization

### API Key Management

**Never hardcode secrets:**
```typescript
// Bad
const API_KEY = "sk-actual-secret-key";

// Good - Environment variables
const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  throw new Error("API_KEY environment variable required");
}
```

**Configuration:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

### Token Validation

```typescript
async function validateToken(token: string): Promise<boolean> {
  // Check token format
  if (!token || typeof token !== "string") {
    return false;
  }

  // Check token length
  if (token.length < 32) {
    return false;
  }

  // Verify against trusted source
  try {
    const response = await fetch("https://api.example.com/validate", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.ok;
  } catch {
    return false;
  }
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const token = request.params._meta?.token;

  if (!await validateToken(token)) {
    throw new Error("Unauthorized");
  }

  // Process request
});
```

### OAuth 2.0 Implementation

For remote SSE servers:

```typescript
import express from "express";
import passport from "passport";
import { Strategy as OAuth2Strategy } from "passport-oauth2";

passport.use(new OAuth2Strategy({
  authorizationURL: "https://provider.com/oauth/authorize",
  tokenURL: "https://provider.com/oauth/token",
  clientID: process.env.CLIENT_ID,
  clientSecret: process.env.CLIENT_SECRET,
  callbackURL: "https://yourserver.com/callback"
}, (accessToken, refreshToken, profile, done) => {
  // Verify user
  return done(null, profile);
}));

app.get("/sse", passport.authenticate("oauth2"), (req, res) => {
  // Authenticated SSE endpoint
});
```

### Rate Limiting

Prevent abuse:

```typescript
import rateLimit from "express-rate-limit";

const limiter = rateLimit({
  windowMs: 60000, // 1 minute
  max: 100, // 100 requests per window
  message: "Too many requests"
});

app.use("/mcp", limiter);
```

**Per-tool rate limiting:**
```typescript
const toolCallCounts = new Map<string, number>();

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name } = request.params;
  const count = toolCallCounts.get(name) || 0;

  if (count > 100) {
    throw new Error("Rate limit exceeded");
  }

  toolCallCounts.set(name, count + 1);

  // Reset after 1 minute
  setTimeout(() => {
    toolCallCounts.set(name, Math.max(0, (toolCallCounts.get(name) || 1) - 1));
  }, 60000);

  // Execute tool
});
```

## Secrets Management

### Environment Variables

**Server side:**
```typescript
interface Config {
  apiKey: string;
  databaseUrl: string;
  jwtSecret: string;
}

function loadConfig(): Config {
  const apiKey = process.env.API_KEY;
  const databaseUrl = process.env.DATABASE_URL;
  const jwtSecret = process.env.JWT_SECRET;

  if (!apiKey || !databaseUrl || !jwtSecret) {
    throw new Error("Missing required environment variables");
  }

  return { apiKey, databaseUrl, jwtSecret };
}

const config = loadConfig();
```

**Documentation:**
```markdown
## Required Environment Variables

- `API_KEY`: Service API key (obtain from dashboard)
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret for JWT signing (generate: `openssl rand -hex 32`)

## Optional Environment Variables

- `LOG_LEVEL`: Logging level (default: info)
- `TIMEOUT`: Request timeout ms (default: 30000)
```

### Secrets in Logs

**Never log secrets:**
```typescript
// Bad
console.log("API request", { apiKey: config.apiKey, endpoint });

// Good
console.log("API request", { endpoint });

// Good - Redacted
console.log("API request", {
  apiKey: config.apiKey.slice(0, 4) + "...",
  endpoint
});
```

**Structured logging:**
```typescript
function log(level: string, message: string, data: Record<string, any>) {
  const sanitized = { ...data };

  // Remove sensitive fields
  delete sanitized.apiKey;
  delete sanitized.password;
  delete sanitized.token;

  console.log(JSON.stringify({
    level,
    message,
    timestamp: new Date().toISOString(),
    ...sanitized
  }));
}
```

## Error Handling

### Information Disclosure Prevention

**Don't expose internals:**
```typescript
// Bad - Leaks internal details
try {
  await fetchFromDatabase(query);
} catch (error) {
  return {
    content: [{
      type: "text",
      text: `Database error: ${error.stack}` // Stack trace exposed!
    }],
    isError: true
  };
}

// Good - Generic error to client
try {
  await fetchFromDatabase(query);
} catch (error) {
  // Log detailed error server-side
  console.error("Database error:", error);

  // Return generic error to client
  return {
    content: [{
      type: "text",
      text: "Database operation failed"
    }],
    isError: true
  };
}
```

### Error Classification

```typescript
class PublicError extends Error {
  constructor(message: string, public code: number = -32001) {
    super(message);
    this.name = "PublicError";
  }
}

class InternalError extends Error {
  constructor(message: string, public originalError?: Error) {
    super(message);
    this.name = "InternalError";
  }
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    // Tool implementation
  } catch (error) {
    if (error instanceof PublicError) {
      // Safe to return to client
      return {
        content: [{ type: "text", text: error.message }],
        isError: true
      };
    }

    // Log internal errors
    console.error("Internal error:", error);

    // Return generic message
    return {
      content: [{ type: "text", text: "Internal server error" }],
      isError: true
    };
  }
});
```

## Resource Access Control

### File System Access

**Whitelist approach:**
```typescript
const ALLOWED_DIRECTORIES = [
  "/workspace/data",
  "/workspace/output"
];

function validatePath(requestedPath: string): string {
  const normalized = path.normalize(requestedPath);
  const resolved = path.resolve(normalized);

  const allowed = ALLOWED_DIRECTORIES.some(dir =>
    resolved.startsWith(path.resolve(dir))
  );

  if (!allowed) {
    throw new PublicError("Access denied");
  }

  return resolved;
}

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  const filePath = new URL(uri).pathname;
  const validPath = validatePath(filePath);

  return {
    contents: [{
      uri,
      mimeType: "text/plain",
      text: fs.readFileSync(validPath, "utf-8")
    }]
  };
});
```

### Network Access

**URL validation:**
```typescript
const ALLOWED_HOSTS = ["api.example.com", "data.example.com"];

async function fetchFromAPI(url: string): Promise<Response> {
  const parsed = new URL(url);

  // Validate protocol
  if (parsed.protocol !== "https:") {
    throw new PublicError("Only HTTPS allowed");
  }

  // Validate host
  if (!ALLOWED_HOSTS.includes(parsed.hostname)) {
    throw new PublicError("Host not allowed");
  }

  // Prevent SSRF to internal networks
  const ip = await dns.resolve4(parsed.hostname);
  if (isPrivateIP(ip[0])) {
    throw new PublicError("Internal IPs not allowed");
  }

  return fetch(url);
}

function isPrivateIP(ip: string): boolean {
  return (
    ip.startsWith("10.") ||
    ip.startsWith("172.16.") ||
    ip.startsWith("192.168.") ||
    ip === "127.0.0.1"
  );
}
```

### Database Access

**Row-level security:**
```typescript
async function queryDatabase(userId: string, query: string) {
  // Set session context for RLS
  await db.query("SET app.current_user_id = $1", [userId]);

  // Query now respects RLS policies
  const result = await db.query(query);

  return result.rows;
}
```

**Permission checks:**
```typescript
async function checkPermission(userId: string, resource: string, action: string): Promise<boolean> {
  const result = await db.query(
    "SELECT has_permission($1, $2, $3)",
    [userId, resource, action]
  );

  return result.rows[0].has_permission;
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const userId = request.params._meta?.userId;

  if (name === "delete-record") {
    if (!await checkPermission(userId, args.recordId, "delete")) {
      throw new PublicError("Permission denied");
    }

    // Proceed with deletion
  }
});
```

## Secure Communication

### TLS/SSL for SSE

**Require HTTPS:**
```typescript
import express from "express";
import https from "https";
import fs from "fs";

const app = express();

const options = {
  key: fs.readFileSync("privkey.pem"),
  cert: fs.readFileSync("fullchain.pem")
};

https.createServer(options, app).listen(443);

// Redirect HTTP to HTTPS
app.use((req, res, next) => {
  if (req.secure) {
    next();
  } else {
    res.redirect(`https://${req.headers.host}${req.url}`);
  }
});
```

### Certificate Validation

**Client-side:**
```typescript
import https from "https";

const agent = new https.Agent({
  rejectUnauthorized: true, // Verify certificates
  ca: fs.readFileSync("ca-cert.pem") // Custom CA if needed
});

const response = await fetch("https://api.example.com", { agent });
```

## Audit Logging

### Security Event Logging

```typescript
interface AuditLog {
  timestamp: string;
  event: string;
  userId?: string;
  resource?: string;
  action?: string;
  result: "success" | "failure";
  details?: Record<string, any>;
}

function auditLog(log: AuditLog) {
  console.log(JSON.stringify({
    ...log,
    timestamp: new Date().toISOString()
  }));

  // Send to logging service
  // sendToLogService(log);
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const userId = request.params._meta?.userId;

  try {
    const result = await executeTool(name, args);

    auditLog({
      timestamp: new Date().toISOString(),
      event: "tool_call",
      userId,
      resource: name,
      action: "execute",
      result: "success"
    });

    return result;
  } catch (error) {
    auditLog({
      timestamp: new Date().toISOString(),
      event: "tool_call",
      userId,
      resource: name,
      action: "execute",
      result: "failure",
      details: { error: error.message }
    });

    throw error;
  }
});
```

### Log Sensitive Operations

Track security-relevant events:
- Authentication attempts (success/failure)
- Authorization failures
- Resource access (file reads, database queries)
- Configuration changes
- Error conditions
- Rate limit hits

## Dependency Security

### Regular Updates

```bash
# Check for vulnerabilities
npm audit

# Update dependencies
npm update

# Fix vulnerabilities
npm audit fix
```

**Python:**
```bash
# Check for vulnerabilities
pip-audit

# Update dependencies
pip install --upgrade package-name
```

### Pin Versions

**package.json:**
```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "1.0.0", // Exact version
    "other-package": "^2.0.0" // Minor updates allowed
  }
}
```

**Lock files:**
- Commit `package-lock.json` (npm)
- Commit `poetry.lock` (Poetry)
- Commit `Pipfile.lock` (Pipenv)

### Minimal Dependencies

- Only include necessary packages
- Review dependencies before adding
- Check for known vulnerabilities
- Prefer well-maintained packages
- Avoid deprecated packages

## Security Checklist

Before deployment:

**Input Validation:**
- [ ] All tool parameters validated against schemas
- [ ] Type checking on all inputs
- [ ] Range/format validation
- [ ] Path traversal prevention
- [ ] SQL injection prevention
- [ ] Command injection prevention

**Authentication/Authorization:**
- [ ] API keys via environment variables
- [ ] Token validation implemented
- [ ] Rate limiting configured
- [ ] Permission checks on sensitive operations
- [ ] Session management if stateful

**Secrets Management:**
- [ ] No hardcoded credentials
- [ ] Secrets in environment variables
- [ ] Secrets not logged
- [ ] Documentation of required secrets

**Error Handling:**
- [ ] No stack traces to client
- [ ] Generic errors for security issues
- [ ] Detailed logging server-side
- [ ] No information disclosure

**Resource Access:**
- [ ] File system access restricted
- [ ] Network access validated
- [ ] Database access controlled
- [ ] URL validation for SSRF prevention

**Communication:**
- [ ] HTTPS for remote servers
- [ ] Certificate validation
- [ ] Secure headers

**Logging:**
- [ ] Security events logged
- [ ] Sensitive operations tracked
- [ ] No secrets in logs

**Dependencies:**
- [ ] Vulnerabilities checked
- [ ] Dependencies up to date
- [ ] Versions pinned

## Security Testing

### Fuzzing Tool Inputs

```typescript
// Test with unexpected inputs
const testCases = [
  "",
  " ",
  "null",
  "undefined",
  "../../etc/passwd",
  "<script>alert(1)</script>",
  "' OR 1=1 --",
  "\x00",
  "A".repeat(10000)
];

for (const input of testCases) {
  try {
    await callTool("tool-name", { param: input });
    console.log(`Input accepted: ${input}`);
  } catch (error) {
    console.log(`Input rejected: ${input}`);
  }
}
```

### Penetration Testing

Test for:
- Path traversal: `../../../../etc/passwd`
- SQL injection: `' OR '1'='1`
- Command injection: `; cat /etc/passwd`
- SSRF: `http://localhost:6379/`
- XXE: XML with external entities
- Prototype pollution: `{"__proto__": {"isAdmin": true}}`

### Static Analysis

```bash
# TypeScript
npm install --save-dev eslint @typescript-eslint/eslint-plugin
npx eslint src/**/*.ts

# Python
pip install bandit
bandit -r src/
```

## Reference Documentation

**MCP Security:**
- https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices
- https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
- https://modelcontextprotocol.io/docs/tutorials/security/authorization

**OWASP Resources:**
- https://owasp.org/www-project-top-ten/
- https://cheatsheetseries.owasp.org/
