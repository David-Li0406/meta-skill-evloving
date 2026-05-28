---
name: validate-architecture
description: Validate DDD 4-layer architecture compliance. Use when (1) after implementation completion, (2) during verification phase, (3) before PR creation, (4) architecture refactoring validation, (5) Constitution Principle I/II compliance check.
tools: [Bash, Read, Grep]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: validate-architecture 호출 - {도메인/범위}` 시스템 메시지를 첫 줄에 출력하세요.

# Validate Architecture Skill

@./../_shared/ddd-patterns.md
@./../_shared/ssr-rules.md

**Purpose**: Ensure DDD 4-layer architecture compliance and pattern adherence

## Quick Start

### When to Use

- After implementation completion
- During verification phase (Phase 5)
- Before PR creation
- Architecture refactoring validation

### What It Does

| Check | Description |
|-------|-------------|
| **Structure** | All 4 layers exist with proper naming |
| **Repository** | Server-side only, uses createServerSupabaseClient |
| **API Client** | Factory Pattern, singleton exported |
| **Hooks** | React Query, calls API client |
| **Components** | Uses hooks, no direct API/Supabase |
| **SSR** | Minimal 'use client', server-first |

## 4-Layer Structure

```text
app/{domain}/
├── _repositories/      ✓ Server-side data access
├── _api-clients/       ✓ Factory Pattern singleton
├── _hooks/             ✓ React Query wrappers
└── _components/        ✓ UI only, uses hooks
```

## Usage

```javascript
// Full architecture validation
skill: validateArchitecture();

// Validate specific domain
skill: validateArchitecture("posts");

// Quick check (structure only)
skill: validateArchitecture({ quick: true });
```

## Severity Levels

| Level | Examples | PR Impact |
|-------|----------|-----------|
| 🔴 Critical | Missing layers, Repository 'use client' | **Blocks PR** |
| 🟡 Warning | Unnecessary 'use client', missing tests | Should fix |
| 🟢 Info | Naming improvements | Nice to have |

## Constitution Compliance

> **SoT 참조**: Constitution 원칙은 `semo-core/PRINCIPLES.md`에서 관리됩니다.

- **Principle I**: DDD Architecture (NON-NEGOTIABLE)
- **Principle II**: SSR-First Development

## Related

- [Output Format](references/output-format.md) - Skill-specific output

## Related Skills

- `verify` - Uses this for architecture validation
- `scaffold-domain` - Creates validated structure
- `implement` - Ensures compliance during implementation
