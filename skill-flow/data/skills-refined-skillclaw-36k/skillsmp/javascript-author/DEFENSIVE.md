# Defensive JavaScript Patterns

Write robust, defensive JavaScript that handles edge cases, validates inputs, and degrades gracefully.

## Type Guards

### typeof Checks

```javascript
/**
 * Type-safe property access
 * @param {unknown} value
 * @returns {string}
 */
function getDisplayName(value) {
    if (typeof value === 'string') {
        return value;
    }
    if (typeof value === 'object' && value !== null && 'name' in value) {
        return String(value.name);
    }
    return 'Unknown';
}
```

### Common typeof Guards

| Check | Use Case |
|-------|----------|
| `typeof x === 'string'` | String operations |
| `typeof x === 'number'` | Math operations |
| `typeof x === 'function'` | Before calling |
| `typeof x === 'object' && x !== null` | Object access |
| `typeof x === 'undefined'` | Optional values |

### instanceof and Constructor Checks

```javascript
// Array check (preferred)
if (Array.isArray(items)) {
    items.forEach(process);
}

// Date check
if (value instanceof Date && !isNaN(value.getTime())) {
    return value.toISOString();
}

// Error check
if (error instanceof Error) {
    console.error(error.message, error.stack);
}

// Custom class check
if (element instanceof HTMLElement) {
    element.setAttribute('data-processed', 'true');
}
```

### Nullish Checks

```javascript
// Nullish coalescing for defaults
const timeout = config.timeout ?? 5000;

// Optional chaining for deep access
const city = user?.address?.city ?? 'Unknown';

// Guard before access
if (data != null) {
    process(data);
}
```

---

## Number Safety

### isNaN and isFinite

```javascript
/**
 * Parse user input as number
 * @param {string} input - User-provided value
 * @param {number} defaultValue - Fallback if invalid
 * @returns {number}
 */
function parseUserNumber(input, defaultValue = 0) {
    const parsed = parseFloat(input);

    // Check for NaN
    if (Number.isNaN(parsed)) {
        return defaultValue;
    }

    // Check for Infinity
    if (!Number.isFinite(parsed)) {
        return defaultValue;
    }

    return parsed;
}
```

### Safe Integer Checks

```javascript
/**
 * Validate array index
 * @param {number} index
 * @param {number} length - Array length
 * @returns {boolean}
 */
function isValidIndex(index, length) {
    return (
        Number.isInteger(index) &&
        index >= 0 &&
        index < length
    );
}

// Safe integer range: -(2^53 - 1) to 2^53 - 1
if (Number.isSafeInteger(value)) {
    // Safe for precise arithmetic
}
```

### BigInt for Large Numbers

```javascript
/**
 * Calculate large factorial
 * @param {number} n
 * @returns {bigint}
 */
function factorial(n) {
    if (n < 0 || !Number.isInteger(n)) {
        throw new RangeError('Requires non-negative integer');
    }

    let result = 1n;
    for (let i = 2n; i <= BigInt(n); i++) {
        result *= i;
    }
    return result;
}

// Use BigInt for:
// - IDs from databases (avoid precision loss)
// - Cryptographic operations
// - Financial calculations requiring precision
const userId = BigInt('9007199254740993');
```

### Explicit Type Coercion

```javascript
// Prefer explicit over implicit coercion

// Numbers
const count = parseInt(input, 10);      // Always specify radix
const price = parseFloat(priceStr);
const num = Number(value);              // Strict conversion

// Strings
const str = String(value);              // Explicit
const display = `${value}`;             // Template literal

// Booleans
const flag = Boolean(value);            // Explicit
const exists = value != null;           // Nullish check

// Avoid
// +value, value * 1, !!value, value + ''
```

---

## Feature Detection

### API Availability

```javascript
/**
 * Check if API is available before use
 */
function supportsLocalStorage() {
    try {
        const test = '__storage_test__';
        localStorage.setItem(test, test);
        localStorage.removeItem(test);
        return true;
    } catch {
        return false;
    }
}

// Usage pattern
const storage = supportsLocalStorage()
    ? localStorage
    : createMemoryStorage();
```

### Common Feature Checks

```javascript
// IntersectionObserver
if ('IntersectionObserver' in window) {
    // Use native
} else {
    // Fallback or polyfill
}

// Fetch API
if (typeof fetch === 'function') {
    // Use fetch
}

// Web Components
if ('customElements' in window) {
    customElements.define('my-component', MyComponent);
}

// Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
}

// CSS.supports for CSS feature detection
if (CSS.supports('display', 'grid')) {
    // Grid is supported
}
```

### Media Query Checks

```javascript
// Check reduced motion preference
const prefersReducedMotion =
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Check color scheme
const prefersDark =
    window.matchMedia('(prefers-color-scheme: dark)').matches;

// Listen for changes
const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
mediaQuery.addEventListener('change', (e) => {
    updateTheme(e.matches ? 'dark' : 'light');
});
```

---

## Polyfill Strategy

### Conditional Loading

```javascript
// Load polyfills only when needed
async function loadPolyfills() {
    const polyfills = [];

    if (!('IntersectionObserver' in window)) {
        polyfills.push(import('intersection-observer'));
    }

    if (!Array.prototype.at) {
        polyfills.push(import('array.prototype.at'));
    }

    await Promise.all(polyfills);
}

// Initialize after polyfills load
loadPolyfills().then(initApp);
```

### Polyfill Sources

| Feature | Polyfill |
|---------|----------|
| `fetch` | `whatwg-fetch` |
| `IntersectionObserver` | `intersection-observer` |
| `ResizeObserver` | `resize-observer-polyfill` |
| `URLSearchParams` | `url-search-params-polyfill` |
| Modern array methods | `core-js` |

### Progressive Enhancement Pattern

```javascript
// Define feature as optional enhancement
class EnhancedGallery extends HTMLElement {
    connectedCallback() {
        // Base functionality always works
        this.setupBasicGallery();

        // Enhanced features if supported
        if ('IntersectionObserver' in window) {
            this.setupLazyLoading();
        }

        if (CSS.supports('scroll-snap-type', 'x mandatory')) {
            this.dataset.snapScroll = 'true';
        }
    }
}
```

---

## Error Handling

### try/catch Patterns

```javascript
/**
 * Safe JSON parsing
 * @param {string} jsonString
 * @param {unknown} fallback
 * @returns {unknown}
 */
function safeJsonParse(jsonString, fallback = null) {
    try {
        return JSON.parse(jsonString);
    } catch (error) {
        if (error instanceof SyntaxError) {
            console.warn('Invalid JSON:', error.message);
        }
        return fallback;
    }
}

/**
 * Async operation with error handling
 * @param {string} url
 * @returns {Promise<Response|null>}
 */
async function safeFetch(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return response;
    } catch (error) {
        console.error('Fetch failed:', error);
        return null;
    }
}
```

### Error Boundaries in Components

```javascript
class SafeComponent extends HTMLElement {
    connectedCallback() {
        try {
            this.render();
            this.setupListeners();
        } catch (error) {
            this.handleError(error);
        }
    }

    handleError(error) {
        console.error('Component error:', error);
        this.innerHTML = `
            <div class="error-fallback">
                <p>Something went wrong. Please refresh the page.</p>
            </div>
        `;
        // Report to error tracking service
        this.reportError(error);
    }

    reportError(error) {
        // Send to monitoring service
        if (typeof window.errorReporter === 'function') {
            window.errorReporter(error, {
                component: this.tagName,
                url: location.href
            });
        }
    }
}
```

### Global Error Handling

```javascript
/**
 * Set up global error handlers
 */
function setupErrorHandling() {
    // Uncaught errors
    window.onerror = (message, source, line, col, error) => {
        console.error('Uncaught error:', { message, source, line, col });
        reportToServer({ type: 'error', message, source, line, col, stack: error?.stack });
        // Return true to prevent default browser error handling
        return false;
    };

    // Unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
        console.error('Unhandled rejection:', event.reason);
        reportToServer({ type: 'rejection', reason: String(event.reason) });
    });
}

/**
 * Report error to monitoring service
 * @param {Object} errorData
 */
function reportToServer(errorData) {
    // Use sendBeacon for reliability (works even during page unload)
    if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/errors', JSON.stringify(errorData));
    } else {
        fetch('/api/errors', {
            method: 'POST',
            body: JSON.stringify(errorData),
            keepalive: true
        }).catch(() => {
            // Ignore reporting failures
        });
    }
}
```

---

## Input Validation

### Sanitization Patterns

```javascript
/**
 * Sanitize user input for display
 * @param {string} input
 * @returns {string}
 */
function sanitizeForDisplay(input) {
    if (typeof input !== 'string') {
        return '';
    }
    return input
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;');
}

/**
 * Validate email format
 * @param {string} email
 * @returns {boolean}
 */
function isValidEmail(email) {
    if (typeof email !== 'string') {
        return false;
    }
    // Basic check - server should do full validation
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

### Bounds Checking

```javascript
/**
 * Clamp value to range
 * @param {number} value
 * @param {number} min
 * @param {number} max
 * @returns {number}
 */
function clamp(value, min, max) {
    if (!Number.isFinite(value)) {
        return min;
    }
    return Math.max(min, Math.min(max, value));
}

/**
 * Safe array access
 * @template T
 * @param {T[]} array
 * @param {number} index
 * @param {T} defaultValue
 * @returns {T}
 */
function safeArrayAccess(array, index, defaultValue) {
    if (!Array.isArray(array)) {
        return defaultValue;
    }
    if (!Number.isInteger(index) || index < 0 || index >= array.length) {
        return defaultValue;
    }
    return array[index];
}
```

---

## DOM Injection and Sanitization

### Text Content (Safest)

For text-only content, always use `textContent`:

```javascript
// Safe - automatically escapes HTML
element.textContent = userInput;

// Also safe for attributes
element.setAttribute('data-name', userInput);
```

### insertAdjacentHTML (Preferred for HTML)

Prefer `insertAdjacentHTML()` over `innerHTML` for HTML injection:

```javascript
// Preferred - more control over insertion position
element.insertAdjacentHTML('beforeend', sanitizedHTML);

// Positions:
// 'beforebegin' - Before the element
// 'afterbegin'  - Inside, before first child
// 'beforeend'   - Inside, after last child
// 'afterend'    - After the element
```

**Why prefer insertAdjacentHTML:**

| Method | Behavior | Use Case |
|--------|----------|----------|
| `innerHTML =` | Replaces all content, destroys event listeners | Avoid when possible |
| `insertAdjacentHTML()` | Adds without affecting existing content | Adding content |
| `textContent =` | Safe text only, no HTML parsing | User-provided text |

### The Sanitizer API (Emerging Standard)

The browser-native Sanitizer API provides XSS-safe HTML injection:

```javascript
// Feature detection
if ('Sanitizer' in window) {
    // Safe - automatically removes XSS-unsafe elements
    element.setHTML(untrustedHTML);

    // With custom configuration
    const sanitizer = new Sanitizer({
        elements: ['p', 'b', 'i', 'a'],
        attributes: ['href', 'class']
    });
    element.setHTML(untrustedHTML, { sanitizer });
} else {
    // Fallback required (see below)
}
```

**Browser Support (Late 2025):** Limited - Firefox Nightly, Chrome Canary (behind flag). Use DOMPurify as fallback.

### DOMPurify Fallback

Until Sanitizer API is widely supported, use DOMPurify:

```javascript
import DOMPurify from 'dompurify';

/**
 * Safely inject HTML content
 * @param {HTMLElement} element
 * @param {string} html - Untrusted HTML
 */
function safeSetHTML(element, html) {
    if ('Sanitizer' in window) {
        element.setHTML(html);
    } else {
        element.innerHTML = DOMPurify.sanitize(html);
    }
}

// With configuration
const cleanHTML = DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['p', 'b', 'i', 'a'],
    ALLOWED_ATTR: ['href', 'class']
});
```

### Safe DOM Manipulation Patterns

```javascript
// Pattern 1: Text content only (safest)
function setUserName(element, name) {
    element.textContent = name;
}

// Pattern 2: Build elements programmatically
function createLink(href, text) {
    const link = document.createElement('a');
    link.href = href;           // Automatically handled
    link.textContent = text;    // Escaped
    return link;
}

// Pattern 3: Template with sanitization
function renderCard(data) {
    const template = `
        <article>
            <h2>${escapeHTML(data.title)}</h2>
            <p>${escapeHTML(data.description)}</p>
        </article>
    `;
    container.insertAdjacentHTML('beforeend', template);
}

/**
 * Escape HTML entities
 * @param {string} str
 * @returns {string}
 */
function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}
```

### Avoid These Patterns

```javascript
// DANGEROUS - Direct innerHTML with user input
element.innerHTML = userInput;

// DANGEROUS - Template literals with unescaped data
element.innerHTML = `<div>${userData.name}</div>`;

// DANGEROUS - document.write
document.write(userContent);

// RISKY - eval or Function constructor
eval(userCode);
new Function(userCode)();
```

---

## Checklist

When writing defensive JavaScript:

- [ ] All external inputs validated with type checks
- [ ] Numbers checked with `isNaN`/`isFinite` before math operations
- [ ] Arrays checked with `Array.isArray()` before iteration
- [ ] Optional chaining (`?.`) used for potentially undefined paths
- [ ] Nullish coalescing (`??`) used for defaults (not `||`)
- [ ] Feature detection before using browser APIs
- [ ] try/catch around JSON parsing and async operations
- [ ] Global error handlers set up for uncaught errors
- [ ] Explicit type coercion (no implicit `+value` or `!!value`)
- [ ] BigInt considered for large integers or database IDs
- [ ] `textContent` used for text-only DOM updates (not `innerHTML`)
- [ ] `insertAdjacentHTML()` preferred over `innerHTML` for HTML injection
- [ ] User-provided HTML sanitized via Sanitizer API or DOMPurify
- [ ] No `eval()`, `new Function()`, or `document.write()` with user data
