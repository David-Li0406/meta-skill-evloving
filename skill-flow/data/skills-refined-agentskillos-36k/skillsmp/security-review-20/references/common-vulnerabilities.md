# Common Security Vulnerabilities

Detailed patterns for security issues by category.

## Injection Vulnerabilities

### SQL Injection

**Pattern**: User input concatenated directly into SQL queries.

**Node.js Examples**:
```javascript
// VULNERABLE
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

// SAFE
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

**.NET Examples**:
```csharp
// VULNERABLE
var query = "SELECT * FROM Users WHERE Id = " + userId;
cmd.CommandText = query;

// SAFE
var query = "SELECT * FROM Users WHERE Id = @id";
cmd.Parameters.AddWithValue("@id", userId);
```

**Severity**: Critical

### Command Injection

**Pattern**: User input passed to shell commands.

**Node.js Examples**:
```javascript
// VULNERABLE
exec(`ls ${userInput}`);
spawn('sh', ['-c', userInput]);

// SAFE
execFile('ls', [sanitizedPath]);
```

**.NET Examples**:
```csharp
// VULNERABLE
Process.Start("cmd", "/c " + userInput);

// SAFE
var psi = new ProcessStartInfo("myapp", escapedArgs);
```

**Severity**: Critical

### XSS (Cross-Site Scripting)

**Pattern**: User input rendered in HTML without escaping.

**Node.js Examples**:
```javascript
// VULNERABLE
res.send(`<div>${userInput}</div>`);
element.innerHTML = userInput;

// SAFE
res.send(`<div>${escapeHtml(userInput)}</div>`);
element.textContent = userInput;
```

**.NET Examples**:
```csharp
// VULNERABLE
@Html.Raw(userInput)

// SAFE
@Html.Encode(userInput)
@userInput  // Razor auto-encodes
```

**Severity**: Major (stored XSS = Critical)

## Authentication & Authorization

### Missing Authentication

**Pattern**: Endpoints accessible without authentication.

**Node.js Examples**:
```javascript
// VULNERABLE - no auth middleware
app.get('/api/admin/users', (req, res) => { ... });

// SAFE
app.get('/api/admin/users', requireAuth, requireAdmin, (req, res) => { ... });
```

**.NET Examples**:
```csharp
// VULNERABLE - missing [Authorize]
[HttpGet("admin/users")]
public IActionResult GetUsers() { ... }

// SAFE
[Authorize(Roles = "Admin")]
[HttpGet("admin/users")]
public IActionResult GetUsers() { ... }
```

**Severity**: Critical

### Broken Access Control

**Pattern**: Users can access resources they shouldn't.

```javascript
// VULNERABLE - no ownership check
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findById(req.params.id);
  res.json(order);
});

// SAFE
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findById(req.params.id);
  if (order.userId !== req.user.id) return res.status(403).send();
  res.json(order);
});
```

**Severity**: Critical

## Sensitive Data Exposure

### Hardcoded Secrets

**Pattern**: API keys, passwords, tokens in source code.

```javascript
// VULNERABLE
const API_KEY = 'sk-1234567890abcdef';
const password = 'admin123';

// SAFE
const API_KEY = process.env.API_KEY;
```

**Detection Patterns**:
- `password\s*=\s*["'][^"']+["']`
- `api[_-]?key\s*=\s*["'][^"']+["']`
- `secret\s*=\s*["'][^"']+["']`
- `token\s*=\s*["'][^"']+["']`

**Severity**: Critical

### Sensitive Data in Logs

**Pattern**: Logging passwords, tokens, PII.

```javascript
// VULNERABLE
console.log('User login:', { email, password });
logger.info('Request:', req.body);

// SAFE
console.log('User login:', { email });
logger.info('Request:', sanitizeForLogging(req.body));
```

**Severity**: Major

## Cryptographic Issues

### Weak Hashing

**Pattern**: Using MD5, SHA1, or no salt for passwords.

```javascript
// VULNERABLE
const hash = crypto.createHash('md5').update(password).digest('hex');

// SAFE
const hash = await bcrypt.hash(password, 12);
```

**Severity**: Critical

### Insecure Random

**Pattern**: Using Math.random() for security purposes.

```javascript
// VULNERABLE
const token = Math.random().toString(36);

// SAFE
const token = crypto.randomBytes(32).toString('hex');
```

**Severity**: Major

## Input Validation

### Path Traversal

**Pattern**: User input in file paths without validation.

```javascript
// VULNERABLE
const filePath = path.join('/uploads', req.params.filename);
fs.readFile(filePath);

// SAFE
const filename = path.basename(req.params.filename);
const filePath = path.join('/uploads', filename);
```

**Severity**: Critical

### Regex DoS (ReDoS)

**Pattern**: User input matched against vulnerable regex.

```javascript
// VULNERABLE - catastrophic backtracking
const emailRegex = /^([a-zA-Z0-9]+)+@[a-zA-Z0-9]+$/;
emailRegex.test(userInput);

// SAFE - linear time
const emailRegex = /^[a-zA-Z0-9]+@[a-zA-Z0-9]+$/;
```

**Severity**: Major

## Deserialization

### Unsafe Deserialization

**Pattern**: Deserializing untrusted data.

```javascript
// VULNERABLE
const obj = eval('(' + userInput + ')');
const data = JSON.parse(userInput); // with reviver that executes code

// SAFE
const data = JSON.parse(userInput); // plain JSON.parse is safe
```

**.NET Examples**:
```csharp
// VULNERABLE
var obj = JsonConvert.DeserializeObject(input, new JsonSerializerSettings {
    TypeNameHandling = TypeNameHandling.All
});

// SAFE
var obj = JsonConvert.DeserializeObject<MyType>(input);
```

**Severity**: Critical

## Security Headers

### Missing Headers

Check for these security headers:
- `Content-Security-Policy`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` or `SAMEORIGIN`
- `Strict-Transport-Security`
- `X-XSS-Protection: 1; mode=block`

**Severity**: Minor to Major depending on context

## OWASP Top 10 Quick Reference

| Rank | Vulnerability | Severity |
|------|--------------|----------|
| A01 | Broken Access Control | Critical |
| A02 | Cryptographic Failures | Critical |
| A03 | Injection | Critical |
| A04 | Insecure Design | Major |
| A05 | Security Misconfiguration | Major |
| A06 | Vulnerable Components | Major |
| A07 | Auth Failures | Critical |
| A08 | Software/Data Integrity | Major |
| A09 | Logging Failures | Minor |
| A10 | SSRF | Critical |
