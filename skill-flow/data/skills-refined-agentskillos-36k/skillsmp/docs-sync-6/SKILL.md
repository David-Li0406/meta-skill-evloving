---
name: docs-sync
description: Analyze code and documentation, find gaps, update docs. 문서 업데이트, 코드 문서 동기화, 문서 검토.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Documentation Sync

**IMPORTANT: 모든 설명과 요약은 한국어로 작성하세요. 단, 코드 예시와 명령어는 원문 그대로 유지합니다.**

Analyze entire codebase and documentation, find gaps, update docs.

## Rules

- **Do NOT create new documentation files** unless explicitly requested
- Only `README.md` and `CLAUDE.md` in project root
- All other docs in `docs/` directory
- Single source of truth - no duplicate content
- Update existing docs, don't add new ones

## Exclude Patterns

Skip these directories/files when scanning:
- `node_modules/` - npm dependencies
- `.git/` - git internals
- `dist/`, `build/`, `out/`, `target/` - build outputs
- `coverage/` - test coverage
- `.next/`, `.nuxt/`, `.svelte-kit/` - framework cache
- `vendor/` - Go/PHP dependencies
- `__pycache__/`, `.pytest_cache/` - Python cache
- `.venv/`, `venv/`, `.env/` - Python virtual environments
- `*.min.js`, `*.bundle.js` - minified/bundled files
- Lock files: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- IDE: `.idea/`, `.vscode/`, `.settings/`

## Process

### 1. Analyze Code
- Scan all source files
- Extract public APIs, functions, classes
- Find environment variables, CLI flags
- Build code inventory

### 2. Analyze Documentation
- Read README.md, CLAUDE.md, docs/*
- Extract documented items
- Check structure and index
- Build docs inventory

### 3. Compare & Report
```
## Gap Report

Undocumented:
- function parseConfig() in src/config.ts

Orphaned (remove from docs):
- /api/legacy in docs/API.md

Mismatches:
- MAX_RETRY: docs=3, code=5
```

### 4. Update
- Fix existing documentation
- Remove orphaned content
- Do NOT create new files

### 5. Verify
- Examples work
- Links valid
- No duplicates

## Structure

```
project/
├── README.md         # Overview only
├── CLAUDE.md         # AI instructions only
└── docs/
    ├── README.md     # Index
    └── *.md          # All other docs
```

## Quality

- Clear headings, no skipped levels
- Working code examples
- No duplicate content (link instead)
- Keep docs concise
