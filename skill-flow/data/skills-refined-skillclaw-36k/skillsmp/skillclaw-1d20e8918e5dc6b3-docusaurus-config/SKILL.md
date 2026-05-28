---
name: docusaurus-config
description: Use this skill when working with docusaurus.config.js/ts files to validate or modify Docusaurus configuration.
---

# Docusaurus Config

## Quick Start

Configuration lives in `docusaurus.config.js` or `docusaurus.config.ts` at the project root.

```typescript
import { Config } from '@docusaurus/types';

const config: Config = {
  title: 'My Site', // Required
  url: 'https://example.com', // Required, no trailing /
  baseUrl: '/', // Required, must start and end with /

  favicon: 'img/favicon.ico',
  organizationName: 'my-org',
  projectName: 'my-project',

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        /* options */
      },
    ],
  ],
  themeConfig: {
    /* theme config */
  },
  customFields: {
    /* unknown fields go here */
  },
};

export default config;
```

## Core Principles

- **Required**: `title`, `url`, `baseUrl` are mandatory.
- **Custom fields**: Unknown fields must use the `customFields` object.
- **Validation**: Ensure `url` has no trailing slash and `baseUrl` starts and ends with `/`.
- **Plugins/themes**: Use string or `[name, options]` array format.

## Common Tasks

**Before editing**: Read the current config to preserve format (JS/TS, ESM/CommonJS).

**After editing**: Verify required fields, URL formats, and restart the dev server.

## Reference Files

See [references/detailed-guide.md](references/detailed-guide.md) for comprehensive examples.