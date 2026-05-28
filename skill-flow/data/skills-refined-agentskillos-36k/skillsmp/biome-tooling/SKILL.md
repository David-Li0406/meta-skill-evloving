---
name: biome-tooling
description: Using Biome for fast, unified code formatting and linting - a modern alternative to ESLint and Prettier
---

# Biome Tooling

This skill covers using Biome, a fast all-in-one toolchain for formatting and linting JavaScript/TypeScript code.

## What is Biome?

Biome is a performant toolchain that provides:
- **Formatting** (replaces Prettier)
- **Linting** (replaces ESLint)
- **Fast** (written in Rust, 25x faster than Prettier)
- **Zero config** (sensible defaults)
- **Single tool** (no conflicts between tools)

## Installation

```bash
npm install --save-dev @biomejs/biome
```

## Configuration

Create `biome.json` in your project root:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.5.3/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true,
    "formatWithErrors": false,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "lineEnding": "lf"
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "trailingComma": "es5",
      "semicolons": "always",
      "arrowParentheses": "always",
      "bracketSpacing": true,
      "jsxQuoteStyle": "double"
    }
  }
}
```

## Package.json Scripts

```json
{
  "scripts": {
    "format": "biome format --write .",
    "format:check": "biome format .",
    "lint": "biome lint .",
    "lint:fix": "biome lint --apply .",
    "check": "biome check --apply .",
    "ci": "biome ci ."
  }
}
```

**Script explanations:**
- `format` - Format all files in place
- `format:check` - Check if files are formatted (CI)
- `lint` - Show linting errors
- `lint:fix` - Fix auto-fixable issues
- `check` - Format + lint + organize imports (recommended)
- `ci` - Check everything without modifying files (for CI)

## Basic Usage

### Format Files

```bash
# Format all files
npm run format

# Format specific files
npx biome format --write src/

# Check formatting without modifying
npx biome format src/
```

### Lint Files

```bash
# Lint all files
npm run lint

# Lint and fix
npm run lint:fix

# Lint specific files
npx biome lint src/
```

### All-in-One Check

```bash
# Format, lint, and organize imports
npm run check

# Check without modifying (for CI)
npm run ci
```

## File Configuration

### Include/Exclude Files

```json
{
  "files": {
    "include": ["src/**/*.ts", "src/**/*.tsx"],
    "ignore": [
      "node_modules",
      "dist",
      "build",
      ".sst",
      "*.config.js"
    ]
  }
}
```

### Override for Specific Files

```json
{
  "overrides": [
    {
      "include": ["*.test.ts", "*.spec.ts"],
      "linter": {
        "rules": {
          "suspicious": {
            "noExplicitAny": "off"
          }
        }
      }
    }
  ]
}
```

## Linter Rules

### Enable Recommended Rules

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

### Customize Rule Groups

```json
{
  "linter": {
    "rules": {
      "recommended": true,
      "complexity": {
        "noExcessiveCognitiveComplexity": "warn",
        "noForEach": "off"
      },
      "style": {
        "noNegationElse": "error",
        "useTemplate": "warn"
      },
      "suspicious": {
        "noExplicitAny": "warn",
        "noArrayIndexKey": "warn"
      }
    }
  }
}
```

### Rule Categories

**Complexity:**
- noExcessiveCognitiveComplexity
- noForEach
- useFlatMap
- useSimplifiedLogicExpression

**Correctness:**
- noUnreachable
- noUndeclaredVariables
- noUnusedVariables
- useExhaustiveDependencies

**Performance:**
- noAccumulatingSpread
- noDelete

**Security:**
- noDangerouslySetInnerHtml
- noDangerouslySetInnerHtmlWithChildren

**Style:**
- noArguments
- noImplicitBoolean
- noNegationElse
- useBlockStatements
- useTemplate

**Suspicious:**
- noArrayIndexKey
- noCommentText
- noExplicitAny
- noShadowRestrictedNames

## Formatter Configuration

### Basic Options

```json
{
  "formatter": {
    "enabled": true,
    "formatWithErrors": false,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "lineEnding": "lf"
  }
}
```

### JavaScript-Specific Options

```json
{
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "jsxQuoteStyle": "double",
      "quoteProperties": "asNeeded",
      "trailingComma": "all",
      "semicolons": "always",
      "arrowParentheses": "always",
      "bracketSpacing": true,
      "bracketSameLine": false
    }
  }
}
```

## Import Organization

```json
{
  "organizeImports": {
    "enabled": true
  }
}
```

Biome will:
- Remove unused imports
- Sort imports
- Group imports (built-in, external, internal)

## VSCode Integration

### Install Extension

Install "Biome" extension from VSCode marketplace.

### VSCode Settings

```json
{
  "editor.defaultFormatter": "biomejs.biome",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "quickfix.biome": "explicit",
    "source.organizeImports.biome": "explicit"
  },
  "[javascript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "biomejs.biome"
  }
}
```

## Git Hooks

### Using Husky + lint-staged

```bash
npm install --save-dev husky lint-staged
```

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "biome check --apply --no-errors-on-unmatched"
    ]
  }
}
```

```bash
# Setup husky
npx husky init
echo "npx lint-staged" > .husky/pre-commit
```

## CI/CD Integration

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 20
      - run: npm ci
      - run: npm run ci
        # Runs: biome ci .
```

### GitLab CI

```yaml
check:
  stage: test
  script:
    - npm ci
    - npm run ci
```

## Migration from ESLint + Prettier

### Remove Old Tools

```bash
npm uninstall eslint prettier @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

```bash
# Remove config files
rm .eslintrc.js .prettierrc .prettierignore .eslintignore
```

### Install Biome

```bash
npm install --save-dev @biomejs/biome
```

### Initialize Config

```bash
npx @biomejs/biome init
```

### Update Scripts

Replace:
```json
{
  "scripts": {
    "lint": "eslint .",
    "format": "prettier --write ."
  }
}
```

With:
```json
{
  "scripts": {
    "check": "biome check --apply .",
    "ci": "biome ci ."
  }
}
```

## Common Patterns

### Ignore Generated Files

```json
{
  "files": {
    "ignore": [
      "*.generated.ts",
      "build/",
      ".sst/",
      "coverage/"
    ]
  }
}
```

### Strict Mode for Production

```json
{
  "linter": {
    "rules": {
      "recommended": true,
      "suspicious": {
        "noExplicitAny": "error",
        "noArrayIndexKey": "error"
      }
    }
  }
}
```

### Relaxed Rules for Tests

```json
{
  "overrides": [
    {
      "include": ["**/*.test.ts", "**/*.spec.ts"],
      "linter": {
        "rules": {
          "suspicious": {
            "noExplicitAny": "off"
          },
          "complexity": {
            "noExcessiveCognitiveComplexity": "off"
          }
        }
      }
    }
  ]
}
```

## Best Practices

### 1. Use in Pre-commit Hooks

```bash
# Ensures all committed code is formatted and linted
npx lint-staged
```

### 2. Run in CI/CD

```yaml
- run: npm run ci
```

Fail the build if code doesn't pass checks.

### 3. Format on Save

Configure your editor to format on save.

### 4. Keep Config Minimal

Start with defaults, only configure what you need:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.5.3/schema.json",
  "formatter": {
    "lineWidth": 100
  },
  "linter": {
    "rules": {
      "recommended": true
    }
  }
}
```

### 5. Use with TypeScript

Biome works great with TypeScript:

```json
{
  "javascript": {
    "parser": {
      "unsafeParameterDecoratorsEnabled": true
    }
  }
}
```

## Performance Benefits

Biome is significantly faster than ESLint + Prettier:

```bash
# Formatting 5000 files
Prettier: ~30 seconds
Biome:    ~1 second

# Linting 5000 files
ESLint: ~45 seconds
Biome:  ~2 seconds
```

## Troubleshooting

### "Command not found: biome"

```bash
# Install locally
npm install --save-dev @biomejs/biome

# Or use npx
npx @biomejs/biome check .
```

### "Parse errors" on valid code

Check your biome.json parser options:

```json
{
  "javascript": {
    "parser": {
      "unsafeParameterDecoratorsEnabled": true
    }
  }
}
```

### VSCode not formatting

1. Install Biome extension
2. Check it's the default formatter
3. Reload VSCode

### Conflicts with existing tools

Remove ESLint and Prettier:
```bash
npm uninstall eslint prettier
```

## Advanced Configuration

### Per-Project Settings

```json
{
  "extends": ["@company/biome-config"],
  "formatter": {
    "lineWidth": 120
  }
}
```

### Custom Rule Severity

```json
{
  "linter": {
    "rules": {
      "suspicious": {
        "noExplicitAny": {
          "level": "warn",
          "fix": "none"
        }
      }
    }
  }
}
```

## Comparison: Biome vs ESLint + Prettier

| Feature | Biome | ESLint + Prettier |
|---------|-------|-------------------|
| Speed | 25x faster | Slower |
| Setup | Single tool | Two tools + config |
| Conflicts | None | Possible |
| Rules | Growing | Extensive |
| Plugins | Limited | Many |
| Memory | Lower | Higher |

## When to Use Biome

✅ **Use Biome when:**
- Starting a new project
- Speed is important
- You want simpler tooling
- You're okay with opinionated defaults

⚠️ **Consider alternatives when:**
- You need specific ESLint plugins
- You have complex custom rules
- Team is heavily invested in ESLint

## Migration Checklist

- [ ] Install Biome
- [ ] Create biome.json
- [ ] Update package.json scripts
- [ ] Remove ESLint/Prettier
- [ ] Update pre-commit hooks
- [ ] Update CI/CD pipelines
- [ ] Configure VSCode
- [ ] Test on existing code
- [ ] Update team documentation

## Further Reading

- Biome Docs: https://biomejs.dev/
- Biome GitHub: https://github.com/biomejs/biome
- Biome Playground: https://biomejs.dev/playground/
- VSCode Extension: https://marketplace.visualstudio.com/items?itemName=biomejs.biome
