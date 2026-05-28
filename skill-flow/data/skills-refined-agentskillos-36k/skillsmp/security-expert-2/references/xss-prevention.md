# XSS Prevention Reference (React/TypeScript)

## Table of Contents
1. [XSS Types](#xss-types)
2. [React Built-in Protection](#react-protection)
3. [Dangerous Patterns](#dangerous-patterns)
4. [Sanitization Libraries](#sanitization)
5. [URL and Attribute Handling](#url-handling)
6. [Content Security Policy](#csp)
7. [Testing for XSS](#testing)

## XSS Types {#xss-types}

### Reflected XSS
Malicious script in URL/request reflected back in response.

### Stored XSS
Malicious script saved in database, executed when other users view content.

### DOM-Based XSS
Client-side JavaScript processes untrusted data, modifies DOM unsafely.

```typescript
// Vulnerable: URL hash directly inserted into DOM
document.getElementById('content').innerHTML = location.hash.slice(1);
```

## React Built-in Protection {#react-protection}

### JSX Auto-Escaping
React automatically escapes values embedded in JSX:

```tsx
// SAFE: React escapes the content automatically
function UserGreeting({ name }: { name: string }) {
  return <div>Hello, {name}!</div>;
}

// SAFE: Dynamic attributes are also escaped
function UserLink({ url, label }: { url: string; label: string }) {
  return <a href={url}>{label}</a>;
}

// SAFE: Array rendering
function CommentList({ comments }: { comments: string[] }) {
  return (
    <ul>
      {comments.map((comment, i) => (
        <li key={i}>{comment}</li>
      ))}
    </ul>
  );
}
```

### What React Escapes
- Text content between tags: `<div>{userInput}</div>`
- Attribute values: `<div title={userInput}>`
- Children passed to components

### What React Does NOT Escape
- `href` with `javascript:` protocol
- Event handlers (if you somehow pass user strings)
- Anything using the unsafe HTML API

## Dangerous Patterns {#dangerous-patterns}

### Setting innerHTML Unsafely

When you MUST render HTML (e.g., CMS content), always sanitize first:

```tsx
import DOMPurify from 'dompurify';

// SAFE: Sanitized before rendering
function RichContent({ html }: { html: string }) {
  const sanitized = DOMPurify.sanitize(html);
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}
```

**NEVER** use dangerouslySetInnerHTML with unsanitized user content.

### Direct DOM Manipulation

```tsx
// VULNERABLE: Using refs to set innerHTML directly
// SAFE alternative: Use React's normal rendering
function GoodComponent({ content }: { content: string }) {
  return <div>{content}</div>;  // Auto-escaped
}
```

### Code Execution APIs

**NEVER** use these with user input:
- `eval()`
- `Function()` constructor
- `setTimeout/setInterval` with string arguments

```tsx
// SAFE: Use a proper expression parser for math
import { evaluate } from 'mathjs';

function SafeCalculator({ expression }: { expression: string }) {
  try {
    const result = evaluate(expression);
    return <div>{result}</div>;
  } catch {
    return <div>Invalid expression</div>;
  }
}
```

### Dynamic Script/Style Injection

**NEVER** create script elements with user-provided content.
**NEVER** inject user CSS without strict sanitization.

## Sanitization Libraries {#sanitization}

### DOMPurify
The gold standard for HTML sanitization:

```tsx
import DOMPurify from 'dompurify';

// Basic sanitization
const clean = DOMPurify.sanitize(dirty);

// Configure allowed tags/attributes
const clean = DOMPurify.sanitize(dirty, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
  ALLOWED_ATTR: ['href', 'title'],
});

// Strip all HTML, keep text only
const textOnly = DOMPurify.sanitize(dirty, { ALLOWED_TAGS: [] });
```

### Rich Text Editor Pattern
```tsx
import DOMPurify from 'dompurify';

interface RichTextProps {
  content: string;
  allowImages?: boolean;
}

function RichText({ content, allowImages = false }: RichTextProps) {
  const config = {
    ALLOWED_TAGS: [
      'p', 'br', 'b', 'i', 'em', 'strong', 'a', 'ul', 'ol', 'li',
      'blockquote', 'code', 'pre', 'h1', 'h2', 'h3',
      ...(allowImages ? ['img'] : []),
    ],
    ALLOWED_ATTR: ['href', 'title', 'alt', 'src'],
    ALLOW_DATA_ATTR: false,
  };

  const sanitized = DOMPurify.sanitize(content, config);

  return (
    <div
      className="rich-text"
      dangerouslySetInnerHTML={{ __html: sanitized }}
    />
  );
}
```

### Markdown Rendering
```tsx
import { marked } from 'marked';
import DOMPurify from 'dompurify';

function MarkdownContent({ markdown }: { markdown: string }) {
  const rawHtml = marked(markdown);
  const cleanHtml = DOMPurify.sanitize(rawHtml);

  return <div dangerouslySetInnerHTML={{ __html: cleanHtml }} />;
}
```

## URL and Attribute Handling {#url-handling}

### javascript: Protocol Attacks

React does NOT block javascript: URLs automatically. Always validate:

```tsx
function sanitizeUrl(url: string): string {
  try {
    const parsed = new URL(url, window.location.origin);
    if (!['http:', 'https:', 'mailto:'].includes(parsed.protocol)) {
      return '#';
    }
    return url;
  } catch {
    if (url.startsWith('/') && !url.startsWith('//')) {
      return url;
    }
    return '#';
  }
}

// SAFE: Validate URL protocol
function SafeLink({ url, label }: { url: string; label: string }) {
  const safeUrl = sanitizeUrl(url);
  return <a href={safeUrl}>{label}</a>;
}
```

### Comprehensive URL Validation
```tsx
const ALLOWED_PROTOCOLS = ['http:', 'https:', 'mailto:', 'tel:'];

function validateUrl(input: string): string | null {
  if (!input?.trim()) return null;

  // Block data: URLs (can contain scripts)
  if (input.toLowerCase().startsWith('data:')) return null;

  // Block javascript: (case-insensitive, with possible whitespace)
  if (/^\s*javascript:/i.test(input)) return null;

  try {
    const url = new URL(input, window.location.origin);
    if (!ALLOWED_PROTOCOLS.includes(url.protocol)) {
      return null;
    }
    return input;
  } catch {
    if (input.startsWith('/') && !input.startsWith('//')) {
      return input;
    }
    return null;
  }
}

function UserLink({ href, children }: { href: string; children: React.ReactNode }) {
  const safeHref = validateUrl(href) ?? '#';
  return <a href={safeHref}>{children}</a>;
}
```

### Image Sources
```tsx
function validateImageUrl(url: string): string | null {
  try {
    const parsed = new URL(url, window.location.origin);
    if (parsed.protocol !== 'https:' && parsed.origin !== window.location.origin) {
      return null;
    }
    const allowedDomains = ['cdn.example.com', 'images.example.com'];
    if (parsed.origin !== window.location.origin &&
        !allowedDomains.includes(parsed.hostname)) {
      return null;
    }
    return url;
  } catch {
    return null;
  }
}

function UserAvatar({ src, alt }: { src: string; alt: string }) {
  const safeSrc = validateImageUrl(src) ?? '/default-avatar.png';
  return <img src={safeSrc} alt={alt} />;
}
```

## Content Security Policy {#csp}

### Why CSP?
Defense-in-depth layer. Even if XSS bypasses other protections, CSP can prevent script execution.

### Next.js CSP Configuration
```tsx
// next.config.js
const cspHeader = `
  default-src 'self';
  script-src 'self' 'nonce-{nonce}';
  style-src 'self' 'unsafe-inline';
  img-src 'self' https://cdn.example.com data:;
  font-src 'self';
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
`;

module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: cspHeader.replace(/\n/g, ''),
          },
        ],
      },
    ];
  },
};
```

### Nonce-Based CSP (Next.js 13+)
```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64');
  const csp = `
    default-src 'self';
    script-src 'self' 'nonce-${nonce}' 'strict-dynamic';
    style-src 'self' 'nonce-${nonce}';
    img-src 'self' data: https:;
    font-src 'self';
    connect-src 'self';
    frame-ancestors 'none';
  `.replace(/\n/g, '');

  const response = NextResponse.next();
  response.headers.set('Content-Security-Policy', csp);
  response.headers.set('x-nonce', nonce);
  return response;
}

// app/layout.tsx
import { headers } from 'next/headers';
import Script from 'next/script';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const nonce = headers().get('x-nonce') ?? '';

  return (
    <html>
      <head>
        <Script nonce={nonce} src="/analytics.js" />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### CSP Directives Reference
| Directive | Purpose |
|-----------|---------|
| `default-src` | Fallback for other directives |
| `script-src` | JavaScript sources |
| `style-src` | CSS sources |
| `img-src` | Image sources |
| `connect-src` | XHR, fetch, WebSocket |
| `frame-ancestors` | Who can embed this page |
| `form-action` | Form submission targets |
| `base-uri` | Restrict `<base>` tag |

### Report-Only Mode for Testing
```typescript
headers: [
  {
    key: 'Content-Security-Policy-Report-Only',
    value: cspHeader,
  },
  {
    key: 'Report-To',
    value: '{"group":"csp","endpoints":[{"url":"/api/csp-report"}]}',
  },
]
```

## Testing for XSS {#testing}

### Manual Test Payloads
```
<script>alert('xss')</script>
<img src=x onerror=alert('xss')>
<svg onload=alert('xss')>
javascript:alert('xss')
<a href="javascript:alert('xss')">click</a>
<div onmouseover="alert('xss')">hover</div>
```

### Unit Tests
```tsx
import { render, screen } from '@testing-library/react';
import { RichText, sanitizeUrl } from './security';

describe('XSS Prevention', () => {
  it('should escape script tags in JSX', () => {
    render(<div data-testid="content">{'<script>alert("xss")</script>'}</div>);
    const content = screen.getByTestId('content');
    expect(content.innerHTML).not.toContain('<script>');
    expect(content.textContent).toContain('<script>');
  });

  it('should sanitize HTML content', () => {
    const dirty = '<img src=x onerror=alert("xss")><p>Safe content</p>';
    render(<RichText content={dirty} />);
    const content = screen.getByText('Safe content');
    expect(content.parentElement?.innerHTML).not.toContain('onerror');
  });

  it('should block javascript: URLs', () => {
    expect(sanitizeUrl('javascript:alert(1)')).toBe('#');
    expect(sanitizeUrl('JAVASCRIPT:alert(1)')).toBe('#');
  });

  it('should allow safe URLs', () => {
    expect(sanitizeUrl('https://example.com')).toBe('https://example.com');
    expect(sanitizeUrl('/relative/path')).toBe('/relative/path');
  });
});
```

### Integration Tests
```tsx
import { test, expect } from '@playwright/test';

test('XSS payload in search should be escaped', async ({ page }) => {
  await page.goto('/search?q=<script>alert(1)</script>');

  const dialogPromise = page.waitForEvent('dialog', { timeout: 1000 });
  await expect(dialogPromise).rejects.toThrow();

  await expect(page.locator('.search-query')).toContainText('<script>');
});
```

### Automated Scanning
```bash
# Run OWASP ZAP against local dev server
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://host.docker.internal:3000

# Use semgrep for static analysis
npx @semgrep/semgrep --config=p/react
```

## Quick Reference

### Always Safe
- Normal JSX: `<div>{userInput}</div>`
- React state rendering
- Props passed to components

### Requires Sanitization
- Rendering user-provided HTML
- Markdown content
- Rich text from CMS

### Always Validate
- User-controlled `href` attributes
- Image/iframe `src` attributes
- Any URL from user input

### Never Do
- Code execution APIs with user input
- innerHTML without sanitization
- `javascript:` URLs
- Creating scripts from user content

### Defense Layers
1. **Primary**: React's auto-escaping
2. **Sanitization**: DOMPurify for HTML content
3. **URL validation**: Block dangerous protocols
4. **CSP**: Prevent inline script execution
5. **Testing**: Automated XSS payload testing
