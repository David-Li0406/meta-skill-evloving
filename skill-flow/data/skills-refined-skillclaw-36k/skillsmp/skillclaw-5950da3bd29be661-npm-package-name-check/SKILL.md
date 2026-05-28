---
name: npm-package-name-check
description: Use this skill when you need to validate npm package names, check their availability, or verify if a package is published in the npm registry.
---

# npm Package Name Check

This skill allows you to validate npm package names, check their availability on the npm registry, and confirm if a package is published.

## CLI Usage

### Check Package Name Availability

To check if a package name is available, use the following command:

```bash
npx npm-package-name-check <package-name> [options]
```

### Options

| Option           | Description                      |
| ---------------- | -------------------------------- |
| `--validate, -v` | Validate only (no network check) |
| `--check, -c`    | Full check with detailed output  |
| `--no-cache`      | Bypass cache and fetch fresh data from API |
| `--json, -j`     | Output as JSON for scripting     |
| `--quiet, -q`    | Minimal output (exit codes only) |

### Examples

```bash
# Check single package availability
npx npm-package-name-check my-awesome-package

# Check multiple packages
npx npm-package-name-check react vue angular

# Validate without network check
npx npm-package-name-check "My Package" --validate

# JSON output for scripting
npx npm-package-name-check foo bar --json

# Check if a package exists
npx npm-package-name-check react --check
```

## Programmatic Usage

You can also use this skill programmatically:

```typescript
import npmPackageNameCheck from "npm-package-name-check";

// Check availability
const isAvailable = await npmPackageNameCheck("my-package");

// Validate only (no network)
const validation = npmPackageNameCheck.validate("my-package");

// Full check: validate + availability
const result = await npmPackageNameCheck.check("my-package");

// Batch check multiple names
const results = await npmPackageNameCheck.many(["name1", "name2", "name3"]);
```

## npm Naming Rules

### Errors (Invalid for all packages)

- Must be a string
- Cannot be empty
- No leading/trailing spaces
- Cannot start with `.`, `_`, or `-`
- Must be URL-safe (no special characters like `:`, `?`, etc.)
- Cannot be blacklisted names (`node_modules`, `favicon.ico`)

### Warnings (Invalid for new packages)

- Max 214 characters
- No uppercase letters
- No special characters (`~'!()*`)
- Cannot be Node.js core module names (`fs`, `http`, `path`, etc.)

### Scoped Packages

Within a scope (`@scope/name`), the name portion can:

- Start with `-` or `_`
- Use core module names
- Use reserved names

## Best Practices

When suggesting package names:

1. Use lowercase letters, numbers, and hyphens only.
2. Keep names short but descriptive.
3. Check availability before recommending.
4. For scoped packages, use `@org/package-name` format.
5. Avoid generic names.