---
name: react-security
description: Use this skill when implementing security best practices in React applications to prevent vulnerabilities such as XSS and improper authentication.
---

# React Security

## **Priority: P0 (CRITICAL)**

Preventing vulnerabilities in client-side apps.

## Implementation Guidelines

- **XSS**: Avoid `dangerouslySetInnerHTML`. Sanitize via `DOMPurify` if needed.
- **URLs**: Validate `javascript:` protocols in user links.
- **Auth**: Store tokens in `HttpOnly` cookies. Avoid `localStorage`.
- **Dependencies**: Run `npm audit`. Pin versions.
- **Secrets**: Keep server-side only. Do not include `.env` secrets in the build.
- **CSP**: Implement strict Content-Security-Policy headers.

## Anti-Patterns

- **No `eval()`**: This poses a risk of Remote Code Execution (RCE).
- **No Serialized State**: Avoid injecting JSON into the DOM without proper escaping.
- **No Client Logic for Permissions**: Always validate permissions on the backend.

## Code Examples

```tsx
import DOMPurify from 'dompurify';

// Safe HTML Injection
function SafeHtml({ content }) {
  const clean = DOMPurify.sanitize(content);
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}

// Bad Link Prevention
const safeUrl = url.startsWith('javascript:') ? '#' : url;
<a href={safeUrl}>Link</a>;
```

## Related Topics

common/security-standards | typescript/security | component-patterns