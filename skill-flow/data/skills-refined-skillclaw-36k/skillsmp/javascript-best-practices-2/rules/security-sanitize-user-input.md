---
title: Sanitize User Input Before DOM Insertion
impact: HIGH
impactDescription: Prevents XSS and injection attacks from malicious input
tags: security, sanitization, xss, input
---

## Sanitize User Input Before DOM Insertion

User input can contain malicious scripts, HTML, or unexpected characters. Always sanitize before using in the DOM, URLs, or other sensitive contexts.

**Incorrect (direct insertion of user input):**

```javascript
// URL injection
const redirectUrl = userInput;
window.location.href = redirectUrl; // javascript:alert('xss')

// Attribute injection
element.setAttribute('onclick', userInput);

// Template literal injection
const html = `<a href="${userUrl}">${userName}</a>`;
```

**Correct (sanitized input):**

```javascript
// URL validation
function sanitizeURL(url) {
  try {
    const parsed = new URL(url);
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      return '/fallback';
    }
    return parsed.href;
  } catch {
    return '/fallback';
  }
}

const safeUrl = sanitizeURL(userInput);
window.location.href = safeUrl;

// Use data attributes instead of inline handlers
element.dataset.action = 'click';
element.addEventListener('click', handlers[element.dataset.action]);

// Build DOM safely
const link = document.createElement('a');
link.href = sanitizeURL(userUrl);
link.textContent = userName; // Automatically escaped
```

**For HTML content, use DOMPurify:**

```javascript
import DOMPurify from 'dompurify';

const clean = DOMPurify.sanitize(dirtyHTML, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href']
});
```

Reference: [DOMPurify](https://github.com/cure53/DOMPurify)
