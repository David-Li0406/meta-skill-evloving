---
title: Write CSP-Compliant Code
impact: HIGH
impactDescription: Enables Content Security Policy to block XSS attacks
tags: security, csp, xss, headers
---

## Write CSP-Compliant Code

Content Security Policy (CSP) headers block inline scripts and eval(). Code that relies on these features breaks when CSP is enabled.

**Incorrect (breaks with CSP):**

```javascript
// Inline event handlers blocked by CSP
element.setAttribute('onclick', 'handleClick()');

// Inline scripts blocked
document.write('<script>doSomething()</script>');

// eval() blocked
const result = eval(userExpression);

// new Function() blocked
const fn = new Function('return ' + code);

// Inline styles may be blocked
element.style.cssText = 'color: ' + userColor;
```

**Correct (CSP-compliant):**

```javascript
// Use addEventListener instead of inline handlers
element.addEventListener('click', handleClick);

// Append scripts properly
const script = document.createElement('script');
script.src = '/js/safe-script.js';
document.head.appendChild(script);

// Use safe alternatives to eval
import { evaluate } from 'mathjs';
const result = evaluate(userExpression);

// Use CSS classes or CSS custom properties
element.classList.add('user-theme');
element.style.setProperty('--user-color', sanitizedColor);
```

**Testing CSP compliance:**

```javascript
// Add CSP header in development to catch violations
// Content-Security-Policy: default-src 'self'; script-src 'self'

// Listen for CSP violations
document.addEventListener('securitypolicyviolation', (e) => {
  console.error('CSP violation:', e.violatedDirective, e.blockedURI);
});
```

Reference: [MDN CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
