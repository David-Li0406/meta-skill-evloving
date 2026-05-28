---
name: translate-articles
description: |
  Use when user says "translate articles", "translate blog posts",
  "translate missing articles", "add Spanish translations",
  "add Catalan translations", or "translate untranslated posts".
allowed-tools:
  - Read
  - Bash
---

# Translate Articles Skill

Translates blog articles to Spanish (Castellano) and Catalan using Gemini CLI.

## Usage

Run the translation script:

```bash
npx -y tsx .claude/skills/translate-articles/scripts/translate.ts
```

## What It Does

1. Scans `data/blog/` for publishable `.mdx` articles (excludes `draft: true`)
2. Identifies articles missing `.es.mdx` or `.ca.mdx` translations
3. Translates in parallel using Gemini CLI (`gemini-3-pro-preview` model)
4. Saves translated files alongside originals

## Translation Conventions

- **Frontmatter**: Translates `title` and `spoiler`, keeps `tags` in English
- **Technical terms**: Keeps terms in English that engineers commonly use (see
  list below)
- **Regional style**: Uses Castellano from Spain for Spanish, standard Catalan
- **Tone**: Informal "tú"/"tu" form
- **Formatting**: Preserves all markdown structure and code blocks

## Technical Terms to Keep in English

Software engineers are accustomed to these terms in English regardless of their
native language. Keep them untranslated:

### General Programming

- flag, flags
- commit, merge, rebase, branch, pull request, push
- bug, debug, fix
- build, deploy, release
- cache, buffer
- callback, promise, async, await
- framework, library, runtime
- script, shebang
- stack, heap, queue
- string, array, object, map, set
- type, interface, enum
- variable, constant, function, method, class

### Web & Frontend

- API, REST, GraphQL
- CLI, terminal, shell
- component, props, state, hooks
- DOM, event, handler
- frontend, backend, fullstack
- middleware, endpoint
- render, hydrate
- router, route

### Tools & Technologies

- TypeScript, JavaScript, React, Node.js, Deno, Bun
- npm, yarn, pnpm
- Git, GitHub, GitLab
- Docker, Kubernetes
- VS Code, IDE

### DevOps & Infrastructure

- CI/CD, pipeline
- container, pod
- environment, staging, production
- log, logging
- server, serverless
- test, unit test, integration test
