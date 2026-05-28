# Edge Cases & Gotchas

Poorly documented behaviors that cause real-world pain:

## Pattern Specificity (PATTERN_KEY_COMPARE)

When multiple patterns match, Node uses a **two-tier specificity algorithm**:

1. **Longer base wins** - compare index of `*` in each key
2. **Longer total wins** - if base indices equal, compare total key length

```
"#foo/*"    (base=5) beats "#f/*"      (base=3)
"#foo/*.js" (len=10) beats "#foo/*"    (len=6)
```

Source: [Node.js ESM spec - PATTERN_KEY_COMPARE](https://nodejs.org/api/esm.html#resolution-algorithm-specification)

## No Extension Guessing

Unlike regular `require('./file')` which tries `.js`, `.json`, etc., subpath imports do **not** attempt extension resolution in **either CJS or ESM**:

```javascript
// package.json: { "imports": { "#lib/*": "./src/*" } }

require("#lib/util"); // FAILS - MODULE_NOT_FOUND
require("#lib/util.js"); // Works

import("#lib/util"); // FAILS - ERR_MODULE_NOT_FOUND
import("#lib/util.js"); // Works
```

**Workaround**: Always use explicit extensions in your imports.

Source: [nodejs/node#51492](https://github.com/nodejs/node/issues/51492)

## Arrays: Fallbacks for Validation Errors Only

Arrays work as fallbacks for **validation failures** (unsupported protocols, unmet conditions), but **NOT for file-not-found errors**:

```json
{
  "imports": {
    "#polyfill": ["node:test", "./polyfill.js"],
    "#lib/*": ["./src/*.js", "./src/*/index.js"]
  }
}
```

- `#polyfill` → Works! Falls back to `./polyfill.js` if `node:test` unavailable
- `#lib/foo` → If `./src/foo.js` doesn't exist, `./src/foo/index.js` is **NOT tried**

This is by design to avoid filesystem access during resolution.

Source: [nodejs/node#49945](https://github.com/nodejs/node/issues/49945), [PACKAGE_TARGET_RESOLVE spec](https://nodejs.org/api/esm.html#resolution-algorithm-specification)

## Trailing Slash Deprecated (DEP0155)

Folder mappings with trailing `/` are deprecated for import maps compatibility:

```json
{
  "imports": {
    "#lib/": "./src/"
  }
}
```

Use patterns instead: `"#lib/*": "./src/*"`

Source: [nodejs/node#40039](https://github.com/nodejs/node/pull/40039)

## Pattern Keys: Exactly One `*`

Pattern **keys** must have exactly one `*` to participate in pattern matching. Keys with zero or multiple `*` are treated as exact matches only:

```json
{
  "imports": {
    "#lib/*": "./src/*.js",
    "#*/*": "./src/*/*"
  }
}
```

- `#lib/*` → Valid pattern, matched by PATTERN_KEY_COMPARE
- `#*/*` → **Not a pattern** (multiple `*`), only matches literal `#*/*`

Pattern **targets** can have multiple `*` - all instances are replaced with the captured value.

Source: [Node.js ESM spec - expansionKeys](https://nodejs.org/api/esm.html#resolution-algorithm-specification) ("keys containing only a single `*`")

## Exact Match Before Patterns

Non-pattern keys are checked **before** pattern keys in PACKAGE_IMPORTS_EXPORTS_RESOLVE:

```json
{
  "imports": {
    "#foo": "./exact.js",
    "#foo/*": "./pattern/*.js"
  }
}
```

`#foo` → `./exact.js` (exact match wins, patterns never evaluated)

Source: [Node.js ESM spec - PACKAGE_IMPORTS_EXPORTS_RESOLVE](https://nodejs.org/api/esm.html#resolution-algorithm-specification)
