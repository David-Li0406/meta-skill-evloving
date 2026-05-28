# React Security Patterns

**Category**: code-security/framework-security/react
**Description**: Security vulnerabilities and secure coding patterns for React applications
**CWE**: CWE-79, CWE-200, CWE-522, CWE-352, CWE-639

---

## Overview

React applications face unique security challenges related to XSS, state management, and third-party dependencies.

---

## XSS Patterns

### DangerouslySetInnerHTML
**Pattern**: `dangerouslySetInnerHTML\s*=\s*\{\s*\{\s*__html\s*:`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, jsx, tsx]
- Using dangerouslySetInnerHTML without sanitization
- CWE-79: Cross-site Scripting

### DangerouslySetInnerHTML with Props
**Pattern**: `dangerouslySetInnerHTML\s*=\s*\{\s*\{\s*__html\s*:\s*(?:props|this\.props)`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, jsx, tsx]
- Props directly in dangerouslySetInnerHTML
- CWE-79: Cross-site Scripting

### Href with Props
**Pattern**: `href\s*=\s*\{\s*(?:props|this\.props)\.\w+\s*\}`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, jsx, tsx]
- User-controlled href (potential javascript: XSS)
- CWE-79: Cross-site Scripting

### Eval with State
**Pattern**: `eval\s*\(\s*(?:this\.)?state\.`
**Type**: regex
**Severity**: critical
**Languages**: [javascript, typescript, jsx, tsx]
- State value in eval
- CWE-94: Code Injection

---

## Sensitive Data Exposure Patterns

### Password in State
**Pattern**: `(?:password|secret|token)\s*:\s*['"][^'"]+['"]`
**Type**: regex
**Severity**: high
**Context**: react-state
- Sensitive data in Redux/state (visible in DevTools)
- CWE-200: Information Exposure

### API Key in Frontend
**Pattern**: `(?:REACT_APP_|process\.env\.)(?:\w*(?:SECRET|PRIVATE|KEY)\w*)`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript, jsx, tsx]
- Secret exposed in frontend bundle
- CWE-200: Information Exposure

### Console Log Sensitive
**Pattern**: `console\.log\s*\([^)]*(?:password|token|secret|key)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, jsx, tsx]
- Sensitive data logged to console
- CWE-200: Information Exposure

---

## Token Storage Patterns

### LocalStorage Token
**Pattern**: `localStorage\.setItem\s*\(\s*['"](?:token|jwt|auth|session)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, jsx, tsx]
- Token stored in localStorage (XSS accessible)
- CWE-922: Insecure Storage

### SessionStorage Token
**Pattern**: `sessionStorage\.setItem\s*\(\s*['"](?:token|jwt|auth)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, jsx, tsx]
- Token stored in sessionStorage (XSS accessible)
- CWE-922: Insecure Storage

---

## Authorization Patterns

### Client-Side Only Auth Check
**Pattern**: `if\s*\(\s*!?(?:user|auth|isAdmin|isAuthenticated)\s*\)\s*(?:return|navigate)`
**Type**: regex
**Severity**: low
**Languages**: [javascript, typescript, jsx, tsx]
- Frontend-only authorization check (backend must also verify)
- CWE-639: Authorization Bypass

### Direct Object Reference
**Pattern**: `useParams\s*\(\s*\).*fetch\s*\([^)]*\$\{.*Id\}`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, jsx, tsx]
- URL parameter used directly in API call
- CWE-639: Authorization Bypass (IDOR)

---

## CSRF Patterns

### Missing CSRF Header
**Pattern**: `fetch\s*\(\s*['"][^'"]*['"],\s*\{[^}]*method\s*:\s*['"]POST['"][^}]*\}\s*\)(?![\s\S]*X-CSRF)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, jsx, tsx]
- POST request without CSRF token
- CWE-352: Cross-Site Request Forgery

### Form Without CSRF
**Pattern**: `<form[^>]*method\s*=\s*['"]post['"][^>]*>(?![\s\S]*csrf)`
**Type**: regex
**Severity**: medium
**Languages**: [javascript, typescript, jsx, tsx]
- Form POST without CSRF token
- CWE-352: Cross-Site Request Forgery

---

## Dependency Patterns

### Outdated React
**Pattern**: `"react"\s*:\s*"[<^~]?1[0-6]\.\d+\.\d+"`
**Type**: regex
**Severity**: medium
**Context**: package.json
- Potentially outdated React version
- CWE-1104: Use of Unmaintained Components

---

## Code Examples

### XSS - Vulnerable vs Secure

```jsx
// VULNERABLE - XSS via dangerouslySetInnerHTML
function Comment({ html }) {
  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}

// SECURE - Use DOMPurify for sanitization
import DOMPurify from 'dompurify';

function Comment({ html }) {
  const sanitized = DOMPurify.sanitize(html);
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// BEST - Avoid dangerouslySetInnerHTML entirely
function Comment({ text }) {
  return <div>{text}</div>;  // React escapes by default
}
```

### URL Injection - Vulnerable vs Secure

```jsx
// VULNERABLE - javascript: protocol XSS
function Link({ url, text }) {
  return <a href={url}>{text}</a>;
}

// SECURE - Validate URL protocol
function Link({ url, text }) {
  const isValidUrl = (u) => {
    try {
      const parsed = new URL(u);
      return ['http:', 'https:'].includes(parsed.protocol);
    } catch {
      return false;
    }
  };

  return <a href={isValidUrl(url) ? url : '#'}>{text}</a>;
}
```

### Token Storage - Vulnerable vs Secure

```jsx
// VULNERABLE - Token in localStorage (XSS accessible)
localStorage.setItem('token', response.token);

// BETTER - HttpOnly cookie (server-side)
// The token should be set via Set-Cookie header with HttpOnly flag
// React just makes authenticated requests, doesn't handle token storage

// If localStorage is required, consider:
// 1. Short-lived access tokens
// 2. Token refresh mechanism
// 3. Proper CSP headers to mitigate XSS
```

---

## Security Best Practices

### Content Security Policy

```jsx
// In your server or meta tag
<meta
  httpEquiv="Content-Security-Policy"
  content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
/>
```

### Form Handling with CSRF

```jsx
// SECURE - CSRF protection with tokens
function LoginForm() {
  const [csrfToken, setCsrfToken] = useState('');

  useEffect(() => {
    fetch('/api/csrf-token')
      .then(r => r.json())
      .then(d => setCsrfToken(d.token));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('/api/login', {
      method: 'POST',
      headers: {
        'X-CSRF-Token': csrfToken,
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(formData)
    });
  };
}
```

### Environment Variables

```jsx
// VULNERABLE - Exposing sensitive keys
const API_KEY = process.env.REACT_APP_SECRET_API_KEY;
// All REACT_APP_ vars are bundled into client code!

// SECURE - Only expose public keys
const PUBLIC_KEY = process.env.REACT_APP_PUBLIC_KEY;
// Keep secrets server-side only
```

---

## React Security Checklist

- [ ] No dangerouslySetInnerHTML without sanitization
- [ ] URL/href values validated
- [ ] No sensitive data in state/localStorage
- [ ] CSRF tokens on forms/API calls
- [ ] Backend authorization (not just frontend)
- [ ] Dependencies regularly audited
- [ ] CSP headers configured
- [ ] No secrets in REACT_APP_ variables
- [ ] Error boundaries don't expose details

---

## References

- [React Security Best Practices](https://react.dev/learn/keeping-components-pure)
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
