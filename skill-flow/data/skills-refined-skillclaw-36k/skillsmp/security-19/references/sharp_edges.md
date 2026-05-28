# Security - Sharp Edges

## Sql Injection String Concat

### **Id**
sql-injection-string-concat
### **Summary**
Building SQL queries with string concatenation
### **Severity**
critical
### **Situation**
  "SELECT * FROM users WHERE id = " + userId. Attacker sends
  "1; DROP TABLE users; --". Database gone. Company gone.
  
### **Why**
  String concatenation treats user input as SQL code. Attackers can inject
  arbitrary SQL commands. This is the #1 way databases get compromised.
  Parameterized queries exist specifically to prevent this.
  
### **Solution**
  # Never concatenate:
  ```typescript
  // BAD - SQL injection
  const query = `SELECT * FROM users WHERE id = ${userId}`;
  
  // GOOD - Parameterized query
  const { data } = await supabase
    .from('users')
    .select('*')
    .eq('id', userId);
  
  // GOOD - Parameterized with raw SQL
  const result = await db.query(
    'SELECT * FROM users WHERE id = $1',
    [userId]
  );
  ```
  
  # ORMs are safer:
  Supabase, Prisma, Drizzle all parameterize by default
  Only danger is raw SQL queries
  
  # Test yourself:
  Try inputting: ' OR '1'='1
  If it works, you're vulnerable
  
### **Symptoms**
  - String concatenation in SQL
  - Template literals with user input in queries
  - Raw SQL queries with variables
### **Detection Pattern**
SELECT.*\$\{|INSERT.*\$\{|UPDATE.*\$\{|DELETE.*\$\{

## Xss Unescaped Output

### **Id**
xss-unescaped-output
### **Summary**
Rendering user input without escaping
### **Severity**
critical
### **Situation**
  User submits comment with <script>alert('xss')</script>. Other users view
  the comment. Script executes in their browsers. Attacker steals sessions.
  
### **Why**
  User input in HTML can include JavaScript. If you render it unescaped,
  the browser executes it. XSS allows session hijacking, defacement, and
  worse. React escapes by default, but dangerouslySetInnerHTML bypasses it.
  
### **Solution**
  # React escapes by default:
  ```typescript
  // SAFE - React escapes this
  return <div>{userInput}</div>;
  
  // DANGEROUS - Bypasses escaping
  return <div dangerouslySetInnerHTML={{ __html: userInput }} />;
  ```
  
  # If you must render HTML:
  ```typescript
  import DOMPurify from 'dompurify';
  const clean = DOMPurify.sanitize(userInput);
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
  ```
  
  # URLs also need checking:
  ```typescript
  // BAD - javascript: URLs execute code
  <a href={userUrl}>Link</a>
  
  // GOOD - Validate URL protocol
  const safeUrl = userUrl.startsWith('https://') ? userUrl : '#';
  ```
  
### **Symptoms**
  - dangerouslySetInnerHTML with user input
  - innerHTML assignment
  - User input in href without validation
### **Detection Pattern**
dangerouslySetInnerHTML.*\{.*__html.*[^sanitize]

## Secrets In Code

### **Id**
secrets-in-code
### **Summary**
Hardcoding API keys, passwords, or secrets in source code
### **Severity**
critical
### **Situation**
  API key in JavaScript file. Pushed to GitHub. Bot scrapes it in seconds.
  AWS bill: $50,000. Or database password exposed. Full breach.
  
### **Why**
  Code is not secret. It goes to version control, build systems, browsers.
  Hardcoded secrets become public secrets. Bots constantly scan for them.
  
### **Solution**
  # Never in code:
  ```typescript
  // BAD
  const API_KEY = 'sk_live_abc123';
  
  // GOOD
  const API_KEY = process.env.API_KEY;
  ```
  
  # For client-side:
  Only use publishable/public keys
  NEXT_PUBLIC_ prefix = exposed to client
  
  # Environment structure:
  - .env.local for development (gitignored)
  - Environment variables in hosting (Vercel, etc.)
  - Never commit .env files with secrets
  
  # If you already committed a secret:
  - Revoke it immediately
  - Rotate to new secret
  - It's already compromised
  
### **Symptoms**
  - API keys in JavaScript/TypeScript files
  - Passwords in config files
  - .env files in git
### **Detection Pattern**
sk_live_|sk_test_|password.*=.*['"][^'"]{8,}['"]|api_key.*=.*['"][^'"]{16,}['"]

## Csrf Missing Protection

### **Id**
csrf-missing-protection
### **Summary**
State-changing operations without CSRF protection
### **Severity**
high
### **Situation**
  User logged in to your app. Visits malicious site. Site submits form to
  your API. Browser sends auth cookie. Action executes as user.
  
### **Why**
  Browsers send cookies automatically. Malicious sites can trigger requests
  to your origin. Without CSRF protection, any logged-in user can be tricked
  into taking actions.
  
### **Solution**
  # For same-origin APIs:
  SameSite=Strict cookies prevent CSRF
  ```typescript
  res.setHeader('Set-Cookie', 'session=xxx; HttpOnly; Secure; SameSite=Strict');
  ```
  
  # For cross-origin APIs:
  Use tokens in headers (not cookies)
  ```typescript
  // Client sends Authorization header
  fetch('/api/action', {
    headers: { Authorization: `Bearer ${token}` }
  });
  ```
  
  # Check Origin header:
  ```typescript
  if (req.headers.origin !== 'https://yoursite.com') {
    return res.status(403).json({ error: 'Invalid origin' });
  }
  ```
  
  # Mutating operations:
  Use POST/PUT/DELETE, not GET
  GET requests are easier to trigger
  
### **Symptoms**
  - State-changing GET requests
  - Cookies without SameSite
  - No origin checking
### **Detection Pattern**


## Insecure Direct Object Reference

### **Id**
insecure-direct-object-reference
### **Summary**
Not verifying user owns the resource they're accessing
### **Severity**
high
### **Situation**
  GET /api/invoice/123. Returns invoice. User changes to /api/invoice/124.
  Returns someone else's invoice. Full data breach.
  
### **Why**
  Numeric IDs are guessable. Users will try changing them. If you only check
  authentication (who they are) but not authorization (what they can access),
  they can access anything.
  
### **Solution**
  # Always check ownership:
  ```typescript
  // BAD - Only checks authentication
  const invoice = await getInvoice(invoiceId);
  return invoice;
  
  // GOOD - Checks authorization
  const invoice = await getInvoice(invoiceId);
  if (invoice.userId !== currentUser.id) {
    throw new Error('Unauthorized');
  }
  return invoice;
  ```
  
  # Even better - filter in query:
  ```typescript
  const invoice = await db.invoices
    .where({ id: invoiceId, userId: currentUser.id })
    .first();
  if (!invoice) throw new Error('Not found');
  ```
  
  # Use UUIDs instead of sequential IDs:
  Harder to guess, though still need auth checks
  
### **Symptoms**
  - Fetching by ID without ownership check
  - Sequential IDs in URLs
  - If I change the ID, I see other users' data
### **Detection Pattern**


## Missing Rate Limiting

### **Id**
missing-rate-limiting
### **Summary**
No rate limiting on sensitive endpoints
### **Severity**
high
### **Situation**
  Login endpoint. Attacker sends 10,000 password attempts per second.
  Eventually guesses password. Account compromised.
  
### **Why**
  Without rate limiting, attackers can brute force passwords, scrape data,
  or DoS your service. Rate limiting is essential for login, registration,
  password reset, and any expensive operation.
  
### **Solution**
  # Critical endpoints to rate limit:
  - Login: 5 attempts per minute
  - Registration: 3 per hour per IP
  - Password reset: 3 per hour
  - Any expensive operation
  
  # Implementation with Upstash:
  ```typescript
  import { Ratelimit } from '@upstash/ratelimit';
  
  const ratelimit = new Ratelimit({
    limiter: Ratelimit.slidingWindow(5, '1m'),
  });
  
  const { success } = await ratelimit.limit(ip);
  if (!success) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  ```
  
  # Consider:
  - Per-IP limiting
  - Per-user limiting
  - Progressive delays
  - CAPTCHA after failures
  
### **Symptoms**
  - Login with no rate limiting
  - Password reset with no limiting
  - Expensive APIs without protection
### **Detection Pattern**


## Missing Security Headers

### **Id**
missing-security-headers
### **Summary**
Not setting security headers
### **Severity**
medium
### **Situation**
  No Content-Security-Policy. XSS vulnerability is exploited. No X-Frame-Options.
  Site is clickjacked. Missing headers make attacks easier.
  
### **Why**
  Security headers tell browsers how to behave. They prevent many attacks
  by default. Missing headers means the browser allows risky behavior.
  
### **Solution**
  # Essential headers:
  ```typescript
  // next.config.js
  const securityHeaders = [
    {
      key: 'X-Content-Type-Options',
      value: 'nosniff',
    },
    {
      key: 'X-Frame-Options',
      value: 'DENY',
    },
    {
      key: 'X-XSS-Protection',
      value: '1; mode=block',
    },
    {
      key: 'Strict-Transport-Security',
      value: 'max-age=31536000; includeSubDomains',
    },
    {
      key: 'Content-Security-Policy',
      value: "default-src 'self'; script-src 'self'",
    },
  ];
  ```
  
  # Test your headers:
  https://securityheaders.com
  
### **Symptoms**
  - No security headers set
  - Site can be iframed
  - No HSTS
### **Detection Pattern**


## Jwt None Algorithm

### **Id**
jwt-none-algorithm
### **Summary**
Not validating JWT algorithm
### **Severity**
critical
### **Situation**
  JWT signed with RS256. Attacker changes algorithm to "none" in header.
  Server accepts unsigned token. Attacker forges any identity.
  
### **Why**
  JWT "none" algorithm vulnerability is well-known. Libraries sometimes
  accept "none" by default. Attackers can change the alg header and
  forge tokens.
  
### **Solution**
  # Always specify algorithm:
  ```typescript
  import jwt from 'jsonwebtoken';
  
  // BAD - Accepts any algorithm
  jwt.verify(token, secret);
  
  // GOOD - Explicitly specify algorithm
  jwt.verify(token, secret, { algorithms: ['HS256'] });
  ```
  
  # For RS256:
  ```typescript
  jwt.verify(token, publicKey, { algorithms: ['RS256'] });
  ```
  
  # Never accept:
  - "none" algorithm
  - Algorithm from token header
  - Algorithm negotiation
  
### **Symptoms**
  - jwt.verify without algorithms option
  - Token algorithm not validated
  - "none" algorithm accepted
### **Detection Pattern**
jwt\.verify.*(?!algorithms)

## Path Traversal

### **Id**
path-traversal
### **Summary**
User input in file paths without sanitization
### **Severity**
critical
### **Situation**
  Download endpoint: /download?file=report.pdf. Attacker sends
  file=../../../etc/passwd. Server returns system file.
  
### **Why**
  "../" in paths traverses up directories. Without sanitization, attackers
  can read any file on the system. This includes configuration files,
  source code, and sensitive data.
  
### **Solution**
  # Never use user input directly in paths:
  ```typescript
  // BAD
  const filePath = `./uploads/${req.query.file}`;
  
  // GOOD - Validate against whitelist
  const allowedFiles = ['report.pdf', 'invoice.pdf'];
  if (!allowedFiles.includes(req.query.file)) {
    throw new Error('Invalid file');
  }
  
  // GOOD - Use path.basename
  import path from 'path';
  const fileName = path.basename(req.query.file);
  const filePath = path.join('./uploads', fileName);
  ```
  
  # path.basename removes directories:
  ../../../etc/passwd → passwd
  
  # Best: Use IDs, not filenames:
  /download?id=123 → lookup in database
  
### **Symptoms**
  - User input in file paths
  - No path sanitization
  - File downloads by filename
### **Detection Pattern**
path\.join.*req\.|path\.resolve.*req\.

## Mass Assignment

### **Id**
mass-assignment
### **Summary**
Accepting all fields from user input into database
### **Severity**
high
### **Situation**
  Update profile endpoint. User sends { name: 'John', isAdmin: true }.
  Server spreads into database update. User is now admin.
  
### **Why**
  Spreading request body directly into database updates lets users set
  any field, including ones you didn't intend (isAdmin, balance, role).
  This is called mass assignment.
  
### **Solution**
  # Whitelist fields:
  ```typescript
  // BAD - Mass assignment vulnerability
  await db.users.update({
    where: { id: userId },
    data: req.body,  // User controls all fields!
  });
  
  // GOOD - Explicitly pick fields
  const { name, email, bio } = req.body;
  await db.users.update({
    where: { id: userId },
    data: { name, email, bio },  // Only allowed fields
  });
  ```
  
  # With Zod:
  ```typescript
  const UpdateSchema = z.object({
    name: z.string().optional(),
    email: z.string().email().optional(),
    bio: z.string().optional(),
  });
  const data = UpdateSchema.parse(req.body);
  await db.users.update({ where: { id }, data });
  ```
  
### **Symptoms**
  - Spreading request body into updates
  - No field whitelisting
  - Any field can be updated
### **Detection Pattern**
update.*data:.*req\.body|create.*data:.*req\.body

## Http Only Cookie Missing

### **Id**
http-only-cookie-missing
### **Summary**
Session cookies accessible to JavaScript
### **Severity**
high
### **Situation**
  Session cookie without HttpOnly. XSS vulnerability found. Attacker steals
  session cookies via JavaScript. Full session hijacking.
  
### **Why**
  Without HttpOnly, JavaScript can read cookies. XSS becomes session hijacking.
  HttpOnly cookies can only be read by the server, limiting XSS damage.
  
### **Solution**
  # Always use HttpOnly for sessions:
  ```typescript
  res.setHeader('Set-Cookie', [
    'session=xxx; HttpOnly; Secure; SameSite=Strict',
  ]);
  
  // With next-auth or similar:
  // HttpOnly is typically default
  ```
  
  # Cookie flags:
  - HttpOnly: Not accessible to JavaScript
  - Secure: Only sent over HTTPS
  - SameSite=Strict: Not sent cross-origin
  - Path=/: Scope limitation
  
  # For authentication tokens:
  Store in HttpOnly cookies, not localStorage
  localStorage is always accessible to JS
  
### **Symptoms**
  - Session cookie without HttpOnly
  - Token in localStorage
  - document.cookie contains session
### **Detection Pattern**
Set-Cookie.*(?!.*HttpOnly)