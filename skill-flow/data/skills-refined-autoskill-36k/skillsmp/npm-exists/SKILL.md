---
name: npm-exists
description: Check if an npm package name exists in the registry. Use when the user asks if a package name is available, wants to check package existence, or verify if a package is published.
---

# Check npm Package Existence

Check if a package name exists in the npm registry.

## Usage

```bash
npx tsx scripts/exists.ts <package-name> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `package-name` | Yes | The exact package name to check (case-sensitive) |

### Options

| Option | Description |
|--------|-------------|
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

Package exists:
```
✓ Package "react" exists
  URL: https://www.npmjs.com/package/react
  Published: Yes
```

Package does not exist:
```
✗ Package "my-awesome-pkg-12345" does not exist
  The name is available for use
```

## Script Execution (Preferred)

```bash
npx tsx scripts/exists.ts <package-name> [options]
```

Options:
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the npm-registry plugin directory: `~/.claude/plugins/cache/npm-registry/`

## Existence Check API

```
HEAD https://registry.npmjs.org/{package}
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `package` | Yes | The exact package name to check (case-sensitive) |

### Examples

Check if a package exists:
```
HEAD https://registry.npmjs.org/react
```

For scoped packages:
```
HEAD https://registry.npmjs.org/@babel/core
```

## Response Interpretation

**Package exists** - HTTP 200 OK
- The package is published and available
- You can use `npm info` or `npm install` with this name

**Package does not exist** - HTTP 404 Not Found
- The package name is available for use
- No package with this exact name exists in the registry

Before publishing a new package, verify the name is available:
```bash
npx tsx exists.ts my-new-package
```

### Validate Package Name
Confirm a package exists before installing or using it:
```bash
npx tsx exists.ts some-dependency
```

### Scoped Packages
Check scoped package names:
```bash
npx tsx exists.ts @myorg/package-name
```

## Naming Rules

Package names must:
- Start with a letter, number, `@`, or `_`
- Contain only URL-safe characters (letters, numbers, hyphens, underscores)
- Not start with `.` or `_`
- Not contain spaces
- Not exceed 214 characters
- Not be the same as a node.js/core module name

Scoped packages (`@scope/name`) have additional rules:
- Scope must be the username of the npm owner
- Scope must be followed by a slash

## Caching

Existence checks are cached for 1 hour. Package availability changes infrequently, so short cache times provide a good balance between freshness and performance.

Use the `--no-cache` flag to bypass the cache.

## Related

- Use `npm-info` to get detailed package metadata when it exists
- Use `npm-search` to find similar or alternative packages
- Use `npm-downloads` to see package statistics

## Error Handling

**Network errors**: The npm registry may be temporarily unavailable. Retry after a brief delay.

**Rate limiting**: While existence checks use HEAD requests (minimal bandwidth), excessive rapid requests may be rate-limited.

**Scoped packages**: Remember that scoped packages require the full name including the scope (e.g., `@babel/core`, not just `core`).
