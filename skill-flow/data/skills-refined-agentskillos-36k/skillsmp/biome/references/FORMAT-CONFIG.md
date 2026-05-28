# Biome Format Configuration

Guide for Biome code formatting in projects.

## Overview

Biome provides integrated code formatting with consistent style across all projects. It's configured in `biome.json` under the `formatter` and `javascript` sections.

## Formatter Configuration

Example from `GGA Team.this project.WebApi/biome.json`:

```json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "always",
      "bracketSpacing": true,
      "bracketSameLine": false
    },
    "parser": {
      "unsafeParameterDecoratorsEnabled": true
    }
  }
}
```

## Formatter Options

### Basic Options

| Option | Value | Description |
|--------|-------|-------------|
| `enabled` | `true` | Enable formatter |
| `indentStyle` | `"space"` | Use spaces for indentation |
| `indentWidth` | `2` | Indentation width (spaces) |
| `lineWidth` | `100` | Maximum line length |

### JavaScript/TypeScript Options

| Option | Value | Description |
|--------|-------|-------------|
| `quoteStyle` | `"single"` | Use single quotes for strings |
| `semicolons` | `"always"` | Always use semicolons |
| `bracketSpacing` | `true` | Add spaces inside object brackets |
| `bracketSameLine` | `false` | Put closing bracket on new line |

### Parser Options

| Option | Value | Description |
|--------|-------|-------------|
| `unsafeParameterDecoratorsEnabled` | `true` | Enable parameter decorators in TypeScript |

## Code Formatting Examples

### Quote Style

```typescript
// Single quotes (configured)
const message = 'Hello world';
const name = 'John';

// NOT: Double quotes
const message = "Hello world"; // ❌
```

### Semicolons

```typescript
// Always use semicolons (configured)
const x = 10;
const y = 20;
const sum = x + y;

// NOT: Missing semicolons
const x = 10 // ❌
const y = 20
```

### Indentation (2 spaces)

```typescript
function example(): void {
  const data = {
    id: 1,
    name: 'Test'
  };
  
  if (data.id > 0) {
    console.log(data.name);
  }
}
```

### Bracket Spacing

```typescript
// Spaces inside brackets (configured)
const data = { id: 1, name: 'Test' };
const arr = [1, 2, 3];

// NOT: No spaces
const data = {id: 1, name: 'Test'}; // ❌
```

### Line Width (100)

```typescript
// Lines ≤ 100 characters
interface User {
  id: number;
  name: string;
  email: string;
}

// Long lines are wrapped
function processUser(userId: number, userName: string, userEmail: string): void {
  console.log(userId, userName, userEmail);
}
```

### Bracket Same Line

```typescript
// Closing bracket on new line (configured)
const user = {
  id: 1,
  name: 'John',
  email: 'john@example.com'
};

// NOT: Same line
const user = { id: 1, name: 'John', email: 'john@example.com' }; // ❌
```

## File Formatting Rules

Biome automatically formats files based on extension:

### TypeScript/JavaScript (.ts, .js)
- Uses JavaScript formatter options
- Single quotes, semicolons, 2-space indent

### JSON (.json)
- Uses JSON-specific formatter
- Consistent indentation and spacing

### CSS/SCSS (.css, .scss)
- Uses CSS-specific formatter
- Consistent spacing and ordering

## Formatting Best Practices

### 1. Import Ordering

Biome maintains consistent import order:

```typescript
// Node imports
import { Controller, Get, Post } from '@nestjs/common';
import { Injectable } from '@nestjs/core';

// Internal imports (alphabetical)
import { AgentService } from './services/agent.service';
import { UserService } from './services/user.service';
```

### 2. Object Properties

```typescript
// Consistent spacing and ordering
const user = {
  id: 1,
  name: 'John',
  email: 'john@example.com',
  active: true
};
```

### 3. Function Parameters

```typescript
// Wrap long parameter lists
function createUser(
  name: string,
  email: string,
  role: UserRole,
  permissions: string[]
): User {
  return { name, email, role, permissions };
}
```

### 4. Destructuring

```typescript
// Consistent spacing
const { id, name, email } = user;
const [first, second, third] = array;
```

## Running Formatter

### Format All Files

```bash
# Format all files in src/
npx biome format --write ./src

# Format specific file
npx biome format --write ./src/services/user.service.ts

# Check formatting without changes (dry run)
npx biome format ./src
```

### Format with Lint (Combined)

```bash
# Lint and fix (includes formatting)
npx biome lint --write ./src

# Or use npm script
npm run lint:fix
```

## Format vs Lint: Key Differences

| Feature | Format | Lint |
|---------|---------|------|
| Purpose | Code style (spacing, quotes) | Code quality (bugs, patterns) |
| Changes | Automatic, safe | May require manual review |
| Speed | Very fast | Fast (but slower than format) |
| Auto-fix | Yes | Yes (with `--write`) |

Use both commands together:
```bash
npx biome lint --write ./src  # Runs both linter and formatter
```

## Ignoring Files

To ignore specific files, create `.biomeignore`:

```ignore
# Ignore dist and build
dist/
build/

# Ignore node_modules
node_modules/

# Ignore generated files
*.generated.ts

# Ignore specific file
src/deprecated/legacy.ts
```

## Customizing Format Rules

To change format settings for a project, edit `biome.json`:

```json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100  // Change from 100 to 120
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",    // Change to "double"
      "semicolons": "always"     // Change to "asNeeded"
    }
  }
}
```

## Pre-commit Hooks

Consider adding Biome to pre-commit hooks for automatic formatting:

```bash
# Example lefthook hook
#!/bin/sh
npx biome lint --write ./src
git add -u
```

## Finding Format Examples

```bash
# View formatted files in WebApi
ls GGA Team.this project.WebApi/src/**/*.ts

# Check if files are formatted
npx biome format --check ./src

# View formatter configuration
cat GGA Team.this project.WebApi/biome.json | grep -A 20 "formatter"

# Format errors examples
npx biome format --write ./src 2>&1 | grep "formatted"
```

## Related Skills

- **`biome`** - Biome commands and lint rules
- **`webapi`** - NestJS backend code formatting
- **`testing`** - Test file formatting
