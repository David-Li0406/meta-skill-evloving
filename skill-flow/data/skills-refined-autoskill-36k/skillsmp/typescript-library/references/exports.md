# Package.json Exports Field

## Basic Structure

```json
{
  "name": "my-library",
  "type": "module",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    }
  }
}
```

## With TypeScript Types

Types MUST come before other conditions:

```json
{
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    }
  }
}
```

## Multiple Entry Points

```json
{
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    },
    "./utils": {
      "import": "./dist/utils.js",
      "require": "./dist/utils.cjs"
    },
    "./plugins/*": {
      "import": "./dist/plugins/*.js",
      "require": "./dist/plugins/*.cjs"
    }
  }
}
```

Usage:
```typescript
import { main } from 'my-library';
import { helper } from 'my-library/utils';
import { plugin } from 'my-library/plugins/auth';
```

## Condition Keys

| Condition | When Used |
|-----------|-----------|
| `import` | ESM import |
| `require` | CommonJS require |
| `types` | TypeScript types |
| `default` | Fallback |
| `node` | Node.js environment |
| `browser` | Browser environment |
| `development` | Development builds |
| `production` | Production builds |

## Browser/Node Split

```json
{
  "exports": {
    ".": {
      "browser": {
        "import": "./dist/browser.js"
      },
      "node": {
        "import": "./dist/node.js",
        "require": "./dist/node.cjs"
      },
      "default": "./dist/index.js"
    }
  }
}
```

## Legacy Fallbacks

For older bundlers/Node versions:

```json
{
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    }
  }
}
```

## Restricting Access

Only export specific paths:

```json
{
  "exports": {
    ".": "./dist/index.js",
    "./utils": "./dist/utils.js",
    "./package.json": "./package.json"
  }
}
```

Anything not listed is inaccessible:
```typescript
import { internal } from 'my-library/internal';  // Error!
```

## Subpath Patterns

```json
{
  "exports": {
    ".": "./dist/index.js",
    "./*": "./dist/*.js",
    "./*/index": "./dist/*/index.js"
  }
}
```

## TypeScript Project References

For monorepos with TypeScript:

```json
{
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      }
    }
  },
  "typesVersions": {
    "*": {
      "*": ["./dist/*"]
    }
  }
}
```

## Testing Exports

```bash
# Verify with npm pack
npm pack --dry-run

# Test import/require
node -e "import('my-library').then(console.log)"
node -e "console.log(require('my-library'))"

# Use publint
npx publint
npx attw --pack
```
