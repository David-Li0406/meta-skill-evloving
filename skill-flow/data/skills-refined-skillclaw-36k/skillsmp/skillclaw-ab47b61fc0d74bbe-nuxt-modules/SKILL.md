---
name: nuxt-modules
description: Use this skill when creating Nuxt modules to extend framework functionality, including published npm modules, local project modules, runtime and server extensions, and setting up CI/CD workflows.
---

# Nuxt Module Development

Guide for creating Nuxt modules that extend framework functionality.

**Related skills:** `nuxt` (basics), `vue` (runtime patterns)

## Quick Start

```bash
npx nuxi init -t module my-module
cd my-module && npm install
npm run dev        # Start playground
npm run dev:build  # Build in watch mode
npm run test       # Run tests
```

## Available Guidance

- **[references/development.md](references/development.md)** - Module anatomy, defineNuxtModule, Kit utilities, hooks
- **[references/testing-and-publishing.md](references/testing-and-publishing.md)** - E2E testing, best practices, releasing, publishing
- **[references/ci-workflows.md](references/ci-workflows.md)** - Copy-paste CI/CD workflow templates

**Load based on context:**

- Building module features? → [references/development.md](references/development.md)
- Testing or publishing? → [references/testing-and-publishing.md](references/testing-and-publishing.md)
- CI workflow templates? → [references/ci-workflows.md](references/ci-workflows.md)

## Module Types

| Type      | Location         | Use Case                         |
| --------- | ---------------- | -------------------------------- |
| Published | npm package      | `@nuxtjs/`, `nuxt-` distribution |
| Local     | `modules/` dir   | Project-specific extensions      |
| Inline    | `nuxt.config.ts` | Simple one-off hooks             |

## Project Structure

```
my-module/
├── src/
│   ├── module.ts           # Entry point
│   └── runtime/            # Injected into user's app
│       ├── components/
│       ├── composables/
│       ├── plugins/
│       └── server/
├── playground/             # Dev testing
└── test/fixtures/          # E2E tests
```

## Resources

- [Module Guide](https://nuxt.com/docs/guide/going-further/modules)
- [Nuxt Kit](https://nuxt.com/docs/api/kit)
- [Module Starter](https://github.com/nuxt/starter/tree/module)