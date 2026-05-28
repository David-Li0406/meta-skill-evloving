# npname 📦

> Validate npm package names and check availability on the registry

[![npm version](https://img.shields.io/npm/v/npname.svg)](https://www.npmjs.com/package/npname)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agent Skill](https://img.shields.io/badge/Agent_Skill-skills.sh-blue)](https://skills.sh)

A comprehensive npm package name library that combines validation, availability checking, and registry utilities in one lightweight package.

## ✨ Features

- 🔍 **Validate** package names against npm's naming rules
- 🌐 **Check availability** on npm registry (or custom registries)
- 📦 **Batch check** multiple package names in parallel
- 🏷️ **Parse** scoped package names (`@scope/name`)
- 🔐 **Registry auth** support (Bearer, Basic, legacy tokens)
- 💡 **Suggestions** for invalid names (URL-safe alternatives)
- 📝 **Full TypeScript** support with detailed types
- 💻 **Powerful CLI** with JSON output, validation mode, and batch checking
- 🤖 **AI Agent Skill** for Claude Code, Cursor, Copilot, and 20+ AI tools

## 🤖 AI Agent Skill

This package is available as an [Agent Skill](https://skills.sh) for AI coding assistants like Claude Code, Cursor, Copilot, and more.

```bash
npx skills add dobroslavradosavljevic/npname
```

Once installed, your AI agent will know how to validate npm package names and check availability on the registry.

## 📥 Installation

```bash
# npm
npm install npname

# yarn
yarn add npname

# pnpm
pnpm add npname

# bun
bun add npname
```

## 🚀 Quick Start

```typescript
import npname from "npname";

// Check if a package name is available
const isAvailable = await npname("my-awesome-package");
console.log(isAvailable); // true or false

// Validate a package name (no network request)
const validation = npname.validate("my-package");
console.log(validation.valid); // true

// Full check: validate + check availability
const result = await npname.check("my-package");
console.log(result.available); // true, false, or null (if error)
console.log(result.validation); // ValidationResult
```

## 💻 CLI

The package includes a powerful command-line interface.

### Installation

```bash
# Global installation
npm install -g npname

# Or use with npx
npx npname my-package
```

### Usage

```bash
$ npname <name> [names...]
```

### Commands & Options

| Option           | Description                            |
| ---------------- | -------------------------------------- |
| `--validate, -v` | Validate only (no network check)       |
| `--check, -c`    | Full check with detailed output        |
| `--registry, -r` | Custom registry URL                    |
| `--timeout, -t`  | Request timeout in ms (default: 10000) |
| `--json, -j`     | Output as JSON for scripting           |
| `--quiet, -q`    | Minimal output (exit codes only)       |
| `--concurrency`  | Parallel requests (default: 4)         |
| `--help`         | Show help message                      |
| `--version`      | Show version number                    |

### Exit Codes

| Code | Description                    |
| ---- | ------------------------------ |
| 0    | All names available/valid      |
| 1    | Some names unavailable/invalid |
| 2    | Invalid arguments or errors    |

### Examples

```bash
# Check single package
$ npname my-awesome-package
✔ my-awesome-package available

# Check multiple packages
$ npname react vue angular
✔ react unavailable
✖ vue unavailable
✖ angular unavailable

# Validate without network check
$ npname "My Package" --validate
✖ My Package invalid
  ✖ name can only contain URL-friendly characters
  ⚠ name can no longer contain capital letters
  Suggestions:
    ℹ my-package

# JSON output for scripting
$ npname foo bar --json
[
  {"name": "foo", "available": false, ...},
  {"name": "bar", "available": true, ...}
]

# Custom registry
$ npname @myorg/pkg --registry https://npm.pkg.github.com/

# Quiet mode (for CI/CD)
$ npname my-pkg --quiet && echo "Available!"
```

## 📖 API Reference

### `npname(name, options?)` 🔍

Check if a package name is available on the npm registry.

```typescript
const available = await npname("chalk"); // false (taken)
const available = await npname("my-unique-pkg-xyz"); // true (available)

// With custom registry
const available = await npname("my-package", {
  registryUrl: "https://registry.mycompany.com/",
  timeout: 5000,
});
```

**Returns:** `Promise<boolean>`

---

### `npname.many(names, options?)` 📦

Check availability of multiple package names in parallel.

```typescript
const results = await npname.many(["chalk", "lodash", "my-new-pkg"]);

results.get("chalk"); // false
results.get("lodash"); // false
results.get("my-new-pkg"); // true

// With concurrency control
const results = await npname.many(names, { concurrency: 2 });
```

**Returns:** `Promise<Map<string, boolean>>`

---

### `npname.validate(name)` ✅

Validate a package name without checking the registry.

```typescript
const result = npname.validate("my-package");
// {
//   valid: true,
//   validForNewPackages: true,
//   validForOldPackages: true,
//   errors: [],
//   warnings: []
// }

const result = npname.validate("UPPERCASE");
// {
//   valid: false,
//   validForNewPackages: false,
//   validForOldPackages: true,
//   errors: [],
//   warnings: ['name can no longer contain capital letters'],
//   suggestions: ['uppercase']
// }

const result = npname.validate(".invalid");
// {
//   valid: false,
//   validForNewPackages: false,
//   validForOldPackages: false,
//   errors: ['name cannot start with a period'],
//   warnings: []
// }
```

**Returns:** `ValidationResult`

---

### `npname.check(name, options?)` 🔎

Full check: validates the name and checks availability.

```typescript
const result = await npname.check("my-package");
// {
//   name: 'my-package',
//   available: true,
//   validation: { valid: true, ... }
// }

// Invalid name returns error
const result = await npname.check(".invalid");
// {
//   name: '.invalid',
//   available: null,
//   validation: { valid: false, ... },
//   error: InvalidNameError
// }
```

**Returns:** `Promise<CheckResult>`

---

### `npname.parse(name)` 🏷️

Parse a package name into its components.

```typescript
npname.parse("my-package");
// {
//   scope: null,
//   name: 'my-package',
//   full: 'my-package',
//   isScoped: false,
//   isOrganization: false
// }

npname.parse("@myorg/my-package");
// {
//   scope: 'myorg',
//   name: 'my-package',
//   full: '@myorg/my-package',
//   isScoped: true,
//   isOrganization: true
// }
```

**Returns:** `ParsedName`

---

### `npname.registry(scope?)` 🌐

Get the registry URL for a scope (or default registry).

```typescript
npname.registry(); // 'https://registry.npmjs.org/'
npname.registry("@myorg"); // Custom registry if configured in .npmrc
```

**Returns:** `string`

---

### `npname.auth(registryUrl)` 🔐

Get authentication info for a registry URL.

```typescript
const auth = npname.auth("https://registry.npmjs.org/");
// {
//   token: 'npm_xxxx',
//   type: 'Bearer'
// }
```

**Returns:** `AuthInfo | undefined`

---

### `isScoped(name)` 🏷️

Check if a package name is scoped.

```typescript
import { isScoped } from "npname";

isScoped("@babel/core"); // true
isScoped("lodash"); // false
```

**Returns:** `boolean`

---

### `isOrganization(name)` 🏢

Check if a name is a standalone npm organization (not a scoped package).

```typescript
import { isOrganization } from "npname";

isOrganization("@babel"); // true
isOrganization("@babel/core"); // false
isOrganization("lodash"); // false
```

**Returns:** `boolean`

## 📋 Validation Rules

### ❌ Errors (Invalid for all packages)

| Rule                         | Example                    | Error Message                                    |
| ---------------------------- | -------------------------- | ------------------------------------------------ |
| Must be a string             | `null`, `undefined`, `123` | `name must be a string`                          |
| Cannot be empty              | `''`                       | `name length must be greater than zero`          |
| No leading/trailing spaces   | `' pkg '`                  | `name cannot contain leading or trailing spaces` |
| Cannot start with period     | `.hidden`                  | `name cannot start with a period`                |
| Cannot start with underscore | `_private`                 | `name cannot start with an underscore`           |
| Cannot start with hyphen     | `-pkg`                     | `name cannot start with a hyphen`                |
| Must be URL-safe             | `pkg:name`                 | `name can only contain URL-friendly characters`  |
| Not blacklisted              | `node_modules`             | `node_modules is not a valid package name`       |

### ⚠️ Warnings (Invalid for new packages only)

| Rule               | Example              | Warning Message                                            |
| ------------------ | -------------------- | ---------------------------------------------------------- |
| Max 214 characters | `very...long...name` | `name can no longer contain more than 214 characters`      |
| No uppercase       | `MyPackage`          | `name can no longer contain capital letters`               |
| No special chars   | `pkg!`               | `name can no longer contain special characters ("~'!()*")` |
| Not a core module  | `fs`, `http`         | `fs is a core module name`                                 |

### ✅ Scoped Package Relaxations

Within a scope (`@scope/name`), the package name portion can:

- Start with `-` or `_` (e.g., `@scope/-pkg`, `@scope/_pkg`)
- Use core module names (e.g., `@scope/http`)
- Use reserved names (e.g., `@scope/node_modules`)

## 🔧 Named Exports

All functions are also available as named exports:

```typescript
import {
  validate,
  parseName,
  checkAvailability,
  checkAvailabilityMany,
  getRegistryUrl,
  getAuthToken,
  parseNpmrc,
  DEFAULT_REGISTRY,
  InvalidNameError,
  // Utility functions
  isScoped,
  isOrganization,
  expandEnvVars,
  normalizeUrl,
} from "npname";

// Types
import type {
  ValidationResult,
  CheckResult,
  ParsedName,
  AuthInfo,
  AvailabilityOptions,
  BatchOptions,
} from "npname";
```

## ⚙️ Options

### AvailabilityOptions

```typescript
interface AvailabilityOptions {
  registryUrl?: string; // Custom registry URL (default: npm registry)
  timeout?: number; // Request timeout in ms (default: 10000)
}
```

### BatchOptions

```typescript
interface BatchOptions extends AvailabilityOptions {
  concurrency?: number; // Max parallel requests (default: 4)
}
```

## 🔐 Registry Authentication

The library automatically reads authentication from your `.npmrc` file:

```ini
# Bearer token (recommended)
//registry.npmjs.org/:_authToken=npm_xxxxxxxxxxxx

# Basic auth
//registry.example.com/:username=myuser
//registry.example.com/:_password=base64encodedpassword

# Legacy auth
_auth=base64encodedusername:password

# Scoped registries
@myorg:registry=https://npm.myorg.com/
//npm.myorg.com/:_authToken=${NPM_TOKEN}
```

Environment variables are automatically expanded (`${VAR}` and `$VAR` syntax).

## 🌍 Environment Variables

| Variable              | Description                                                |
| --------------------- | ---------------------------------------------------------- |
| `npm_config_registry` | Override default registry URL                              |
| `NPM_CONFIG_REGISTRY` | Override default registry URL (lowercase takes precedence) |

## 💡 Suggestions

When a package name is invalid, the library provides suggestions:

```typescript
const result = npname.validate("My Package!");
// {
//   valid: false,
//   suggestions: ['my-package']  // URL-safe, lowercase alternative
// }
```

## 🚨 Error Handling

```typescript
import { InvalidNameError } from "npname";

try {
  await npname(".invalid-name");
} catch (error) {
  if (error instanceof InvalidNameError) {
    console.log(error.message); // 'Invalid package name: .invalid-name'
    console.log(error.errors); // ['name cannot start with a period']
    console.log(error.warnings); // []
  }
}

// Batch operations throw AggregateError
try {
  await npname.many([".invalid", "-also-invalid"]);
} catch (error) {
  if (error instanceof AggregateError) {
    console.log(error.errors); // Array of InvalidNameError
  }
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

```bash
# Clone the repo
git clone https://github.com/dobroslavradosavljevic/npname.git
cd npname

# Install dependencies
bun install

# Run tests
bun test

# Build
bun run build

# Lint
bun run lint
```

## 📄 License

[MIT](LICENSE) © [Dobroslav Radosavljevic](https://github.com/dobroslavradosavljevic)

---

<p align="center">
  Made with ❤️ for the npm community
</p>
