# Project Migration Skill Template

이 템플릿은 `/jikime:migrate-2-plan --skill {project}` 명령어 실행 시 생성되는 프로젝트별 SKILL.md의 기본 구조입니다.

---

```markdown
---
name: {{PROJECT_NAME}}-migration
description: {{PROJECT_NAME}} {{SOURCE_FRAMEWORK}} → Next.js 16 migration rules
version: 1.0.0
type: project-specific
---

# {{PROJECT_NAME}} Migration Skill

## Reference Skills (Required)

이 스킬은 다음 JikiME-ADK 스킬들을 참조합니다. 마이그레이션 작업 시 필요에 따라 로드하세요.

### Core Migration Skills
| Skill | Purpose | When to Load |
|-------|---------|--------------|
| `jikime-migration-to-nextjs` | 마이그레이션 워크플로우 | 항상 |
| `jikime-framework-nextjs@16` | Next.js 16 패턴 | App Router, 'use cache' 사용 시 |
| `jikime-framework-nextjs@15` | Next.js 15 패턴 | async params 마이그레이션 시 |

### Auth Migration (if applicable)
| Skill | Purpose | When to Load |
|-------|---------|--------------|
| `jikime-migration-patterns-auth` | 인증 마이그레이션 | 인증 로직 전환 시 |
| `jikime-platform-clerk` | Clerk 통합 | Clerk 사용 시 |
| `jikime-platform-supabase` | Supabase 통합 | Supabase Auth 사용 시 |

### Additional Patterns
| Skill | Purpose | When to Load |
|-------|---------|--------------|
| `jikime-library-vercel-ai-sdk` | AI SDK 패턴 | AI 기능 구현 시 |
| `jikime-library-shadcn` | shadcn/ui 패턴 | UI 컴포넌트 사용 시 |
| `jikime-library-zod` | Zod 검증 | 폼 검증 시 |

---

## Project Analysis Summary

### Source Framework
- **Framework**: {{SOURCE_FRAMEWORK}}
- **Version**: {{SOURCE_VERSION}}
- **Router**: {{SOURCE_ROUTER}}
- **State Management**: {{SOURCE_STATE}}
- **Styling**: {{SOURCE_STYLING}}

### Target Stack
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS 4.x
- **UI**: shadcn/ui
- **State**: Zustand
- **Forms**: react-hook-form + Zod

---

## Component Mapping Rules

{{COMPONENT_MAPPING}}

---

## Coding Conventions

### File Naming
- Components: PascalCase (`TaskItem.tsx`)
- Hooks: camelCase with 'use' prefix (`useTaskStore.ts`)
- Utilities: camelCase (`formatDate.ts`)
- Types: PascalCase (`Task.ts`)

### Component Pattern

**Server Component (Default)**
```tsx
// No 'use client' directive needed
// @see jikime-framework-nextjs@16 for patterns
import { db } from '@/lib/db'

export default async function {{COMPONENT_NAME}}() {
  const data = await db.query()
  return <div>{/* render */}</div>
}
```

**Client Component**
```tsx
'use client'

// @see jikime-framework-nextjs@16 for patterns
import { useState } from 'react'

export function {{COMPONENT_NAME}}() {
  const [state, setState] = useState()
  return <div>{/* render */}</div>
}
```

### State Migration Pattern

**From {{SOURCE_STATE}} to Zustand**
```tsx
// @see jikime-migration-to-nextjs/modules/react-patterns.md
// Before: {{SOURCE_STATE_EXAMPLE}}
// After: Zustand store pattern
```

---

## Import Aliases

```json
{
  "@/*": ["src/*"],
  "@/components/*": ["src/components/*"],
  "@/stores/*": ["src/stores/*"],
  "@/lib/*": ["src/lib/*"],
  "@/types/*": ["src/types/*"]
}
```

---

## Quality Gates

Before marking migration complete:

- [ ] All components migrated
- [ ] TypeScript compiles without errors
- [ ] `npm run build` succeeds
- [ ] Core functionality verified
- [ ] Auth flow working (if applicable)

---

## Related Documentation

Load additional patterns as needed:

```
# Next.js 16 specific patterns
Skill("jikime-framework-nextjs@16")

# Auth migration
Skill("jikime-migration-patterns-auth")

# React patterns
@modules/react-patterns.md

# Full migration tutorial
@modules/migration-flow-tutorial.md
```

---

Version: 1.0.0
Generated: {{GENERATED_DATE}}
Source: jikime-migration-to-nextjs skill template
```
