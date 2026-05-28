---
name: project-context
description: cm-template 프로젝트의 아키텍처, 개발 패턴, 워크플로우 컨텍스트를 제공합니다. Use when (1) 새 도메인/기능 구현 시, (2) 아키텍처 결정 필요 시, (3) 코드 패턴 확인 시, (4) DDD 구조 이해 필요 시.
tools: [Read]
---

# Project Context Skill

**Purpose**: cm-template 프로젝트의 핵심 컨텍스트 제공

## Project Overview

**Semicolon Community Template** - 세미콜론 커뮤니티 에코시스템을 위한 솔루션 기반 커뮤니티 서비스 템플릿

- **Core Stack**: Next.js 14 + TypeScript + Supabase + Shadcn/ui
- **Methodology**: SDD (Spec-Driven) + ADD (Agent-Driven)

## DDD 4-Layer Architecture

```text
app/{domain}/
├── _repositories/    # 서버사이드 데이터 접근
├── _api-clients/     # 브라우저 HTTP 통신
├── _hooks/           # React 상태 관리
├── _components/      # 도메인 전용 UI
└── page.tsx
```

## Layer Responsibilities

| Layer | 역할 | 핵심 규칙 |
|-------|------|----------|
| **Repository** | 서버사이드 데이터 | `'use client'` 금지 |
| **API Client** | 브라우저 HTTP | Factory Pattern 필수 |
| **Hooks** | React 상태 | React Query 사용 |
| **Components** | 도메인 UI | 비즈니스 로직 금지 |

## Data Flow (1-Hop Rule)

```text
Browser → API Client → Backend → Repository → Supabase
```

**❌ 금지**: 2-hop (Browser → Next.js → Spring Boot)

## Development Workflow

| Phase | 산출물 |
|-------|--------|
| SDD 1-3 | spec.md → plan.md → tasks.md |
| ADD v0.0.x~v0.4.x | CONFIG → PROJECT → TESTS → DATA → CODE |

## Related Skills

- `validate-architecture` - DDD 4-layer 준수 검사
- `scaffold-domain` - 도메인 구조 스캐폴딩
- `fetch-supabase-example` - core-supabase 참조 조회

## References

For detailed documentation, see:

- [DDD Architecture](references/ddd-architecture.md) - 구조, 원칙, layer 책임, SSR 가이드
- [Workflow Patterns](references/workflow-patterns.md) - SDD/ADD, 명령어, 컴포넌트, 환경변수
