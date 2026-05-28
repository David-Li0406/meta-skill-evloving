---
name: musubix-adr-generation
description: Guide for creating Architecture Decision Records (ADRs). Use this when asked to document architecture decisions, technology choices, or design trade-offs.
license: MIT
---

# MUSUBIX ADR Generation Skill

This skill guides you through creating Architecture Decision Records following **Article VIII - Decision Records**.

## Overview

An **ADR (Architecture Decision Record)** documents significant architectural decisions with their context and consequences.

## ADR Template

```markdown
# ADR-[NUMBER]: [Decision Title]

## ステータス
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## コンテキスト
[What is the issue that we're seeing that is motivating this decision?]

## 決定
[What is the change that we're proposing and/or doing?]

## 選択肢

### Option 1: [Name]
**メリット:**
- [Advantage 1]
- [Advantage 2]

**デメリット:**
- [Disadvantage 1]
- [Disadvantage 2]

### Option 2: [Name]
**メリット:**
- [Advantage 1]

**デメリット:**
- [Disadvantage 1]

## 結果
[What becomes easier or more difficult to do because of this change?]

## トレーサビリティ
- 関連要件: REQ-XXX-NNN
- 関連設計: DES-XXX-NNN
```

## Common ADR Topics

### 1. Technology Selection

```markdown
# ADR-001: Use TypeScript for Backend

## コンテキスト
We need to choose a programming language for the backend API.

## 決定
We will use TypeScript with Node.js.

## 選択肢

### Option 1: TypeScript + Node.js
**メリット:**
- Type safety reduces runtime errors
- Same language as frontend (code sharing)
- Large ecosystem (npm)
- Strong async/await support

**デメリット:**
- Slower than compiled languages
- Type definitions not always available

### Option 2: Go
**メリット:**
- High performance
- Strong concurrency support

**デメリット:**
- Different language from frontend
- Smaller ecosystem for web

## 結果
- Frontend/backend code sharing enabled
- Need to maintain TypeScript configuration
- Team can use consistent tooling
```

### 2. Architecture Pattern

```markdown
# ADR-002: Layered Architecture with DDD

## コンテキスト
We need to define the overall architecture pattern.

## 決定
We will use Layered Architecture with Domain-Driven Design principles.

## 選択肢

### Option 1: Layered Architecture
- Presentation → Application → Domain → Infrastructure

### Option 2: Hexagonal Architecture
- Ports and Adapters pattern

## 結果
- Clear separation of concerns
- Domain logic isolated from infrastructure
- Easier testing with dependency injection
```

### 3. Database Selection

```markdown
# ADR-003: Use PostgreSQL for Primary Database

## コンテキスト
We need a primary data store for the application.

## 決定
PostgreSQL will be our primary database.

## 選択肢

### Option 1: PostgreSQL
**メリット:**
- ACID compliance
- JSON support
- Strong ecosystem
- Free and open source

### Option 2: MongoDB
**メリット:**
- Schema flexibility
- Horizontal scaling

**デメリット:**
- Eventual consistency concerns
- Complex transactions

## 結果
- Reliable transactional data storage
- Need to manage schema migrations
- Can use JSON columns for flexibility
```

## CLI Commands

```bash
# Generate ADR from decision description
npx musubix design adr "Use React for frontend"

# List all ADRs
ls storage/design/adr/

# Generate ADR interactively
npx musubix design adr --interactive
```

## ADR Numbering

ADRs are numbered sequentially:
- ADR-001, ADR-002, ADR-003...

Never renumber existing ADRs. If an ADR is superseded, mark it as such and reference the new ADR.

## Storage Location

```
storage/design/adr/
├── ADR-001-typescript-backend.md
├── ADR-002-layered-architecture.md
├── ADR-003-postgresql-database.md
└── index.md  # ADR index
```

## ADR Index Template

```markdown
# Architecture Decision Records

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-001](./ADR-001-typescript-backend.md) | Use TypeScript for Backend | Accepted | 2026-01-04 |
| [ADR-002](./ADR-002-layered-architecture.md) | Layered Architecture | Accepted | 2026-01-04 |
```

## When to Write an ADR

- Technology selection (language, framework, database)
- Architecture patterns (layered, hexagonal, microservices)
- External integrations (APIs, services)
- Security decisions (authentication, authorization)
- Performance trade-offs (caching, scaling)

## Related Skills

- `musubix-c4-design` - Architecture diagrams
- `musubix-sdd-workflow` - Full development workflow
- `musubix-traceability` - Link ADRs to requirements
