---
title: Use textContent Instead of innerHTML
impact: HIGH
impactDescription: Prevents XSS vulnerabilities from user-provided content
tags: security, xss, innerhtml, textcontent
---

## Use textContent Instead of innerHTML

innerHTML parses content as HTML, enabling XSS attacks when user input is inserted. textContent safely inserts text without HTML parsing.

**Incorrect (XSS vulnerability):**

```javascript
// User input: <img src=x onerror="alert('hacked')">
const userComment = getUserComment();
commentDiv.innerHTML = userComment; // Executes malicious script
```

**Correct (safe text insertion):**

```javascript
const userComment = getUserComment();
commentDiv.textContent = userComment; // Renders as plain text
```

**When HTML is needed, use sanitization:**

```javascript
import DOMPurify from 'dompurify';

// Sanitize before inserting
const sanitizedHTML = DOMPurify.sanitize(userContent);
contentDiv.innerHTML = sanitizedHTML;
```

**For building HTML dynamically:**

```javascript
// Create elements programmatically instead
const link = document.createElement('a');
link.href = sanitizeURL(userURL);
link.textContent = userText; // Safe
container.appendChild(link);
```

Never use innerHTML with untrusted content. Prefer textContent, createElement, or a sanitization library.

Reference: [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
