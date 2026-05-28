---
name: npm-package-management
description: Use this skill when validating npm package names, checking their availability, or verifying if a package is published in the npm registry.
---

# npm Package Management

This skill allows you to validate npm package names, check their availability, and determine if a package exists in the npm registry.

## CLI Usage

### Check Package Name Availability

To check if a package name is available:

```bash
npx npname <name> [names...]
```

### Check Package Existence

To check if a package name exists in the npm registry:

```bash
npx tsx scripts/exists.ts <package-name> [options]
```

### Options

| Option           | Description                      |
| ---------------- | -------------------------------- |
| `--validate, -v` | Validate only (no network check) |
| `--check, -c`    | Full check with detailed output  |
| `--registry, -r` | Custom registry URL              |
| `--json, -j`     | Output as JSON for scripting     |
| `--no-cache`     | Bypass cache and fetch fresh data from API |
| `--quiet, -q`    | Minimal output (exit codes only) |

## Examples

### Check Availability

```bash
# Check single package availability
npx npname my-awesome-package

# Check multiple packages
npx npname react vue angular

# Validate without network check
npx npname "My Package" --validate

# JSON output for scripting
npx npname foo bar --json
```

### Check Existence

```bash
# Check if a package exists
npx tsx scripts/exists.ts react

# Check if a scoped package exists
npx tsx scripts/exists.ts @myorg/package-name
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
5. Avoid generic names that are likely taken.

## Response Interpretation

**Package exists** - HTTP 200 OK
- The package is published and available.

**Package does not exist** - HTTP 404 Not Found
- The package name is available for use.

Before publishing a new package, verify the name is available:

```bash
npx tsx scripts/exists.ts my-new-package
```

## Related

- Use `npm-info` to get detailed package metadata when it exists.
- Use `npm-search` to find similar or alternative packages.
- Use `npm-downloads` to see package statistics.

## Error Handling

**Network errors**: The npm registry may be temporarily unavailable. Retry after a brief delay.

**Rate limiting**: While existence checks use HEAD requests (minimal bandwidth), excessive rapid requests may be rate-limited.

**Scoped packages**: Remember that scoped packages require the full name including the scope (e.g., `@babel/core`, not just `core`).