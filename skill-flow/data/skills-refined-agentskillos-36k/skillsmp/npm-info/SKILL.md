---
name: npm-info
description: Get detailed metadata for an npm package including versions, dependencies, maintainers, and repository information. Use when the user asks for package details, version history, or package metadata.
---

# Get npm Package Information

Retrieve detailed metadata for a specific npm package.

## Usage

```bash
npx tsx scripts/info.ts <package-name> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `package-name` | Yes | The exact package name (case-sensitive) |

### Options

| Option | Description |
|--------|-------------|
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
react
------
Description: React is a JavaScript library for building user interfaces.
Latest: 18.2.0
License: MIT
Homepage: https://react.dev
Repository: https://github.com/facebook/react

Versions (last 5):
  18.2.0 - Published 2022-06-14
  18.1.0 - Published 2022-04-26
  18.0.0 - Published 2022-03-29
  17.0.2 - Published 2021-03-10
  17.0.1 - Published 2020-12-20

Maintainers:
  - @hzoo
  - @acdlite
```

## Script Execution (Preferred)

```bash
npx tsx scripts/info.ts <package-name> [options]
```

Options:
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the npm-registry plugin directory: `~/.claude/plugins/cache/npm-registry/`

## Package Metadata API

```
GET https://registry.npmjs.org/{package}
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `package` | Yes | The exact package name (case-sensitive) |

### Examples

Get package metadata:
```
https://registry.npmjs.org/react
```

## Response Format

The response contains comprehensive package metadata:

- **`name`** - Package name
- **`versions`** - Object mapping version numbers to full version metadata
- **`dist-tags`** - Tags like `latest`, `next`, `canary`
- **`time`** - Timestamps for each version publish
- **`maintainers`** - Array of package maintainers
- **`description`** - Package description
- **`homepage`** - Project homepage URL
- **`repository`** - Repository information (type, URL)
- **`bugs`** - Bug tracker URL or email
- **`license`** - License identifier
- **`author`** - Author information
- **`keywords`** - Array of keywords
- **`dependencies`** - Production dependencies (per version)
- **`devDependencies`** - Development dependencies (per version)
- **`peerDependencies`** - Peer dependencies (per version)

## Repository URL Formats

The registry accepts various repository URL formats:
- `https://github.com/owner/repo`
- `git+https://github.com/owner/repo`
- `git@github.com:owner/repo`
- `ssh://git@github.com/owner/repo`

These are automatically parsed and normalized.

## Caching

Package metadata is cached for 6 hours. Versions change infrequently, and most metadata remains stable between releases.

Use the `--no-cache` flag to bypass the cache.

## Related

- Use `npm-search` to find packages before getting details
- Use `npm-exists` for a quick availability check
- Use `npm-downloads` to see usage statistics

## Error Handling

**Package not found**: If the package doesn't exist, you'll receive a 404 response. Use `npm-exists` to check availability first.

**Invalid package name**: Package names must be valid npm package names (lowercase, can contain hyphens, underscores, periods).

**Scope issues**: For scoped packages like `@babel/core`, include the scope in the name.
