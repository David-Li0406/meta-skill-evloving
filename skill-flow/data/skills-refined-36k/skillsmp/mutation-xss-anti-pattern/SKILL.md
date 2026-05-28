---
name: "mutation-xss-anti-pattern"
description: "Security anti-pattern for mutation XSS (mXSS) vulnerabilities (CWE-79 variant). Use when generating or reviewing code that sanitizes HTML content, handles user-provided markup, or processes rich text. Detects sanitizer bypass through browser parsing mutations."
---

# Mutation XSS (mXSS) Anti-Pattern

**Severity:** High

## Summary

Mutation XSS bypasses HTML sanitizers through inconsistent parsing. Attackers provide HTML appearing safe to sanitizers. When inserted into DOM, browser parsing "corrects" malformed code, creating executable scripts. Sanitizer sees one DOM, browser creates a different, malicious one.

## The Anti-Pattern

The anti-pattern is HTML sanitizers ignoring browser's unpredictable parsing. Final browser DOM differs from sanitizer's checked DOM.

### BAD Code Example

```javascript
// VULNERABLE: A simple sanitizer that is unaware of browser mutations.

function simpleSanitize(html) {
    // Naive sanitizer: removes `<script>` tags only.
    // Doesn't understand browser's HTML parsing quirks.
    return html.replace(/<script.*?>.*?<\/script>/gi, '');
}

function renderComment(commentHtml) {
    const sanitizedHtml = simpleSanitize(commentHtml);
    // Sanitized HTML inserted into page.
    document.getElementById('comments').innerHTML = sanitizedHtml;
}

// Attack: '<noscript><p title="</noscript><img src=x onerror=alert(1)>">'

// 1. simpleSanitize sees no `<script>` tags, does nothing
// 2. Browser receives: '<noscript><p title="</noscript><img src=x onerror=alert(1)>">'
// 3. Browser parsing "fixes" broken structure:
//    - Sees `<noscript>`, `<p title="`
//    - Treats `</noscript>` as malformed text in title attribute
//    - Continues, sees `<img src=x onerror=alert(1)>`
//    - Creates `<img>` with `onerror` attribute
// 4. `onerror` fires, executes script. Sanitizer bypassed.
renderComment(payload);
```

### GOOD Code Example

```javascript
// SECURE: Use a mature, well-maintained, and mutation-aware HTML sanitizer like DOMPurify.

function renderCommentSafe(commentHtml) {
    // DOMPurify designed to understand and defeat mXSS.
    // Parses HTML in sandbox, removes dangerous content, serializes to clean HTML.
    // Aware of browser parsing quirks.
    const sanitizedHtml = DOMPurify.sanitize(commentHtml);

    document.getElementById('comments').innerHTML = sanitizedHtml;
}

// DOMPurify correctly identifies broken HTML,
// strips malicious `onerror` attribute, neutralizes attack.
const payload = '<noscript><p title="</noscript><img src=x onerror=alert(1)>">';
renderCommentSafe(payload);

// Combine with strong CSP (defense-in-depth).
```

## Detection

- **mXSS is extremely difficult to detect manually.** It relies on deep knowledge of browser-specific parsing edge cases.
- **Review Sanitizer Choice:** Check if the application uses a known-vulnerable or homegrown HTML sanitizer. If it's not a library like DOMPurify that is actively maintained to fight mXSS, it is likely vulnerable.
- **Use mXSS-specific payloads:** Test the application's sanitizer with known mXSS payloads from security research (e.g., from the Cure53 research paper).

## Prevention

- [ ] **Use mXSS-aware sanitizer:** Industry standard is DOMPurify. Never write your own sanitizer.
- [ ] **Keep sanitizer updated:** New mXSS vectors discovered periodically. Libraries receive new defenses.
- [ ] **Configure for maximum safety:** Forbid dangerous tags (`<style>`, `<svg>`, `<math>`) unless absolutely necessary.
- [ ] **Implement strong CSP:** Second defense layer. Strict CSP blocks inline event handlers (`onerror`) and untrusted scripts, preventing mXSS execution if sanitizer fails.
- [ ] **Avoid HTML sanitization when possible:** For simple formatting (bold, italics), use Markdown with safe converter instead of raw HTML.

## Related Security Patterns & Anti-Patterns

- [Cross-Site Scripting (XSS) Anti-Pattern](../xss/): mXSS is a specific and advanced technique for achieving XSS.
- [DOM Clobbering Anti-Pattern](../dom-clobbering/): Another client-side attack that abuses the browser's DOM manipulation behavior.
- [Encoding Bypass Anti-Pattern](../encoding-bypass/): A different technique for bypassing input filters and sanitizers.

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM09:2025 - Misinformation](https://genai.owasp.org/llmrisk/llm09-misinformation/)
- [CWE-79: Cross-site Scripting](https://cwe.mitre.org/data/definitions/79.html)
- [CAPEC-86: XSS Through HTTP Headers](https://capec.mitre.org/data/definitions/86.html)
- [PortSwigger: Cross Site Scripting](https://portswigger.net/web-security/cross-site-scripting)
- [DOMPurify](https://github.com/cure53/DOMPurify)
- [Mutation XSS Research (Cure53)](https://cure53.de/fp170.pdf)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
