# Workflow & Patterns

## Development Workflow (SDD + ADD)

### SDD Phases (1-3)

1. **Specify** (`/speckit.specify`): `specs/{domain}/spec.md` 생성
2. **Plan** (`/speckit.plan`): `specs/{domain}/plan.md` 생성
3. **Tasks** (`/speckit.tasks`): `specs/{domain}/tasks.md` 생성

### ADD Phases (4)

- **v0.0.x**: CONFIG (dependencies, spikes)
- **v0.1.x**: PROJECT (DDD scaffolding)
- **v0.2.x**: TESTS (Repository, Hooks, Components tests)
- **v0.3.x**: DATA (Models, Supabase schemas)
- **v0.4.x**: CODE (Repository → API Client → Hooks → Components)

## Key Commands

```bash
# Development
npm run dev          # localhost:3000
npm run build        # Production build
npm run lint         # ESLint

# Testing
npm test             # Run all tests
npm run test:watch   # Watch mode
npm run test:coverage

# Shadcn/ui
npx shadcn-ui@latest add [component]

# Supabase Types
npx supabase gen types typescript --project-id [id] > lib/supabase/database.types.ts
```

## Component Development (Atomic Design)

| 레벨 | 설명 | 비즈니스 로직 | 예시 |
|------|------|--------------|------|
| **Atoms** | Shadcn/ui 기본 | ❌ 금지 | Button, Input, Card |
| **Molecules** | 2-3개 Atoms 조합 | ❌ 금지 | FormField, UserAvatar |
| **Organisms** | 복잡한 기능 | Container 패턴 | LoginForm, Navigation |
| **Templates** | 페이지 레이아웃 | ❌ 금지 | CommunityLayout |

### 핵심 규칙

- **Container Pattern**: `SidebarContainer` (로직) → `Sidebar` (UI)
- **Props over imports**: 데이터/콜백은 props로 전달
- **Never mix**: UI 컴포넌트에서 auth/API 직접 import 금지

## Environment Variables

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_ROLE_KEY=eyJxxx...

# API Mode
NEXT_PUBLIC_API_MODE=next-api    # "next-api" | "spring"
NEXT_PUBLIC_SPRING_API_URL=http://localhost:8080
```

## Supabase Patterns

### Schema Verification Priority

1. **Supabase MCP** (실시간 클라우드 스키마) - 우선
2. **database.types.ts** (outdated 가능)
3. **core-supabase** (참조 구현)

### Storage Buckets

| 버킷 | 용도 | 예시 |
|------|------|------|
| `public-bucket` | 공개 파일 | 프로필 이미지, 게시물 첨부 |
| `private-bucket` | 비공개 파일 | 민감 문서, 관리자 자료 |

### Best Practices

- All tables: RLS enabled
- User identification: `auth.uid()`
- Naming: snake_case columns, plural tables
- Always generate types after schema changes

## Performance Targets

| 지표 | 목표 | 현재 |
|------|------|------|
| LCP | < 2.5s | ✅ |
| FID | < 100ms | ✅ |
| CLS | < 0.1 | ✅ |
| Initial Bundle | < 500KB | 129KB ✅ |
