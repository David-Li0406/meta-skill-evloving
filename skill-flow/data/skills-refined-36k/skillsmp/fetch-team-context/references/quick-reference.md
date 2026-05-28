# Quick Reference Cache

For efficiency, maintain quick reference for common queries.

## Git Conventions

```yaml
commit_types:
  - feat: 새로운 기능
  - fix: 버그 수정
  - docs: 문서 변경
  - style: 코드 스타일 (포맷팅)
  - refactor: 리팩토링
  - test: 테스트 추가/수정
  - chore: 빌드, 설정 변경

commit_format: "type(scope): subject"
commit_rules:
  - 제목은 50자 이내
  - 본문은 72자에서 줄바꿈
  - 이슈 번호 연결 권장

branch_format: "{issue-number}-{title}"
```

## Workflow Phases

```yaml
phases:
  sdd_phase_1: "specify → spec.md"
  sdd_phase_2: "plan → plan.md"
  sdd_phase_3: "tasks → tasks.md"
  add_phase_4:
    - "v0.0.x CONFIG"
    - "v0.1.x PROJECT"
    - "v0.2.x TESTS"
    - "v0.3.x DATA"
    - "v0.4.x CODE"
  phase_5: "verify → PR"
```

## Quality Gates

```yaml
quality_gates:
  eslint: "0 errors, 0 warnings"
  typescript: "0 errors (strict)"
  tests: "80%+ coverage"
  debug_code: "none allowed"
  any_types: "avoid, use explicit types"
  pre_commit_hooks: "NEVER bypass"
```

## Context Summaries

### Team Codex Summary

```markdown
### Git & Commit Rules
- Commit format: `type(scope): subject`
- Types: feat, fix, docs, style, refactor, test, chore
- NEVER use --no-verify

### Code Quality Rules
- ESLint: 0 errors, 0 warnings
- TypeScript: 0 errors (strict mode)
- No debug code in commits
- No 'any' types

### Branch Strategy
- main/master: protected
- {issue-number}-{title}: feature branches
- fix/{issue-number}-{title}: bug fixes
```

### Collaboration Process Summary

```markdown
### Workflow Stages
1. Epic Creation (command-center)
2. Specification (SDD Phase 1-3)
3. Task Generation
4. Implementation (ADD Phase 4)
5. Verification
6. PR & Review
7. Deployment

### Epic → Task Flow
- Epic: High-level feature description
- Spec: Detailed requirements (spec.md)
- Plan: Technical approach (plan.md)
- Tasks: Actionable items (tasks.md)
- Issues: GitHub Issues for tracking
```

### Development Philosophy Summary

```markdown
### Architecture Principles
- DDD 4-Layer: repositories, api-clients, hooks, components
- SSR-First: Server Components by default
- 1-Hop Rule: Browser → Backend direct

### Technology Stack
- Frontend: Next.js 15, React 19
- Backend: Supabase (dev), Spring Boot (prod)
- State: React Query (server), Zustand (client)
- Testing: Vitest, Testing Library
```
