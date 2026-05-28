---
name: docusaurus-generator
description: Use this skill when you need to create end-user documentation using Docusaurus 3.x from your project. It helps in analyzing project structure, generating markdown documentation, configuring Docusaurus, and building a documentation site.
---

# Docusaurus Generator

This skill generates end-user documentation using Docusaurus 3.x by analyzing the current project.

## Workflow Overview

1. **Analyze** the project structure to understand what to document
2. **Initialize** a new Docusaurus 3.x project (or use existing)
3. **Generate** documentation content from project analysis
4. **Configure** Docusaurus settings and theme
5. **Build & Preview** the documentation site

## Step 1: Analyze Project

Before generating docs, analyze the project to identify:

- **Package structure**: Check `package.json`, monorepo setup
- **Existing docs**: Look for `docs/`, `README.md`, JSDoc comments
- **Features**: Identify main features from routes, components, APIs
- **Configuration**: Check for config files that reveal functionality

```bash
# Key files to examine
find . -name "README.md" -o -name "*.md" | head -20
ls -la docs/ 2>/dev/null
cat package.json | jq '.name, .description'
```

## Step 2: Initialize Docusaurus

Create a new Docusaurus 3.x project in the `docs-site/` directory:

```bash
npx -y create-docusaurus@latest docs-site classic --typescript
```

Or if docs already exist, skip to configuration.

## Step 3: Generate Documentation Content

### Documentation Structure

Organize docs following this structure:

```
docs-site/docs/
├── intro.md                    # Getting started
├── installation.md             # Installation guide
├── features/
│   ├── feature-1.md
│   └── feature-2.md
├── guides/
│   ├── quick-start.md
│   └── advanced-usage.md
├── configuration/
│   └── settings.md
└── faq.md
```

### Frontmatter Template

Every doc should have proper frontmatter:

```markdown
---
sidebar_position: 1
title: Page Title
description: Brief description for SEO
---

# Page Title

Content here...
```

### Content Guidelines

- **Write for end users**, not developers
- Use simple, clear language
- Include screenshots for UI features
- Add code examples where relevant
- Link between related docs

## Step 4: Configure Docusaurus

### docusaurus.config.ts

Key configuration options:

```typescript
import {themes as prismThemes} from 'prism-
// Additional configuration goes here
```