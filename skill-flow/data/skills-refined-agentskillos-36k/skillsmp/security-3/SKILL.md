---
name: security
description: Write secure web pages and applications. Use when handling user input, forms, external resources, authentication, or implementing security headers and CSP.
allowed-tools: Read, Write, Edit
---

# Security Skill

This skill ensures web pages and applications follow security best practices to prevent common vulnerabilities.

## OWASP Top 10 Awareness

Key vulnerabilities this skill helps prevent:

| Vulnerability | Prevention |
|---------------|------------|
| Injection (XSS, SQL) | Input validation, output encoding, CSP |
| Broken Authentication | Secure forms, HTTPS, secure cookies |
| Sensitive Data Exposure | HTTPS, secure headers, no secrets in HTML |
| Security Misconfiguration | Proper headers, CSP, secure defaults |
| Cross-Site Scripting (XSS) | CSP, output encoding, input validation |
| Insecure Deserialization | Validate all input, avoid eval() |
| Using Vulnerable Components | SRI for external resources |
| Insufficient Logging | Error handling without exposure |

## HTTPS and Transport Security

### Require HTTPS

All production sites MUST use HTTPS:

```html
<head>
  <!-- Upgrade insecure requests -->
  <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests"/>

  <!-- Only use HTTPS URLs -->
  <link rel="stylesheet" href="https://example.com/styles.css"/>
  <script src="https://example.com/script.js"></script>
</head>
```

### Avoid Mixed Content

Never load HTTP resources on HTTPS pages:

```html
<!-- BAD: Mixed content (blocked by browsers) -->
<img src="http://example.com/image.jpg"/>
<script src="http://cdn.example.com/lib.js"></script>

<!-- GOOD: Always use HTTPS -->
<img src="https://example.com/image.jpg" alt="Description"/>
<script src="https://cdn.example.com/lib.js"></script>

<!-- GOOD: Protocol-relative (inherits page protocol) -->
<img src="//example.com/image.jpg" alt="Description"/>
```

## Security Headers

### Essential Headers (Server Configuration)

Document required headers in HTML comments for server configuration:

```html
<!--
  Required Security Headers (configure on server):

  # Prevent clickjacking
  X-Frame-Options: DENY

  # Prevent MIME sniffing
  X-Content-Type-Options: nosniff

  # Enable XSS filter (legacy browsers)
  X-XSS-Protection: 1; mode=block

  # Control referrer information
  Referrer-Policy: strict-origin-when-cross-origin

  # Enforce HTTPS
  Strict-Transport-Security: max-age=31536000; includeSubDomains

  # Permissions policy
  Permissions-Policy: geolocation=(), camera=(), microphone=()
-->
```

### Meta Tag Equivalents

Some headers can be set via meta tags:

```html
<head>
  <!-- Referrer policy -->
  <meta name="referrer" content="strict-origin-when-cross-origin"/>

  <!-- Content Security Policy (limited) -->
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'"/>

  <!-- Prevent caching of sensitive pages -->
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta http-equiv="Pragma" content="no-cache"/>
</head>
```

## Content Security Policy (CSP)

### Basic CSP

Start with a restrictive policy:

```html
<head>
  <meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self';
    style-src 'self';
    img-src 'self' data:;
    font-src 'self';
    connect-src 'self';
    frame-ancestors 'none';
    form-action 'self';
    base-uri 'self';
  "/>
</head>
```

### CSP Directives Reference

| Directive | Purpose | Example |
|-----------|---------|---------|
| `default-src` | Fallback for all resource types | `'self'` |
| `script-src` | JavaScript sources | `'self' https://cdn.example.com` |
| `style-src` | CSS sources | `'self' 'unsafe-inline'` |
| `img-src` | Image sources | `'self' data: https:` |
| `font-src` | Font sources | `'self' https://fonts.gstatic.com` |
| `connect-src` | XHR, WebSocket, fetch | `'self' https://api.example.com` |
| `frame-src` | iframe sources | `'none'` |
| `frame-ancestors` | Who can embed this page | `'none'` |
| `form-action` | Form submission targets | `'self'` |
| `base-uri` | Restrict `<base>` element | `'self'` |
| `object-src` | Plugins (Flash, etc.) | `'none'` |

### CSP Source Values

| Value | Meaning |
|-------|---------|
| `'self'` | Same origin only |
| `'none'` | Block all |
| `'unsafe-inline'` | Allow inline (avoid if possible) |
| `'unsafe-eval'` | Allow eval() (avoid) |
| `'nonce-{random}'` | Allow specific inline with nonce |
| `'sha256-{hash}'` | Allow specific inline by hash |
| `https:` | Any HTTPS source |
| `data:` | Data URIs |
| `blob:` | Blob URIs |

### Nonce-Based Scripts

For inline scripts, use nonces (server must generate unique nonce per request):

```html
<head>
  <meta http-equiv="Content-Security-Policy"
        content="script-src 'self' 'nonce-abc123random'"/>
</head>
<body>
  <!-- Allowed: has matching nonce -->
  <script nonce="abc123random">
    console.log('This runs');
  </script>

  <!-- Blocked: no nonce -->
  <script>
    console.log('This is blocked');
  </script>
</body>
```

### Hash-Based Scripts

For static inline scripts, use hashes:

```html
<head>
  <!-- Hash of: console.log('Hello'); -->
  <meta http-equiv="Content-Security-Policy"
        content="script-src 'self' 'sha256-xyz123...'"/>
</head>
<body>
  <script>console.log('Hello');</script>
</body>
```

Generate hash: `echo -n "console.log('Hello');" | openssl sha256 -binary | base64`

## Subresource Integrity (SRI)

### External Resources

Always use SRI for third-party resources:

```html
<!-- External CSS with integrity -->
<link rel="stylesheet"
      href="https://cdn.example.com/lib.css"
      integrity="sha384-abc123..."
      crossorigin="anonymous"/>

<!-- External JavaScript with integrity -->
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-xyz789..."
        crossorigin="anonymous"></script>
```

### Generating SRI Hashes

```bash
# Generate SRI hash for a file
cat file.js | openssl dgst -sha384 -binary | openssl base64 -A

# Or use online tools like srihash.org
```

### When to Use SRI

| Resource | SRI Required? |
|----------|---------------|
| Third-party CDN scripts | **Yes** |
| Third-party CDN styles | **Yes** |
| Self-hosted resources | Optional but recommended |
| Dynamic/frequently updated | Not practical |

## Form Security

### CSRF Protection

Include CSRF tokens in forms:

```html
<form method="post" action="/submit">
  <!-- CSRF token (server-generated) -->
  <input type="hidden" name="_csrf" value="token-from-server"/>

  <!-- Form fields -->
  <input type="text" name="username" autocomplete="username"/>
  <button type="submit">Submit</button>
</form>
```

### Secure Form Attributes

```html
<form method="post"
      action="https://example.com/submit"
      autocomplete="off">

  <!-- Password fields -->
  <input type="password"
         name="password"
         autocomplete="new-password"
         minlength="12"
         required/>

  <!-- Sensitive data -->
  <input type="text"
         name="ssn"
         autocomplete="off"
         inputmode="numeric"
         pattern="[0-9]{9}"/>
</form>
```

### Form Action Security

```html
<!-- GOOD: Explicit HTTPS action -->
<form action="https://example.com/api/submit" method="post">

<!-- BAD: Relative action could be HTTP -->
<form action="/api/submit" method="post">

<!-- BAD: HTTP action -->
<form action="http://example.com/api/submit" method="post">
```

## Input Validation

### Client-Side Validation (Defense in Depth)

Use HTML5 validation attributes:

```html
<form-field>
  <label for="email">Email</label>
  <input type="email"
         id="email"
         name="email"
         required
         pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
         maxlength="254"
         autocomplete="email"/>
  <output for="email"></output>
</form-field>

<form-field>
  <label for="phone">Phone</label>
  <input type="tel"
         id="phone"
         name="phone"
         pattern="[0-9]{10}"
         inputmode="tel"
         autocomplete="tel"/>
  <output for="phone"></output>
</form-field>

<form-field>
  <label for="url">Website</label>
  <input type="url"
         id="url"
         name="url"
         pattern="https://.*"
         placeholder="https://example.com"/>
  <output for="url"></output>
</form-field>
```

### Validation Attributes Reference

| Attribute | Purpose |
|-----------|---------|
| `required` | Field must have value |
| `pattern` | Regex pattern to match |
| `minlength` | Minimum character count |
| `maxlength` | Maximum character count |
| `min` / `max` | Numeric range |
| `type="email"` | Email format validation |
| `type="url"` | URL format validation |
| `type="tel"` | Telephone (no validation, just keyboard) |

### Never Trust Client Validation

```html
<!--
  IMPORTANT: Client-side validation is for UX only!

  Server MUST:
  - Validate all input again
  - Sanitize before storage
  - Encode before output
  - Use parameterized queries
-->
```

### Server-Side Validation with JSON Schema

Use the **validation** skill for comprehensive server-side input validation:

```javascript
import { validateBody } from './middleware/validate.js';

// Validate request body against JSON Schema
app.post('/api/users',
  validateBody('entities/user.create'),
  createUser
);
```

**Key security benefits:**
- `additionalProperties: false` - Rejects unknown fields (prevents mass assignment)
- `removeAdditional: 'all'` - Strips unknown properties before processing
- Strict type checking - Prevents type confusion attacks
- Consistent error format - No information leakage

See the **validation** skill for:
- JSON Schema authoring patterns
- AJV middleware configuration
- Error response formatting
- Schema-to-type generation

## Output Encoding

### Prevent XSS in Dynamic Content

When inserting user data into HTML:

```html
<!-- BAD: Direct insertion (XSS vulnerable) -->
<div id="output"></div>
<script>
  document.getElementById('output').innerHTML = userInput; // DANGEROUS!
</script>

<!-- GOOD: Use textContent for text -->
<div id="output"></div>
<script>
  document.getElementById('output').textContent = userInput; // Safe
</script>

<!-- GOOD: Use data attributes for values -->
<div data-user-id="123">Content</div>
```

### Context-Specific Encoding

| Context | Encoding Method |
|---------|-----------------|
| HTML body | HTML entity encode (`&lt;`, `&gt;`, `&amp;`) |
| HTML attributes | Attribute encode + quote |
| JavaScript | JavaScript encode or JSON.stringify |
| URL parameters | encodeURIComponent() |
| CSS | CSS encode |

## Secure Links

### External Links

```html
<!-- Add rel="noopener" for security -->
<a href="https://external-site.com"
   target="_blank"
   rel="noopener noreferrer">
  External Link
</a>
```

### Why `rel="noopener"`?

Without it, the opened page can access `window.opener` and potentially:
- Redirect your page to a phishing site
- Access some properties of your page

### Link Security Attributes

| Attribute | Purpose |
|-----------|---------|
| `rel="noopener"` | Prevent window.opener access |
| `rel="noreferrer"` | Don't send referrer header |
| `rel="nofollow"` | Don't pass SEO value (user content) |

```html
<!-- User-generated content: use all three -->
<a href="https://user-submitted-url.com"
   target="_blank"
   rel="noopener noreferrer nofollow">
  User Link
</a>
```

## Clickjacking Prevention

### Frame Options

```html
<!--
  Server header (preferred):
  X-Frame-Options: DENY

  Or via CSP:
-->
<meta http-equiv="Content-Security-Policy" content="frame-ancestors 'none'"/>
```

### Frame-Busting (Legacy Fallback)

```html
<head>
  <style>
    /* Hide page if framed (fallback) */
    html { display: none; }
  </style>
  <script>
    if (self === top) {
      document.documentElement.style.display = 'block';
    } else {
      top.location = self.location;
    }
  </script>
</head>
```

## Sensitive Data Handling

### Never Expose Secrets in HTML

```html
<!-- BAD: API keys in HTML -->
<script>
  const API_KEY = 'sk-secret123'; // NEVER DO THIS!
</script>

<!-- BAD: Secrets in data attributes -->
<div data-api-key="sk-secret123">

<!-- GOOD: Use server-side proxy for API calls -->
<form action="/api/proxy" method="post">
```

### Password Fields

```html
<input type="password"
       name="password"
       autocomplete="current-password"
       minlength="12"
       aria-describedby="password-requirements"/>
<p id="password-requirements">
  Minimum 12 characters with mixed case, numbers, and symbols.
</p>
```

### Sensitive Form Data

```html
<!-- Prevent autocomplete on sensitive fields -->
<input type="text"
       name="credit-card"
       autocomplete="cc-number"
       inputmode="numeric"
       pattern="[0-9]{16}"/>

<!-- Prevent browser caching of sensitive pages -->
<meta http-equiv="Cache-Control" content="no-store"/>
```

## Cookie Security

### Secure Cookie Attributes

Document required cookie attributes:

```html
<!--
  Cookie Security (set via server):

  Set-Cookie: session=abc123;
    Secure;           # HTTPS only
    HttpOnly;         # No JavaScript access
    SameSite=Strict;  # CSRF protection
    Path=/;           # Scope to root
    Max-Age=3600;     # 1 hour expiry

  Authentication cookies MUST have:
  - Secure (HTTPS only)
  - HttpOnly (prevent XSS theft)
  - SameSite=Strict or Lax (CSRF protection)
-->
```

### SameSite Values

| Value | Behavior |
|-------|----------|
| `Strict` | Cookie only sent for same-site requests |
| `Lax` | Sent for same-site + top-level navigation |
| `None` | Sent for all requests (requires Secure) |

## JavaScript Security

### Safe DOM Manipulation

```javascript
// BAD: innerHTML with user data
element.innerHTML = userInput;

// GOOD: textContent for text
element.textContent = userInput;

// GOOD: createElement for structure
const div = document.createElement('div');
div.textContent = userInput;
parent.appendChild(div);

// GOOD: Template with encoded values
const template = document.getElementById('item-template');
const clone = template.content.cloneNode(true);
clone.querySelector('.name').textContent = userName;
```

### Avoid Dangerous Functions

```javascript
// NEVER USE with user input:
eval(userInput);                    // Code execution
new Function(userInput);            // Code execution
setTimeout(userInput, 1000);        // If string, same as eval
setInterval(userInput, 1000);       // If string, same as eval
element.innerHTML = userInput;      // XSS
document.write(userInput);          // XSS
location.href = userInput;          // Open redirect
```

### URL Validation

```javascript
// Validate URLs before use
function isValidHttpUrl(string) {
  try {
    const url = new URL(string);
    return url.protocol === 'https:' || url.protocol === 'http:';
  } catch {
    return false;
  }
}

// Prevent javascript: URLs
function isSafeUrl(string) {
  try {
    const url = new URL(string, window.location.origin);
    return !url.protocol.startsWith('javascript');
  } catch {
    return false;
  }
}
```

## Error Handling

### Don't Expose Stack Traces

```html
<!-- BAD: Detailed error in HTML -->
<div class="error">
  Error: Cannot read property 'id' of undefined
  at processUser (app.js:123)
  at handleSubmit (app.js:456)
</div>

<!-- GOOD: Generic user-friendly message -->
<div class="error" role="alert">
  <p>Something went wrong. Please try again.</p>
  <p>If the problem persists, contact support.</p>
</div>
```

### Error Logging

```javascript
// Log details server-side, show generic message to user
try {
  await submitForm(data);
} catch (error) {
  // Send to logging service (not console in production)
  logError({ error, context: 'form-submit', timestamp: Date.now() });

  // Show generic message to user
  showError('Unable to submit form. Please try again.');
}
```

## Security Checklist

Before deploying:

### Transport
- [ ] Site uses HTTPS exclusively
- [ ] No mixed content (HTTP resources on HTTPS page)
- [ ] HSTS header configured (server-side)

### Headers
- [ ] Content-Security-Policy defined
- [ ] X-Frame-Options or frame-ancestors set
- [ ] X-Content-Type-Options: nosniff
- [ ] Referrer-Policy configured

### Resources
- [ ] External scripts have SRI integrity attributes
- [ ] External styles have SRI integrity attributes
- [ ] No inline scripts (or use nonces/hashes)

### Forms
- [ ] CSRF tokens included
- [ ] Form actions use HTTPS
- [ ] Input validation attributes set
- [ ] Autocomplete appropriate for field type

### Links
- [ ] External links have `rel="noopener noreferrer"`
- [ ] User-generated links have `rel="nofollow"` too
- [ ] No `javascript:` URLs

### Data
- [ ] No secrets in HTML source
- [ ] No sensitive data in URLs
- [ ] Appropriate cache headers for sensitive pages
- [ ] Error messages don't expose system details

### JavaScript
- [ ] No eval() or equivalent with user input
- [ ] textContent used instead of innerHTML for user data
- [ ] URLs validated before use

## Related Skills

| Skill | Security Overlap |
|-------|------------------|
| `validation` | Server-side input validation with JSON Schema |
| `forms` | Client-side form validation, autocomplete |
| `javascript-author` | Safe DOM manipulation |
| `metadata` | Security meta tags |
| `performance` | Resource loading (SRI compatible) |

## Common Mistakes

| Mistake | Risk | Solution |
|---------|------|----------|
| HTTP resources | Mixed content blocked | Use HTTPS everywhere |
| No SRI on CDN scripts | Supply chain attack | Add integrity attribute |
| innerHTML with user data | XSS | Use textContent |
| Missing CSRF token | CSRF attacks | Include token in forms |
| target="_blank" without rel | Tab nabbing | Add rel="noopener" |
| Secrets in HTML | Credential theft | Use server-side proxy |
| Detailed error messages | Information disclosure | Generic messages |
| No CSP | XSS easier to exploit | Implement CSP |
