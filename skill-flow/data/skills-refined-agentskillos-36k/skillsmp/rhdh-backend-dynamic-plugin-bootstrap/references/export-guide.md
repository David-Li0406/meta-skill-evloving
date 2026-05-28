# Dynamic Plugin Export Guide

This reference provides detailed information about exporting Backstage plugins as RHDH dynamic plugins.

## Overview

The `@red-hat-developer-hub/cli` package provides the `plugin export` command that creates a derived dynamic plugin package from an existing Backstage plugin.

## Basic Export Command

Run from the plugin's root directory (where `package.json` is located):

```bash
npx @red-hat-developer-hub/cli@latest plugin export
```

The resulting package will be in the `dist-dynamic` subdirectory.

## Backend Plugin Requirements

Backend plugins must meet these requirements for dynamic plugin compatibility:

### 1. New Backend System

Plugins must use the new backend system with `createBackendPlugin()` or `createBackendModule()`:

```typescript
import { createBackendPlugin } from '@backstage/backend-plugin-api';

export const myPlugin = createBackendPlugin({
  pluginId: 'my-plugin',
  register(env) {
    // Plugin registration
  },
});

export default myPlugin;
```

### 2. Default Export

The plugin entry point must export the plugin as default:

```typescript
// src/index.ts
export { default } from './plugin';
```

Or for alpha APIs:

```typescript
// src/alpha.ts
export { default } from './plugin';
```

## Dependency Handling

The export process categorizes dependencies into three types:

### Shared Dependencies

Shared dependencies are provided by the main RHDH application and become `peerDependencies`:

- All `@backstage/*` scoped packages are shared by default
- Not bundled in the dynamic plugin package
- Must be compatible with RHDH's versions

### Private Dependencies

Private dependencies are bundled with the plugin:

- Non-backstage dependencies
- Set as `bundleDependencies` in generated package.json
- Included in a private `node_modules` folder

### Embedded Dependencies

Embedded dependencies are merged into the plugin code:

- Packages with `-node` or `-common` suffix (auto-embedded)
- Dependencies hoisted to the plugin's top level
- Useful for workspace packages

## Command Line Options

### --shared-package

Control which packages are considered shared:

```bash
# Add a package to shared (provided by RHDH)
npx @red-hat-developer-hub/cli@latest plugin export \
  --shared-package @my-org/shared-utils

# Exclude a @backstage package from shared (bundle it)
npx @red-hat-developer-hub/cli@latest plugin export \
  --shared-package '!/@backstage/plugin-notifications/'
```

Use the `!` prefix to negate (exclude from shared).

### --embed-package

Control which packages are embedded:

```bash
# Embed a workspace package
npx @red-hat-developer-hub/cli@latest plugin export \
  --embed-package @my-org/plugin-common

# Embed multiple packages
npx @red-hat-developer-hub/cli@latest plugin export \
  --embed-package @my-org/common \
  --embed-package @my-org/utils
```

### Combined Example

```bash
npx @red-hat-developer-hub/cli@latest plugin export \
  --shared-package '!/@backstage/plugin-notifications/' \
  --embed-package @backstage/plugin-notifications-backend
```

This marks `@backstage/plugin-notifications` as private (bundled) and embeds `@backstage/plugin-notifications-backend`.

## Output Structure

After export, the `dist-dynamic` directory contains:

```
dist-dynamic/
├── package.json          # Modified for dynamic loading
├── dist/                 # Compiled JavaScript
│   ├── index.js
│   └── configSchema.json # Self-contained config schema
└── node_modules/         # Private dependencies (if any)
```

### Modified package.json

The generated `package.json` includes:

- `peerDependencies` for shared packages
- `bundleDependencies` for private packages
- Dynamic plugin metadata

## Frontend Plugin Export

Frontend plugins require Scalprum configuration. The CLI generates defaults:

```json
{
  "scalprum": {
    "name": "<package_name>",
    "exposedModules": {
      "PluginRoot": "./src/index.ts"
    }
  }
}
```

### Custom Scalprum Configuration

Add to `package.json` before export:

```json
{
  "scalprum": {
    "name": "custom-package-name",
    "exposedModules": {
      "FooModuleName": "./src/foo.ts",
      "BarModuleName": "./src/bar.ts"
    }
  }
}
```

## Troubleshooting

### Build Errors

1. Run `yarn tsc` first to check TypeScript errors
2. Ensure all dependencies are installed: `yarn install`
3. Clear build artifacts: `rm -rf dist dist-dynamic`

### Missing Dependencies

If export fails with missing dependencies:

```bash
# Install missing dev dependencies
yarn add -D <missing-package>

# Re-run export
npx @red-hat-developer-hub/cli@latest plugin export
```

### Version Conflicts

Ensure `@backstage/*` versions match your target RHDH:

1. Check `references/versions.md` for compatible versions
2. Update package.json dependencies
3. Run `yarn install`
4. Re-export

### Plugin Not Loading in RHDH

1. Verify default export exists
2. Check plugin uses new backend system
3. Verify version compatibility
4. Check RHDH logs for errors

## Best Practices

### 1. Version Lock

Lock `@backstage/*` versions to match target RHDH:

```json
{
  "dependencies": {
    "@backstage/backend-plugin-api": "1.3.1"
  }
}
```

### 2. Minimal Dependencies

Keep dependencies minimal to reduce bundle size and conflicts.

### 3. Test Locally First

Test the exported plugin locally before publishing:

```bash
# Copy to local RHDH
cp -r dist-dynamic /path/to/rhdh/dynamic-plugins-root/my-plugin-dynamic
```

### 4. Config Schema

Include a config schema for validation:

```typescript
// src/config.ts
export interface Config {
  myPlugin?: {
    /**
     * Some option description
     * @visibility frontend
     */
    someOption?: string;
  };
}
```

## Wrapping Third-Party Plugins

To add dynamic plugin support to a third-party plugin without modifying its source:

1. Create a wrapper plugin:

```bash
mkdir my-wrapper-plugin
cd my-wrapper-plugin
yarn init
```

2. Add the third-party plugin as dependency:

```json
{
  "dependencies": {
    "@third-party/plugin": "^1.0.0"
  }
}
```

3. Re-export in `src/index.ts`:

```typescript
export { default } from '@third-party/plugin';
```

4. Export as dynamic plugin:

```bash
npx @red-hat-developer-hub/cli@latest plugin export \
  --embed-package @third-party/plugin
```
