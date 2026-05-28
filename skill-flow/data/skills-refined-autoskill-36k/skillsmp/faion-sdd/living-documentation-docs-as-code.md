---
id: living-documentation-docs-as-code
name: "Living Documentation (Docs-as-Code)"
domain: SDD
skill: faion-sdd
category: "best-practices-2026"
---

# Living Documentation (Docs-as-Code)

### Problem

Documentation becomes outdated immediately after creation:
- 4-week average time to manually create technical documents
- Documentation diverges from actual implementation
- "Documentation debt" accumulates rapidly
- Static docs in wikis become graveyard of outdated info

### Framework

#### Docs-as-Code Principles

1. **Treat docs like code** - Same systems, processes, workflows
2. **Version control** - Store in Git alongside source code
3. **CI/CD integration** - Auto-build, lint, validate on every commit
4. **Single source of truth** - Generate from code where possible

#### Living Documentation Types

```
GENERATED FROM CODE          MAINTAINED MANUALLY
-------------------          ------------------
API reference (OpenAPI)      Architecture decisions
Code comments -> docs        Design rationale
Test specs -> examples       User guides
Type definitions             Tutorials
Changelogs (from commits)    Onboarding docs
```

#### Automation Pipeline

```
Code Change
    |
+--------------------------------------+
| CI/CD Pipeline                       |
|   - Lint docs (Spectral, Vale)       |
|   - Validate links                   |
|   - Generate API docs                |
|   - Build documentation site         |
|   - Run doc tests                    |
|   - Deploy to hosting                |
+--------------------------------------+
    |
Updated Documentation
```

### Templates

#### Documentation CI Pipeline (.github/workflows/docs.yml)

```yaml
name: Documentation CI

on:
  push:
    paths:
      - 'docs/**'
      - 'src/**'
      - 'openapi.yaml'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint OpenAPI spec
        uses: stoplightio/spectral-action@v0.8
        with:
          file_glob: 'openapi.yaml'

      - name: Check broken links
        uses: gaurav-nelson/github-action-markdown-link-check@v1

      - name: Build docs
        run: npm run docs:build

      - name: Deploy to Backstage
        if: github.ref == 'refs/heads/main'
        run: npm run docs:deploy
```

#### LLM-Ready Documentation Structure

```markdown
# [Component Name]

## Summary
[1-2 sentence description for LLM context]

## Quick Start
[Code example that works immediately]

## API Reference
[Auto-generated from OpenAPI/code]

## Architecture
[Human-maintained design decisions]

## Changelog
[Auto-generated from commits]

---
*Last updated: [AUTO-DATE]*
*Generated from: [SOURCE_FILE]*
```

### Best Practices

| Practice | Description |
|----------|-------------|
| **Build artifacts** | Treat docs as build artifacts requiring CI/CD discipline |
| **Centralized storage** | Store in Backstage, GitBook, or similar developer portal |
| **Auto-rebuild** | Rebuild on code changes (ReadTheDocs, GitHub Actions) |
| **LLM-optimized** | Provide markdown versions for AI assistants (Cursor, Copilot) |
| **Test your docs** | Validate code examples actually run |

### Tools (2025-2026)

| Category | Tools |
|----------|-------|
| **Generators** | Doxygen 1.15, Sphinx 8.2, JSDoc, TypeDoc |
| **Platforms** | Mintlify, GitBook, ReadTheDocs, Backstage |
| **Linters** | Spectral (API), Vale (prose), markdownlint |
| **AI-assisted** | doc-comments-ai, ai-doc-gen, Mintlify AI |

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Docs separate from code | Co-locate documentation with source code |
| Manual API doc updates | Generate from OpenAPI spec automatically |
| No link validation | Add link checker to CI pipeline |
| Docs not searchable | Index in developer portal with full-text search |
