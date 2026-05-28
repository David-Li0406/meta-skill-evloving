---
name: jikime-workflow-codemap
description: Comprehensive codebase architecture mapping with AST analysis and dependency visualization
version: 1.0.0
tags: ["workflow", "codemap", "architecture", "documentation", "ast", "dependencies"]
triggers:
  keywords: ["codemap", "architecture map", "dependency graph", "code structure", "아키텍처", "코드맵"]
  phases: ["sync"]
  agents: ["documenter", "manager-docs", "architect"]
  languages: []
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~6000
user-invocable: false
context: fork
agent: documenter
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Codemap Generation Skill

Generate comprehensive, accurate architecture documentation from actual codebase analysis.

## Philosophy

```
Documentation from reality, not imagination:
├─ AST analysis ensures accuracy
├─ Dependency graphs reveal true relationships
├─ Auto-detection reduces manual effort
├─ Timestamps track freshness
└─ Single source of truth: the code itself
```

---

## How It Works

### Generation Pipeline

```
Phase 1: Discovery
    ↓
  Detect framework, language, project type
    ↓
  Identify entry points and key files
    ↓
Phase 2: Analysis
    ↓
  AST parsing (ts-morph for TS/JS)
    ↓
  Dependency graph (madge)
    ↓
  Pattern recognition (MVC, Clean, etc.)
    ↓
Phase 3: Generation
    ↓
  Generate structured codemaps
    ↓
  Create ASCII diagrams
    ↓
  Build relationship tables
    ↓
Phase 4: Validation
    ↓
  Verify paths exist
    ↓
  Check link targets
    ↓
  Report coverage statistics
```

---

## Analysis Tools

### 1. AST Analysis with ts-morph

For TypeScript/JavaScript projects:

```typescript
import { Project } from 'ts-morph'

const project = new Project({
  tsConfigFilePath: 'tsconfig.json',
})

// Get all source files
const sourceFiles = project.getSourceFiles('src/**/*.{ts,tsx}')

// Extract exports
sourceFiles.forEach(file => {
  const exports = file.getExportedDeclarations()
  exports.forEach((declarations, name) => {
    console.log(`Export: ${name}`)
  })
})

// Map imports
sourceFiles.forEach(file => {
  const imports = file.getImportDeclarations()
  imports.forEach(imp => {
    console.log(`Import from: ${imp.getModuleSpecifierValue()}`)
  })
})
```

### 2. Dependency Graph with madge

```bash
# Install madge
npm install -D madge

# Generate visual graph
npx madge --image docs/CODEMAPS/assets/dependency-graph.svg src/

# Find circular dependencies
npx madge --circular src/

# Generate JSON for processing
npx madge --json src/ > dependency-graph.json
```

### 3. JSDoc Extraction

```bash
# Extract documentation from code
npx jsdoc2md src/**/*.ts > docs/API.md

# Or use TypeDoc for TypeScript
npx typedoc --out docs/api src/
```

---

## Output Structure

### Directory Layout

```
docs/
├── CODEMAPS/
│   ├── INDEX.md              # Architecture overview
│   ├── frontend.md           # Frontend structure
│   ├── backend.md            # Backend/API structure
│   ├── database.md           # Database schema
│   ├── integrations.md       # External services
│   └── assets/
│       ├── dependency-graph.svg
│       ├── frontend-components.svg
│       └── data-flow.svg
├── GUIDES/
│   ├── setup.md              # Setup instructions
│   ├── development.md        # Development guide
│   └── deployment.md         # Deployment guide
└── API/
    └── reference.md          # API documentation
```

### Codemap File Format

Each codemap follows a consistent structure:

```markdown
# [Area] Codemap

**Last Updated:** YYYY-MM-DD
**Version:** X.Y.Z
**Entry Points:** [list of main files]

## Overview
[Brief description of this area]

## Architecture
[ASCII diagram showing component relationships]

## Key Modules

| Module | Purpose | Exports | Dependencies |
|--------|---------|---------|--------------|
| ... | ... | ... | ... |

## Data Flow
[Description of data flow through this area]

## External Dependencies
- package@version - Purpose
- ...

## Related Codemaps
- [Related Area](./related.md)
```

---

## Framework-Specific Patterns

### Next.js App Router

```markdown
## Routing Structure

| Route | Component | Type | Middleware |
|-------|-----------|------|------------|
| / | page.tsx | Server | auth |
| /api/* | route.ts | API | rate-limit |
| /dashboard | layout.tsx | Client | auth |

## Server Components vs Client Components

- Server Components: app/**, components/server/**
- Client Components: components/client/** (use client)
- Shared: lib/**, utils/**
```

### Express/Fastify API

```markdown
## Route Hierarchy

```
/api
├── /auth
│   ├── POST /login
│   ├── POST /register
│   └── POST /logout
├── /users
│   ├── GET /
│   ├── GET /:id
│   ├── POST /
│   └── PATCH /:id
└── /admin (protected)
    └── ...
```

## Middleware Chain

Request → [cors] → [helmet] → [auth] → [validate] → Handler → Response
```

### Database Models

```markdown
## Entity Relationship

```
┌──────────────┐     ┌──────────────┐
│    User      │────<│    Post      │
├──────────────┤     ├──────────────┤
│ id           │     │ id           │
│ email        │     │ userId (FK)  │
│ name         │     │ title        │
│ createdAt    │     │ content      │
└──────────────┘     └──────────────┘
        │
        └────────────<┌──────────────┐
                      │   Comment    │
                      ├──────────────┤
                      │ id           │
                      │ userId (FK)  │
                      │ postId (FK)  │
                      │ content      │
                      └──────────────┘
```
```

---

## Orchestrator Integration

### J.A.R.V.I.S. (Development)

```
During /jikime:3-sync:
  → Generate/update codemaps for changed modules
  → Validate README references
  → Report documentation coverage

Predictive Suggestions:
  → "Frontend structure changed, suggest regenerating frontend.md"
  → "New API endpoints detected, update backend.md"
```

### F.R.I.D.A.Y. (Migration)

```
During migration phases:
  → Generate as_is_spec.md from source codemaps
  → Track architecture differences (source vs target)
  → Update codemaps after each module migration
  → Generate migration-specific documentation

Output Format:
  → Include source/target comparison tables
  → Track migration progress in codemaps
```

---

## Best Practices

### DO

1. **Generate from code** - Never manually write what can be extracted
2. **Include timestamps** - Always add Last Updated date
3. **Use consistent format** - Follow the template structure
4. **Keep files focused** - One area per codemap file
5. **Validate paths** - Ensure all referenced files exist
6. **Update on changes** - Regenerate after significant code changes
7. **Include diagrams** - ASCII art is token-efficient and clear

### DON'T

1. **Don't guess** - If unsure, analyze the code
2. **Don't over-document** - Focus on architecture, not implementation details
3. **Don't duplicate** - Reference other codemaps instead of copying
4. **Don't ignore updates** - Stale documentation is worse than none
5. **Don't skip validation** - Always verify paths and links

---

## Automation

### Git Hooks Integration

```json
{
  "hooks": {
    "pre-commit": [
      {
        "matcher": "src/**/*",
        "command": "jikime-adk codemap check --changed-only",
        "message": "Checking if codemaps need update"
      }
    ]
  }
}
```

### CI/CD Integration

```yaml
# GitHub Actions
- name: Validate Codemaps
  run: |
    # Check codemaps are up to date
    jikime-adk codemap validate --strict

    # Regenerate if needed
    if [ $? -ne 0 ]; then
      jikime-adk codemap all --refresh
      git diff --exit-code docs/CODEMAPS/
    fi
```

---

## Maintenance Schedule

| Frequency | Action |
|-----------|--------|
| **After major features** | Full codemap regeneration |
| **Weekly** | Validate paths and links |
| **Before release** | Complete documentation audit |
| **On PR** | Check changed modules' codemaps |

---

## Works Well With

- `jikime-foundation-core`: Core workflow integration
- `jikime-workflow-spec`: SPEC document creation
- `jikime-workflow-ddd`: DDD methodology alignment
- `jikime-foundation-claude`: Claude Code patterns
- `jikime-domain-frontend`: Frontend-specific patterns
- `jikime-domain-backend`: Backend-specific patterns

---

Last Updated: 2026-01-25
Version: 1.0.0
Integration: AST analysis (ts-morph), Dependency graphs (madge), J.A.R.V.I.S./F.R.I.D.A.Y.
