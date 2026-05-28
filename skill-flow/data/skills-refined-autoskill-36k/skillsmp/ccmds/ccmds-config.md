# ccmds Configuration

Configuration file schema and patterns for `.ccmdsrc`.

## Quick Start

```bash
# Create config file
ccmds init

# Create with specific directories
ccmds init -d ./docs ./wiki

# View current config
ccmds config

# View config file path
ccmds config --path
```

---

## Config File Locations

The CLI looks for config files in this order:

1. **Current directory**: `.ccmdsrc`, `.ccmdsrc.json`, `ccmds.config.json`
2. **Parent directories**: Walks up to root (monorepo support)
3. **Home directory**: `~/.ccmdsrc`
4. **Built-in defaults**: Used when no config found

---

## Full Schema

```json
{
  "documentDirectories": [
    "./docs",
    { "name": "api", "path": "./api-docs", "description": "API reference" }
  ],
  "exclude": ["**/node_modules/**", "**/.*/**"],
  "outputMode": "json",
  "limit": 10,
  "fuzzy": {
    "threshold": 0.4,
    "weights": {
      "title": 2,
      "description": 1.5,
      "tags": 1.5,
      "body": 1
    }
  },
  "preview": {
    "maxLines": 20,
    "topResults": 600,
    "midResults": 300,
    "otherResults": 150
  },
  "frontmatterFields": ["title", "description", "tags", "category", "summary", "keywords"],
  "extensions": [".md", ".markdown"]
}
```

---

## Options Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `documentDirectories` | `string[] \| object[]` | `["."]` | Directories to search (strings or named entries) |
| `exclude` | `string[]` | `[]` | Glob patterns to exclude |
| `outputMode` | `string` | `"json"` | Default output mode |
| `limit` | `number` | `10` | Default result limit |
| `fuzzy.threshold` | `number` | `0.4` | Match threshold (0=exact, 1=loose) |
| `fuzzy.weights` | `object` | See above | Field weights for scoring |
| `preview.maxLines` | `number` | `20` | Max lines for context-aware previews |
| `preview.topResults` | `number` | `600` | Fallback preview chars for top 3 results |
| `preview.midResults` | `number` | `300` | Fallback preview chars for results 4-7 |
| `preview.otherResults` | `number` | `150` | Fallback preview chars for remaining |
| `frontmatterFields` | `string[]` | See above | Frontmatter fields to include |
| `extensions` | `string[]` | `[".md", ".markdown"]` | File extensions |
| `cache.enabled` | `boolean` | `false` | Enable result caching |
| `cache.ttl` | `number` | `300` | Cache expiration in seconds |
| `cache.maxEntries` | `number` | `50` | Max cached queries |

---

## Named Documentation Entries

Give directories names for targeted searching with `--doc`:

```json
{
  "documentDirectories": [
    "./general-docs",
    { "name": "api", "path": "./api-reference", "description": "API documentation" },
    { "name": "guides", "path": "./tutorials", "description": "User guides" }
  ]
}
```

Then filter searches:

```bash
ccmds find "auth" --doc api      # Only search api-reference
ccmds list --doc guides          # Only list tutorial files
ccmds grep "TODO" --doc api      # Grep only in API docs
```

**Name matching is prefix-based**: `--doc api` matches `api`, `api-reference`, `api-v2`, etc.

### Named Entry Format

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Short identifier for `--doc` filtering |
| `path` | Yes | Directory path (relative or absolute) |
| `description` | No | Human-readable description |

---

## Caching

Enable caching to speed up repeated searches:

```json
{
  "cache": {
    "enabled": true,
    "ttl": 300,
    "maxEntries": 50
  }
}
```

```bash
ccmds cache stats    # View cache info
ccmds cache clear    # Clear cache
ccmds find "x" --no-cache  # Skip cache
```

---

## Example Configurations

### Simple Project

```json
{
  "documentDirectories": ["./docs"],
  "exclude": ["**/node_modules/**"]
}
```

### Documentation-Heavy Project

```json
{
  "documentDirectories": [
    "./docs/user-guide",
    "./docs/api-reference",
    "./docs/tutorials"
  ],
  "exclude": ["**/drafts/**", "**/archive/**"],
  "limit": 15
}
```

### Monorepo

```json
{
  "documentDirectories": ["./docs", "./packages/*/docs"],
  "exclude": ["**/node_modules/**", "**/dist/**", "**/.*/**"]
}
```

### Monorepo with Named Docs

```json
{
  "documentDirectories": [
    { "name": "web", "path": "./packages/web/docs", "description": "Web app docs" },
    { "name": "api", "path": "./packages/api/docs", "description": "API docs" },
    { "name": "shared", "path": "./docs/shared", "description": "Shared documentation" }
  ]
}
```

Use `--doc web`, `--doc api`, or `--doc shared` to filter searches.

### Strict Search (Less Fuzzy)

```json
{
  "documentDirectories": ["./docs"],
  "fuzzy": { "threshold": 0.2 }
}
```

---

## Exclude Patterns

| Pattern | Matches |
|---------|---------|
| `**/node_modules/**` | Any node_modules directory |
| `**/.*/**` | Hidden directories |
| `**/*.draft.md` | Files ending in .draft.md |
| `archive/**` | archive at project root |

### Common Excludes

```json
{
  "exclude": [
    "**/node_modules/**",
    "**/.*/**",
    "**/dist/**",
    "**/build/**",
    "**/archive/**",
    "**/*.draft.md"
  ]
}
```

---

## CLI Override Behavior

CLI options always override config:

```bash
ccmds find "auth"                    # Uses config defaults
ccmds find "auth" -l 20              # Overrides limit
ccmds find "auth" -o json            # Overrides outputMode
ccmds find "auth" ./other/docs       # Overrides directories
ccmds find "auth" --no-config        # Ignores config entirely
ccmds find "auth" --config ./custom.json  # Uses specific config
```
