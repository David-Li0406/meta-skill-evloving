---
name: typescript-write
description: |
  Write TypeScript/React code following Semicolon team standards with DDD architecture,
  Supabase integration, and TDD approach. Use when developing Next.js features.
tools: [Read, Write, Edit, Bash]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: typescript-write 호출` 시스템 메시지를 첫 줄에 출력하세요.

# TypeScript/React Development Skill

@./../_shared/development-workflow.md
@./../_shared/nextjs-commands.md
@./../_shared/ddd-patterns.md

## Quick Start

1. **Understand First**: 기존 코드/패턴 분석
2. **Tests First**: 실패하는 테스트 먼저 작성 (TDD)
3. **Small Increments**: 작고 테스트 가능한 단위로 작업
4. **Quality Gates**: lint/typecheck 지속 실행

## When to Use

- Next.js 기능 구현
- TypeScript/React 코드 작성
- DDD 4-layer 구조 준수 필요 시
- TDD 기반 개발 진행 시

## Code Writing Guidelines

### DDD Layer Rules

```typescript
// Repository: Server-only, Supabase RPC
import { createServerSupabaseClient } from '@/lib/supabase/server';

// API Client: Factory Pattern, Singleton
export const {domain}Client = new {Domain}ApiClient();

// Hooks: React Query + API Client
import { useQuery } from '@tanstack/react-query';

// Components: Hooks only, no business logic
import { use{Domain}s } from '../_hooks';
```

### Type Safety

```typescript
// ✅ CORRECT: Explicit types
function getPosts(params: GetPostsParams): Promise<PostsResponse>

// ❌ WRONG: any usage
function getPosts(params: any): Promise<any>
```

### Error Handling

```typescript
// ✅ CORRECT: Consistent pattern
try {
  const data = await repository.getData();
  return { data, error: null };
} catch (error) {
  return { data: null, error: error as Error };
}
```

## Integration Points

| Skill | 관계 |
|-------|------|
| `implement` | 전체 워크플로우 (v0.0.x → v0.4.x) |
| `scaffold-domain` | DDD 구조 생성 |
| `fetch-supabase-example` | Supabase 패턴 조회 |
| `verify` | Pre-PR 검증 |

## References

상세 가이드:
- [Test Templates](../_shared/test-templates.md) - 테스트 작성 템플릿
- [Commit Guide](../_shared/commit-guide.md) - 커밋 규칙
- [Quality Gates](../_shared/quality-gates.md) - 품질 기준
