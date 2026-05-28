# Security Code Review Guide

Patterns and checklists for security-focused code reviews with Claude Code.

## Review Process

### 1. Initial Assessment

Before diving into code, understand the context:

```
"What sensitive data does this code handle?"
"What are the trust boundaries?"
"Who has access to this system?"
"What's the potential impact of a vulnerability?"
```

### 2. Security Review Prompts

Use these prompts with Claude Code for comprehensive reviews:

#### Full Security Audit

```
"Perform a security audit on this codebase focusing on:
1. Authentication and authorization flaws
2. Injection vulnerabilities (SQL, command, XSS)
3. Sensitive data exposure
4. Cryptographic issues
5. Security misconfiguration
6. Broken access control"
```

#### Specific Focus Areas

```
"Review this authentication code for:
- Password storage security
- Session management issues
- Timing attack vulnerabilities
- Rate limiting gaps
- Account enumeration risks"

"Check this API endpoint for:
- Input validation completeness
- Authorization checks
- SQL/NoSQL injection
- Mass assignment vulnerabilities
- Rate limiting"

"Audit this file handling code for:
- Path traversal vulnerabilities
- Unrestricted file upload
- File type validation
- Storage security"
```

## Security Checklists

### Authentication Review

```markdown
## Authentication Checklist

### Password Handling
- [ ] Passwords hashed with Argon2id, bcrypt, or scrypt
- [ ] Minimum password length enforced (12+ chars recommended)
- [ ] Password complexity requirements (or use zxcvbn)
- [ ] Passwords never logged or exposed in errors
- [ ] Constant-time comparison for password verification

### Session Management
- [ ] Session tokens cryptographically random (32+ bytes)
- [ ] Sessions invalidated on logout
- [ ] Session timeout implemented
- [ ] Cookies marked HttpOnly, Secure, SameSite
- [ ] Session regeneration after authentication

### Account Security
- [ ] Account lockout after failed attempts
- [ ] Rate limiting on login endpoint
- [ ] No user enumeration (consistent error messages)
- [ ] Secure password reset flow
- [ ] MFA support available
```

### API Security Review

```markdown
## API Security Checklist

### Input Validation
- [ ] All inputs validated and sanitized
- [ ] Schema validation (Zod, Joi, etc.)
- [ ] Type coercion prevented
- [ ] Array/object size limits
- [ ] String length limits
- [ ] Numeric range validation

### Authorization
- [ ] Authentication required for protected endpoints
- [ ] Authorization checked for each request
- [ ] Resource ownership verified
- [ ] Role-based access control implemented
- [ ] No IDOR vulnerabilities

### Data Protection
- [ ] Sensitive data not in URLs
- [ ] Response filtering (no internal fields exposed)
- [ ] Pagination limits enforced
- [ ] Rate limiting implemented
- [ ] CORS properly configured
```

### Database Security Review

```markdown
## Database Security Checklist

### Query Safety
- [ ] All queries parameterized
- [ ] No string concatenation for queries
- [ ] ORM used correctly
- [ ] Raw queries reviewed carefully
- [ ] Stored procedures validated

### Access Control
- [ ] Least privilege database users
- [ ] Sensitive columns encrypted
- [ ] Audit logging enabled
- [ ] Backup encryption enabled
- [ ] Connection encryption (TLS)

### Data Handling
- [ ] PII identified and protected
- [ ] Data retention policies implemented
- [ ] Soft delete for recoverable data
- [ ] No sensitive data in logs
```

### Frontend Security Review

```markdown
## Frontend Security Checklist

### XSS Prevention
- [ ] Output encoding enabled (React, Vue default)
- [ ] dangerouslySetInnerHTML avoided or sanitized
- [ ] User content properly escaped
- [ ] CSP headers configured
- [ ] No inline event handlers with user data

### Data Protection
- [ ] No secrets in client code
- [ ] Sensitive data not in localStorage
- [ ] HTTPS enforced
- [ ] Secure cookie settings
- [ ] No sensitive data in URLs

### Third-Party Security
- [ ] Dependencies audited
- [ ] Subresource integrity for CDN scripts
- [ ] Iframe sandboxing
- [ ] postMessage origin validation
```

## Code Patterns to Flag

### High Severity

```typescript
// FLAG: SQL string concatenation
const query = `SELECT * FROM users WHERE id = '${id}'`;

// FLAG: Command injection risk
exec(`convert ${filename} output.png`);

// FLAG: Hardcoded secrets
const apiKey = 'sk_live_1234567890';

// FLAG: Unsafe deserialization
const data = JSON.parse(userInput);
eval(data.code);

// FLAG: Path traversal
const file = `./uploads/${userFilename}`;

// FLAG: Disabled security
// eslint-disable-next-line security/detect-object-injection
obj[userKey] = value;
```

### Medium Severity

```typescript
// FLAG: Missing input validation
app.post('/api/users', (req, res) => {
  const user = User.create(req.body);  // Mass assignment
});

// FLAG: Weak crypto
const hash = crypto.createHash('md5').update(password).digest('hex');

// FLAG: Insufficient randomness
const token = Math.random().toString(36);

// FLAG: Missing rate limiting
app.post('/login', loginHandler);  // No rate limit

// FLAG: Information disclosure
catch (error) {
  res.status(500).json({ error: error.message, stack: error.stack });
}
```

### Low Severity (But Worth Noting)

```typescript
// FLAG: Verbose error messages
throw new Error(`User ${userId} not found in database ${dbName}`);

// FLAG: Debug logging in production
console.log('User data:', userData);

// FLAG: Commented security code
// authMiddleware,  // Temporarily disabled for testing

// FLAG: TODO security items
// TODO: Add input validation
// FIXME: Rate limiting needed
```

## Review Templates

### Pull Request Security Review

```markdown
## Security Review: PR #{number}

### Summary
Brief description of changes and security implications.

### Risk Assessment
- [ ] High risk - handles auth/crypto/sensitive data
- [ ] Medium risk - user input/API changes
- [ ] Low risk - internal changes/bug fixes

### Security Checklist
- [ ] Input validation reviewed
- [ ] Authorization checks verified
- [ ] No hardcoded secrets
- [ ] Error handling secure
- [ ] Dependencies safe

### Findings

#### Critical
None found / List issues

#### High
None found / List issues

#### Medium
None found / List issues

#### Low / Informational
None found / List issues

### Recommendations
- Suggestion 1
- Suggestion 2

### Approval
- [ ] Approved for merge
- [ ] Requires changes
- [ ] Needs security team review
```

### Vulnerability Report

```markdown
## Vulnerability Report

### Title
Brief descriptive title

### Severity
Critical / High / Medium / Low

### Location
File: `path/to/file.ts`
Lines: 42-58

### Description
Detailed description of the vulnerability.

### Proof of Concept
```typescript
// Code demonstrating the vulnerability
```

### Impact
What can an attacker do with this vulnerability?

### Remediation
```typescript
// Suggested fix
```

### References
- Link to relevant OWASP page
- Link to CWE entry
```

## Automated Security Checks

### ESLint Security Rules

```json
{
  "extends": [
    "plugin:security/recommended"
  ],
  "plugins": ["security"],
  "rules": {
    "security/detect-object-injection": "warn",
    "security/detect-non-literal-regexp": "warn",
    "security/detect-non-literal-fs-filename": "warn",
    "security/detect-eval-with-expression": "error",
    "security/detect-no-csrf-before-method-override": "error",
    "security/detect-possible-timing-attacks": "warn"
  }
}
```

### Security Testing Commands

```bash
# Dependency vulnerabilities
bun audit

# Static analysis
npx eslint --ext .ts,.tsx src/ --rule 'security/*: error'

# Secret scanning
gitleaks detect --source .

# SAST with Semgrep
npx semgrep --config auto src/

# Check for known vulnerabilities
npx snyk test
```

### CI Pipeline Security Checks

```yaml
# .github/workflows/security.yml
name: Security Checks

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: auto

      - name: Dependency audit
        run: bun audit
```

## Review Conversation Examples

### Authentication Review

```
User: "Review this login function for security issues"

Claude: "I'll review this login function for security vulnerabilities.

**Issues Found:**

1. **Timing Attack Vulnerability** (High)
   Line 15: Early return on user not found allows timing-based user enumeration.

   ```typescript
   // Current (vulnerable)
   if (!user) return { error: 'Invalid credentials' };

   // Fixed
   const user = await findUser(email);
   const passwordValid = user
     ? await verify(user.hash, password)
     : await verify(DUMMY_HASH, password);
   if (!user || !passwordValid) {
     return { error: 'Invalid credentials' };
   }
   ```

2. **Missing Rate Limiting** (High)
   No rate limiting on login attempts enables brute force attacks.

   Add rate limiting:
   ```typescript
   const loginLimiter = rateLimit({
     windowMs: 15 * 60 * 1000,
     max: 5,
   });
   ```

3. **Weak Password Hashing** (Critical)
   Line 23: Using MD5 for password hashing.

   ```typescript
   // Current (insecure)
   const hash = crypto.createHash('md5').update(password).digest('hex');

   // Fixed
   const hash = await argon2.hash(password);
   ```

Would you like me to provide complete remediation code?"
```

### API Endpoint Review

```
User: "Check this API endpoint for security vulnerabilities"

Claude: "I'll analyze this API endpoint for security issues.

**Security Analysis:**

1. **SQL Injection** (Critical)
   Line 8: User input directly interpolated into SQL query.

   ```typescript
   // Vulnerable
   const query = `SELECT * FROM products WHERE category = '${req.query.category}'`;

   // Fixed - use parameterized query
   const products = await db.query(
     'SELECT * FROM products WHERE category = ?',
     [req.query.category]
   );
   ```

2. **Missing Input Validation** (High)
   No validation on query parameters.

   ```typescript
   const QuerySchema = z.object({
     category: z.string().max(100).regex(/^[a-zA-Z0-9-]+$/),
     limit: z.coerce.number().int().min(1).max(100).default(20),
   });

   const params = QuerySchema.parse(req.query);
   ```

3. **Missing Authorization** (High)
   Endpoint accessible without authentication.

   ```typescript
   router.get('/products', authenticate, authorize('products:read'), handler);
   ```

4. **No Rate Limiting** (Medium)
   Endpoint can be abused for denial of service.

**Recommended Secure Implementation:**

```typescript
const QuerySchema = z.object({
  category: z.string().max(100).regex(/^[a-zA-Z0-9-]+$/),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  offset: z.coerce.number().int().min(0).default(0),
});

router.get('/products',
  rateLimit({ windowMs: 60000, max: 100 }),
  authenticate,
  async (req, res) => {
    const params = QuerySchema.safeParse(req.query);
    if (!params.success) {
      return res.status(400).json({ error: 'Invalid parameters' });
    }

    const products = await db.select()
      .from(productsTable)
      .where(eq(productsTable.category, params.data.category))
      .limit(params.data.limit)
      .offset(params.data.offset);

    res.json({ products });
  }
);
```"
```

## Security Review Questions

Ask these questions during review:

### Data Flow
- Where does this data come from?
- Is it trusted or untrusted?
- How is it validated?
- Where does it go?
- Who can access it?

### Authentication
- How are users authenticated?
- How are sessions managed?
- What happens on logout?
- How is password reset handled?

### Authorization
- What permissions are required?
- Is ownership verified?
- Are there privilege escalation paths?
- What happens if authorization fails?

### Error Handling
- What information is exposed in errors?
- Are errors logged appropriately?
- Does the system fail securely?

### Cryptography
- What algorithms are used?
- Are keys managed securely?
- Is data encrypted in transit and at rest?
- Are random values cryptographically secure?

## Post-Review Actions

1. **Document findings** with severity and location
2. **Provide fix suggestions** with code examples
3. **Track remediation** until issues are resolved
4. **Verify fixes** don't introduce new issues
5. **Update security tests** to catch similar issues
6. **Share learnings** with the team
