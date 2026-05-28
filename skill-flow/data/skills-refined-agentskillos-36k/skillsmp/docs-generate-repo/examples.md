# Repository Documentation Generation Examples

Examples of Level 2 repository documentation generated from design docs.

## Example 1: effect-type-registry

### Source Design Docs

Module has 3 design docs:

- `architecture.md` - System architecture with Effect-TS layers
- `observability.md` - Event-based observability system
- `performance.md` - Caching and HTTP optimization

### Generated Documentation Structure

```text
pkgs/effect-type-registry/docs/
├── README.md                      # Documentation index
├── architecture/
│   ├── overview.md               # System architecture
│   └── components.md             # Component breakdown
├── guides/
│   ├── getting-started.md        # Detailed getting started
│   ├── caching.md                # Using the cache
│   ├── monitoring.md             # Monitoring and logging
│   └── performance.md            # Performance optimization
└── troubleshooting.md            # Common issues
```

### Example Generated File: docs/guides/caching.md

````markdown
# Caching

Learn how to use the built-in caching system for fast repeated
type definition lookups.

## Table of Contents

- [Overview](#overview)
- [How Caching Works](#how-caching-works)
- [Usage](#usage)
- [Examples](#examples)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview

The type registry includes automatic caching to speed up repeated
lookups. When you request type definitions for a package, they're
cached on disk so future requests are instant.

## How Caching Works

The cache has two layers:

1. **Memory cache** - Fast access for recently used packages
2. **Disk cache** - Persistent storage between runs

Cache entries automatically expire after 24 hours to ensure you
always have current type definitions.

## Usage

Caching is enabled by default. No configuration needed:

```typescript
import { createRegistry } from 'effect-type-registry';

const registry = createRegistry();

// First request: fetches from npm (slow)
const types1 = await registry.getTypeDefinitions('zod', '3.22.0');

// Second request: uses cache (fast)
const types2 = await registry.getTypeDefinitions('zod', '3.22.0');
```

## Examples

### Custom Cache Directory

```typescript
const registry = createRegistry({
  cacheDir: '~/.my-app/cache'
});
```

### Custom Cache TTL

```typescript
const registry = createRegistry({
  cacheTTL: 3600 // 1 hour in seconds
});
```

### Clear Cache

```typescript
// Clear all cached types
await registry.clearCache();

// Clear specific package
await registry.clearCache('zod');
```

## Configuration

Available cache options:

- `cacheDir` - Cache directory path (default: `~/.cache/effect-type-registry`)
- `cacheTTL` - Time to live in seconds (default: 86400 = 24 hours)
- `maxCacheSize` - Maximum cache size in bytes (default: 1GB)

## Troubleshooting

### Cache Not Working

If caching doesn't seem to work:

1. Check cache directory exists and is writable
2. Verify cache TTL hasn't expired
3. Check disk space availability

### Stale Type Definitions

If you're getting old type definitions:

```typescript
// Force refresh by clearing cache first
await registry.clearCache('zod');
const types = await registry.getTypeDefinitions('zod', '3.22.0');
```

## Related Documentation

- [Architecture Overview](../architecture/overview.md)
- [Performance Guide](./performance.md)
- [Configuration Reference](./configuration.md)
````

## Example 2: rspress-plugin-api-extractor

### Example 2 Source Design Docs

Module has 4 design docs:

- `type-loading-vfs.md` - Type loading system
- `snapshot-tracking-system.md` - Incremental builds
- `performance-observability.md` - Build performance
- `error-observability.md` - Error tracking

### Example 2 Generated Documentation Structure

```text
pkgs/rspress-plugin-api-extractor/docs/
├── README.md
├── architecture/
│   └── overview.md
├── guides/
│   ├── getting-started.md
│   ├── configuration.md
│   ├── cross-linking.md
│   └── performance.md
├── integration/
│   └── rspress.md
└── troubleshooting.md
```

### Example Generated File: docs/integration/rspress.md

````markdown
# RSPress Integration

Learn how to integrate the API Extractor plugin with your RSPress
documentation site.

## Overview

The API Extractor plugin generates markdown API documentation from
your TypeScript source code and integrates it seamlessly into your
RSPress site.

## Installation

```bash
npm install rspress-plugin-api-extractor
```

## Configuration

Add the plugin to your RSPress configuration:

```typescript
// rspress.config.ts
import { pluginApiExtractor } from 'rspress-plugin-api-extractor';

export default {
  plugins: [
    pluginApiExtractor({
      apiJsonPath: './lib/packages/my-package.api.json',
      outputDir: './docs/en/api'
    })
  ]
};
```

## Complete Example

### Step 1: Generate API Extractor Model

First, configure API Extractor to generate the model file:

```json
{
  "projectFolder": ".",
  "mainEntryPointFilePath": "./src/index.ts",
  "apiReport": {
    "enabled": false
  },
  "docModel": {
    "enabled": true,
    "apiJsonFilePath": "./lib/packages/<unscopedPackageName>.api.json"
  }
}
```

### Step 2: Add Plugin to RSPress

```typescript
import { pluginApiExtractor } from 'rspress-plugin-api-extractor';

export default {
  plugins: [
    pluginApiExtractor({
      apiJsonPath: './lib/packages/my-package.api.json',
      outputDir: './docs/en/api',
      categories: {
        classes: 'Classes',
        interfaces: 'Interfaces',
        functions: 'Functions',
        types: 'Types'
      }
    })
  ]
};
```

### Step 3: Build Documentation

```bash
npm run build
```

The plugin will generate markdown files in `docs/en/api/` organized
by category.

## Common Patterns

### Custom Categories

```typescript
pluginApiExtractor({
  categories: {
    classes: 'API Classes',
    functions: 'API Functions',
    types: 'Type Definitions'
  }
})
```

### Multiple Packages

```typescript
plugins: [
  pluginApiExtractor({
    apiJsonPath: './lib/packages/package-a.api.json',
    outputDir: './docs/en/package-a/api'
  }),
  pluginApiExtractor({
    apiJsonPath: './lib/packages/package-b.api.json',
    outputDir: './docs/en/package-b/api'
  })
]
```

## Troubleshooting

### Plugin Not Generating Docs

If the plugin doesn't generate documentation:

1. Verify API Extractor model file exists at `apiJsonPath`
2. Check RSPress build output for errors
3. Ensure `outputDir` is writable

### Cross-Links Not Working

If type cross-links in code blocks don't work:

1. Ensure Shiki transformer is configured
2. Verify type definitions are available
3. Check browser console for errors

## Related Documentation

- [Configuration Guide](../guides/configuration.md)
- [Cross-Linking Guide](../guides/cross-linking.md)
- [Architecture Overview](../architecture/overview.md)
````

## Documentation Structure Patterns

### Architecture Documentation

**Pattern:**

```text
docs/architecture/
├── overview.md      # High-level system design
├── components.md    # Component breakdown
└── data-flow.md     # How data flows through system
```

**Content:**

- System architecture diagrams
- Component responsibilities
- Design decisions explained
- Integration points

### Topic Guides

**Pattern:**

```text
docs/guides/
├── getting-started.md  # Entry point
├── {feature-1}.md      # Major features
├── {feature-2}.md
└── advanced.md         # Advanced patterns
```

**Content:**

- Feature-specific guides
- Practical examples
- Best practices
- Common patterns

### Integration Guides

**Pattern:**

```text
docs/integration/
├── {tool-1}.md
└── {tool-2}.md
```

**Content:**

- Integration setup
- Configuration examples
- Complete working code
- Troubleshooting

## Quality Checklist

Generated repository docs should meet:

- ✅ 500-2000 words per document
- ✅ At least 2 code examples per guide
- ✅ Table of contents for docs >800 words
- ✅ Cross-references to related topics
- ✅ Troubleshooting section
- ✅ Valid GitHub-flavored markdown
- ✅ Working, tested code examples
