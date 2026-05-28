# Project Structure Template

## Directory Layout

```
{project-name}/
├── package.json
├── README.md
├── .gitignore
└── docs/
    ├── .vitepress/
    │   └── config.ts
    ├── index.md
    ├── introduction/
    │   ├── overview.md
    │   └── architecture.md
    └── {module}/
        ├── index.md
        └── {topic}.md
```

## package.json

```json
{
  "name": "{project-name}",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vitepress dev docs",
    "build": "vitepress build docs",
    "preview": "vitepress preview docs"
  },
  "devDependencies": {
    "mermaid": "^11.4.0",
    "vitepress": "^1.6.3",
    "vitepress-plugin-mermaid": "^2.0.17"
  },
  "pnpm": {
    "onlyBuiltDependencies": ["esbuild"]
  }
}
```

## .gitignore

```
node_modules/
dist/
.vitepress/cache/
.vitepress/dist/
*.local
.DS_Store
```

## README.md Template

```markdown
# {Project Title}

{Brief description of what this tutorial covers}

## About

This tutorial focuses on source code learning:

- **Official docs** → How to use {project}
- **This tutorial** → How {project} is implemented

### Content Overview

- **{Module 1} Source Analysis**
  - {Topic 1}
  - {Topic 2}

- **{Module 2} Source Analysis**
  - {Topic 1}
  - {Topic 2}

## Development

\`\`\`bash
# Install dependencies
pnpm install

# Local development
pnpm dev

# Build
pnpm build

# Preview build
pnpm preview
\`\`\`

## Deployment

Static files can be deployed to any hosting platform:

- GitHub Pages
- Vercel
- Netlify

## Related Links

- [Official Documentation]({official-docs-url})
- [GitHub Repository]({github-url})

## License

MIT
```

## docs/index.md Template

```markdown
---
layout: home
hero:
  name: "{Project Title}"
  text: "{Tagline}"
  tagline: "{Description}"
  actions:
    - theme: brand
      text: Start Learning
      link: /introduction/overview
    - theme: alt
      text: View on GitHub
      link: {github-url}

features:
  - icon: 📦
    title: {Module 1}
    details: {Module 1 description}
  - icon: 🤖
    title: {Module 2}
    details: {Module 2 description}
  - icon: 🔧
    title: {Module 3}
    details: {Module 3 description}
---
```

## Chapter Frontmatter Template

```markdown
---
outline: [2, 3]
prev:
  text: '{Previous Chapter}'
  link: '/{module}/{prev-topic}'
next:
  text: '{Next Chapter}'
  link: '/{module}/{next-topic}'
---
```

## Module Index Template

```markdown
---
outline: [2, 3]
---

# {Module Name} Overview

Brief introduction to this module.

## Source Location

\`\`\`
{source-path}/
├── {file1}.go
├── {file2}.go
└── {subdir}/
    └── {file3}.go
\`\`\`

## Core Concepts

| Concept | Description | Source |
|---------|-------------|--------|
| {Concept1} | {Description} | `{path}` |
| {Concept2} | {Description} | `{path}` |

## Architecture

\`\`\`mermaid
flowchart TD
    A[Component A] --> B[Component B]
    B --> C[Component C]
\`\`\`

## Chapters

1. [{Topic 1}](./{topic1}) - {Brief description}
2. [{Topic 2}](./{topic2}) - {Brief description}
3. [{Topic 3}](./{topic3}) - {Brief description}
```
