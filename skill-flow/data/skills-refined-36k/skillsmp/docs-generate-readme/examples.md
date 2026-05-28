# README Generation Examples

Complete examples of README generation from design docs.

## Example 1: effect-type-registry

### Source Design Doc

The design doc contains detailed architecture information:

- Effect-TS based system for fetching TypeScript type definitions
- Layered architecture with fault-tolerant HTTP fetching
- Disk caching with TTL and cache invalidation
- VFS generation for Twoslash integration
- Structured logging with observability events

### Source package.json

```json
{
  "name": "effect-type-registry",
  "version": "1.0.0",
  "description": "TypeScript type definition registry with caching",
  "license": "MIT"
}
```

### Generated README Output

````markdown
# effect-type-registry

Fetch and cache TypeScript type definitions from npm packages with automatic
version resolution and reliable HTTP fetching.

## Features

- Automatic version resolution for npm packages
- Reliable downloads with automatic retry on failures
- Fast repeated lookups with intelligent disk caching
- Virtual file system generation for TypeScript tooling
- Fault-tolerant with graceful error handling

## Installation

```bash
npm install effect-type-registry
```

## Quick Start

```typescript
import { createRegistry } from 'effect-type-registry';

// Create a registry with default configuration
const registry = createRegistry();

// Fetch type definitions for a package
const types = await registry.getTypeDefinitions('zod', '3.22.0');

// Generate VFS for Twoslash
const vfs = await registry.generateVFS(['zod@3.22.0']);
```

## API Overview

- `createRegistry(options?)` - Create a new type registry
- `getTypeDefinitions(package, version)` - Fetch type definitions
- `generateVFS(packages)` - Generate virtual file system
- `clearCache()` - Clear cached type definitions

See [full API documentation](./docs/api.md) for complete details.

## Documentation

- [API Reference](./docs/api.md)
- [Architecture Guide](./docs/architecture.md)
- [Examples](./examples)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup and guidelines.

## License

MIT
````

## Transformation Rules Applied

### Feature Extraction

**From design doc:**

> "Version-aware type definition fetching"

**Transformed to user benefit:**

> "Automatic version resolution for npm packages"

**From design doc:**

> "HTTP client with retry and exponential backoff"

**Transformed to user benefit:**

> "Reliable downloads with automatic retry on failures"

### Code Simplification

**Design doc example (internal):**

```typescript
const program = pipe(
  fetchPackage(name, version),
  Effect.flatMap(writeCache),
  Effect.provide(dependencies)
);
```

**README example (user-facing):**

```typescript
const types = await registry.getTypeDefinitions('zod', '3.22.0');
```

## Example 2: Update Mode Preservation

### Input: Existing README

````markdown
# my-package

[![Build](https://img.shields.io/github/workflow/status/user/repo/CI)](...)
[![npm](https://img.shields.io/npm/v/my-package.svg)](...)

A fantastic TypeScript package.

![Demo](./assets/demo.gif)

## Features

- Custom feature 1
- Custom feature 2

## Installation

```bash
npm install my-package
```

## Advanced Usage

Custom section with detailed examples...

## License

MIT
````

### Update Process

**Preserved:**

- All badges
- Demo GIF
- Advanced Usage section (custom)
- Custom features

**Updated:**

- Quick Start example
- API Overview
- Documentation links

### Output: Updated README

````markdown
# my-package

[![Build](https://img.shields.io/github/workflow/status/user/repo/CI)](...)
[![npm](https://img.shields.io/npm/v/my-package.svg)](...)

A fantastic TypeScript package.

![Demo](./assets/demo.gif)

## Features

- Feature 1 from design docs
- Feature 2 from design docs
- Custom feature 1
- Custom feature 2

## Installation

```bash
npm install my-package
```

## Quick Start

```typescript
// Updated example from design docs
import { newApi } from 'my-package';

const result = newApi({ option: 'value' });
```

## Advanced Usage

Custom section with detailed examples...

## License

MIT
````

## Common Transformations

### Technical Terms to User-Friendly Language

- "Effect-TS Layer system" → "Dependency injection"
- "VFS for Twoslash" → "Virtual file system for type checking"
- "CDN fetching with retry" → "Reliable package downloads"
- "Disk-based caching with TTL" → "Fast caching with auto-cleanup"
- "Observability events" → "Built-in logging and monitoring"

### Architecture to Features

**Design doc architecture:**

> "Uses a three-tier caching strategy with in-memory LRU cache (100
> entries), disk cache (1GB max), and CDN fallback, all with configurable
> TTL and automatic invalidation."

**README feature:**

- Fast caching with automatic cleanup
- Configurable cache size and duration
- Reliable fallback to CDN when cache misses

## Quality Checklist

Generated READMEs should meet these criteria:

- ✅ 200-500 words total length
- ✅ 3-5 feature bullet points
- ✅ Copy-paste ready quick start example
- ✅ All required sections present
- ✅ No technical jargon
- ✅ Valid markdown formatting
- ✅ Working code examples
- ✅ Proper line length (≤80 chars)
