# Cross-Platform with Subpath Imports

Use conditional `imports` to abstract platform-specific implementations within your package.

## How It Works

1. Define condition-specific targets in `imports`
2. Your code imports via `#alias`
3. Runtimes/bundlers resolve to the correct target based on conditions
4. First matching condition wins (order matters)

```json
{
  "imports": {
    "#platform": {
      "react-native": "./src/platform/native.js",
      "browser": "./src/platform/browser.js",
      "node": "./src/platform/node.js",
      "default": "./src/platform/node.js"
    }
  }
}
```

```javascript
// Your code - works everywhere
import platform from "#platform";
```

---

## Key Use Cases

### Platform Abstraction

Abstract platform differences behind a stable internal API:

```json
{
  "imports": {
    "#storage": {
      "react-native": "./src/storage/async-storage.js",
      "browser": "./src/storage/local-storage.js",
      "node": "./src/storage/fs.js",
      "default": "./src/storage/memory.js"
    }
  }
}
```

### External Package Substitution

Map to different npm packages per environment (only `imports` can do this - `exports` cannot):

```json
{
  "imports": {
    "#fetch": {
      "node": "node-fetch",
      "default": "./src/fetch-native.js"
    },
    "#lodash": {
      "require": "lodash",
      "import": "lodash-es"
    }
  },
  "dependencies": {
    "node-fetch": "^3.0.0",
    "lodash": "^4.17.21",
    "lodash-es": "^4.17.21"
  }
}
```

### Dev/Prod Implementations

```json
{
  "imports": {
    "#logger": {
      "development": "./src/logger/verbose.js",
      "production": "./src/logger/minimal.js",
      "default": "./src/logger/minimal.js"
    }
  }
}
```

---

## Conditions Reference

Conditions work identically for `imports` and `exports`. The following reference applies to both.

### Built-in Conditions

| Condition     | When Matched               |
| ------------- | -------------------------- |
| `node-addons` | Node.js with native addons |
| `node`        | Any Node.js environment    |
| `import`      | Loaded via `import`        |
| `require`     | Loaded via `require()`     |
| `default`     | Fallback (must be last)    |

### Community Conditions

| Condition      | When Matched                |
| -------------- | --------------------------- |
| `types`        | TypeScript resolution       |
| `browser`      | Web browser                 |
| `react-native` | React Native                |
| `react-server` | React Server Components     |
| `deno`         | Deno runtime                |
| `bun`          | Bun runtime                 |
| `worker`       | Web Worker / Service Worker |
| `development`  | Dev build                   |
| `production`   | Prod build                  |

### Nested Conditions

Conditions can be nested for fine-grained control:

```json
{
  "imports": {
    "#crypto": {
      "node": {
        "import": "./src/crypto/node.mjs",
        "require": "./src/crypto/node.cjs"
      },
      "browser": "./src/crypto/browser.js",
      "default": "./src/crypto/polyfill.js"
    }
  }
}
```

---

## Conditions by Runtime

| Runtime | Default Conditions                           | Custom via       |
| ------- | -------------------------------------------- | ---------------- |
| Node.js | `node`, `import`/`require`, `default`        | `--conditions=X` |
| Deno    | `deno`, `node`, `import`, `default`          | `--conditions=X` |
| Bun     | `bun`, `node`, `import`/`require`, `default` | `--conditions=X` |

### Node.js

```bash
node --conditions=development --conditions=custom app.js
```

### Deno

```bash
deno run --conditions=development,react-server main.ts
```

### Bun

```bash
bun --conditions=react-server ./app.js
```

---

## Conditions by Bundler

### Webpack / Rspack

```javascript
// webpack.config.js
module.exports = {
  resolve: {
    conditionNames: ["import", "module", "browser", "default"],
  },
};
```

Source: [webpack.js.org](https://webpack.js.org/configuration/resolve/#resolveconditionnames)

### esbuild

```bash
esbuild --conditions=custom --platform=node app.js
```

Auto-added: `--platform=node` adds `node`, `--platform=browser` adds `browser`.

Source: [esbuild.github.io](https://esbuild.github.io/api/#conditions)

### Rollup

```javascript
import resolve from "@rollup/plugin-node-resolve";

export default {
  plugins: [
    resolve({
      exportConditions: ["node", "import", "default"],
    }),
  ],
};
```

Source: [npm @rollup/plugin-node-resolve](https://www.npmjs.com/package/@rollup/plugin-node-resolve)

### Vite

```javascript
// vite.config.js
export default {
  resolve: {
    conditions: ["custom", "module", "browser"],
  },
};
```

Source: [vite.dev](https://vite.dev/config/shared-options#resolve-conditions)

### Metro (React Native)

```javascript
// metro.config.js
module.exports = {
  resolver: {
    unstable_conditionNames: ["require", "react-native"],
  },
};
```

Source: [metrobundler.dev](https://metrobundler.dev/docs/package-exports/)

---

## Condition Order (Critical)

First matching condition wins. Order from most specific to least:

```json
{
  "imports": {
    "#dep": {
      "types": "./src/dep.d.ts",
      "react-native": "./src/dep/native.js",
      "browser": "./src/dep/browser.js",
      "node": "./src/dep/node.js",
      "import": "./src/dep/esm.js",
      "require": "./src/dep/cjs.js",
      "default": "./src/dep/fallback.js"
    }
  }
}
```

Recommended order:

1. `types` (TypeScript, always first)
2. Platform-specific (`react-native`, `deno`, `bun`)
3. Environment (`browser`, `node`, `worker`)
4. Module system (`import`, `require`)
5. `default` (always last)

---

## Complete Example

```json
{
  "name": "my-cross-platform-lib",
  "type": "module",
  "imports": {
    "#platform": {
      "react-native": "./src/platform/native.js",
      "browser": "./src/platform/browser.js",
      "node": "./src/platform/node.js",
      "default": "./src/platform/node.js"
    },
    "#fetch": {
      "node": "node-fetch",
      "default": "./src/fetch-native.js"
    },
    "#storage": {
      "react-native": "./src/storage/async-storage.js",
      "browser": "./src/storage/local-storage.js",
      "node": "./src/storage/fs.js",
      "default": "./src/storage/memory.js"
    }
  },
  "dependencies": {
    "node-fetch": "^3.0.0"
  }
}
```

```javascript
// src/index.js - single codebase, works everywhere
import platform from "#platform";
import fetch from "#fetch";
import storage from "#storage";

export async function getData(key) {
  const cached = await storage.get(key);
  if (cached) return cached;

  const data = await fetch(`${platform.apiUrl}/${key}`);
  await storage.set(key, data);
  return data;
}
```

---

## Alternative: `exports` Conditions

Cross-platform can also be achieved via the `exports` field, which controls what consumers import from your package. The `imports` approach (this document) handles internal platform abstraction; `exports` handles external API surface.

Both support the same conditions. Key difference: `imports` can map to external packages, `exports` cannot.

For `exports`-based cross-platform patterns, see a future `nodejs-package-exports` skill.
