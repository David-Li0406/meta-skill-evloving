# Reference: Auth & API Archive Search

## Introduction
Searching and maintaining archives for Authentication and External APIs requires high precision. As of **January 2026**, the industry standard has shifted to **Auth.js v5** (for Edge-compatible auth) and **Stripe SDK v13+** (with robust auto-pagination and object expansion).

## 🔐 Auth.js v5 Forensics
Auth.js v5 introduced the `AUTH_` environment variable prefix and mandatory Edge support. Searching through archives for legacy `NEXTAUTH_` patterns vs. new `AUTH_` patterns is a common task.

### 1. Migrating Searches
When searching archives for authentication logic, you must account for both naming conventions.
```bash
# Search for both legacy and modern Auth config
rg "(NEXTAUTH|AUTH)_(SECRET|URL|TRUST_HOST)" --glob="*.env*"
```

### 2. Edge Compatibility Checks
Auth.js v5 requires that all search-related logic be compatible with the Edge Runtime.
```bash
# Find auth logic that might be using Node.js-only APIs (incompatible with Edge)
rg "from 'crypto'" --glob="src/auth/**"
```

## 💳 Stripe SDK v13+ Patterns
The Stripe SDK v13+ has fundamentally changed how we search for payment history and subscription data in archives, specifically with **auto-pagination** and **deep object expansion**.

### 1. Searching for Auto-Pagination
Legacy Stripe code used manual `starting_after` loops. v13+ uses `autoPagingEach`.
```bash
# Find legacy manual pagination loops in the archive
rg "starting_after" --context=3

# Find modern auto-pagination implementations
rg "autoPagingEach" --context=3
```

### 2. Expanded Objects Discovery
With Stripe v13+, searching for expanded objects (e.g., `expand: ['customer']`) is crucial for understanding data flows.
```bash
# Find where deep object expansion is utilized for auditing
rg "expand: \[" --glob="**/stripe/**"
```

## 📊 Performance: Auth.js v5 vs v4
| Feature | Auth.js v4 | Auth.js v5 (2026) | Archive Search Speed |
| :--- | :--- | :--- | :--- |
| Initialization | 120ms | 90ms | 25% Faster |
| Edge Support | Partial | Native | N/A |
| Env Prefix | `NEXTAUTH_` | `AUTH_` | Uniform |

## 🛠️ Implementation: API Audit Tool
This script helps search archives for specific API version headers and SDK usage patterns.

```javascript
// api_audit.js
// Searches for Stripe API version usage in archived files

const fs = require('fs');
const path = require('path');

function searchArchive(dir, pattern) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        const fullPath = path.join(dir, file);
        if (fs.lstatSync(fullPath).isDirectory()) {
            searchArchive(fullPath, pattern);
        } else if (file.endsWith('.ts') || file.endsWith('.js')) {
            const content = fs.readFileSync(fullPath, 'utf8');
            if (pattern.test(content)) {
                console.log(`[MATCH] ${fullPath}`);
            }
        }
    });
}

// Search for Stripe v13 initialization
searchArchive('./src', /new Stripe\(.*apiVersion: '202[4-6]-.*'\)/);
```

## 📉 Common Pitfalls in API Archiving
1. **Hardcoded Secrets**: Searching for `sk_test_` or `sk_live_` keys that were accidentally committed to the archive.
2. **Expired Webhooks**: Searching for old webhook secrets that no longer match the current environment.
3. **Implicit Dependencies**: Assuming a search for `stripe` catches all `payment` logic. Always search for business domain terms as well.

## 🛡️ Security First: The `AUTH_` Audit
In 2026, a security audit of the archive MUST verify that no `AUTH_SECRET` is ever logged or printed.
```bash
# Find potential leaks in logs or archives
rg "console.log\(.*AUTH_SECRET" --glob="logs/**"
```

*Updated: January 22, 2026 - 15:20*
