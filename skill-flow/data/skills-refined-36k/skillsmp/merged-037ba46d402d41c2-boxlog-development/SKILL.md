---
name: boxlog-development
description: Use this skill when you need to create tRPC routers or manage release processes for the BoxLog project.
---

# BoxLog Development Skill

This skill encompasses the creation of tRPC routers and the management of release processes for the BoxLog project.

## When to Use This Skill

This skill activates automatically when the following keywords are included:

- For tRPC Router Creation:
  - "APIを作成", "エンドポイント追加"
  - "tRPCルーター", "router作成"
  - "バックエンド実装"
  - "CRUD API"

- For Releasing:
  - "リリース", "release"
  - "バージョンアップ", "version"
  - "タグを作成", "タグ付け"
  - "v0.X.0をリリース"

## tRPC Router Creation

### Router Structure

```
src/server/api/routers/{entity}/
├── index.ts        # Router merge and export
├── crud.ts         # Basic CRUD operations
├── bulk.ts         # Bulk operations (optional)
├── statistics.ts   # Statistics (optional)
└── __tests__/
    └── crud.test.ts
```

### Creation Steps

1. **Schema Definition (Zod)**

```typescript
// src/schemas/{entity}.ts
import { z } from 'zod'

export const {entity}IdSchema = z.object({
  id: z.string().uuid(),
})

export const create{Entity}Schema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  // other fields
})

export const update{Entity}Schema = create{Entity}Schema.partial()

export const {entity}FilterSchema = z.object({
  search: z.string().optional(),
  limit: z.number().min(1).max(100).default(50),
  offset: z.number().min(0).default(0),
})
```

2. **Service Layer (Business Logic)**

```typescript
// src/server/services/{entity}/index.ts
import { SupabaseClient } from '@supabase/supabase-js'

export class {Entity}ServiceError extends Error {
  constructor(public code: string, message: string) {
    super(message)
    this.name = '{Entity}ServiceError'
  }
}

// Service functions...
```

3. **CRUD Router**

```typescript
// src/server/api/routers/{entity}/crud.ts
import { z } from 'zod'

// CRUD router implementation...
```

4. **Router Merge**

```typescript
// src/server/api/routers/{entity}/index.ts
import { mergeRouters } from '@/server/api/trpc'
import { {entity}CrudRouter } from './crud'

// Merging routers...
```

5. **Add to Main Router**

```typescript
// src/server/api/root.ts
import { {entity}Router } from './routers/{entity}'

// Main router implementation...
```

### Architecture

```
┌─────────────────────┐
│   tRPC Router       │  ← Input validation + Error handling
├─────────────────────┤
│   Service Layer     │  ← Business logic
├─────────────────────┤
│   Supabase Client   │  ← Data access
└─────────────────────┘
```

## Releasing Process

### Release Workflow Overview

```
Phase 0: Preparation (Before PR Merge)
  ├── 0.1 Version Number Decision & Duplication Check
  ├── 0.2 Code Quality Check (lint, typecheck, test, build)
  ├── 0.3 Update package.json
  └── 0.4 Create Release Notes

Phase 1: PR Merge
  ├── 1.1 Create PR
  ├── 1.2 Confirm CI/CD
  └── 1.3 Merge

Phase 2: Tag Creation
  ├── 2.1 Update main branch
  ├── 2.2 Create & Push Git Tag
  └── 2.3 Confirm GitHub Release

Phase 3: Deployment Confirmation
Phase 4: Post-Release Tasks
```

### Essential Checkpoints

- **Version Duplication Check** (Phase 0.1)

```bash
# Check existing releases
gh release list

# Check for duplication
VERSION="0.X.0"  # Release version
gh release view v${VERSION} 2>/dev/null && echo "❌ Already exists!" || echo "✅ OK"
```

- **Code Quality Check** (Phase 0.2)

```bash
npm run lint && npm run typecheck && npm run test:run && npm run build
```

- **Version Update** (Phase 0.3)

```bash
# Update version command examples...
```

- **Release Notes Creation** (Phase 0.4)

```bash
# Fetch all PRs since last release
gh pr list --state merged --base main --limit 100 --json number,title,mergedAt

# Copy template for release notes
cp docs/releases/template.md docs/releases/RELEASE_NOTES_v${VERSION}.md
```

### Common Mistakes

| Mistake               | Solution                               |
| --------------------- | -------------------------------------- |
| Version Duplication    | Always check with `gh release view`   |
| Forgetting package.json update | Update before merging PR         |
| Missing Full Changelog | Use the template for release notes    |
| Incomplete PR Listing  | Ensure to fetch all merged PRs        |

## Scripts

### Version Duplication Check

```bash
.claude/skills/releasing/scripts/check-version.sh 0.X.0
```

### Fetch Merged PRs

```bash
.claude/skills/releasing/scripts/get-merged-prs.sh
```