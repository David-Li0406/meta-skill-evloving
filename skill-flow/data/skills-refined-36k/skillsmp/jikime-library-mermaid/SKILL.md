---
name: jikime-library-mermaid
description: Enterprise Mermaid diagramming skill for Claude Code using MCP Playwright. Use when creating architecture diagrams, flowcharts, sequence diagrams, or visual documentation.
version: 1.0.0
tags: ["library", "mermaid", "diagrams", "documentation", "flowchart", "visualization"]
triggers:
  keywords: ["mermaid", "diagram", "flowchart", "sequence", "다이어그램", "시퀀스"]
  phases: ["sync"]
  agents: ["manager-docs"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
user-invocable: false
---

# Mermaid Diagram Guide

Mermaid 11+ 다이어그램 작성을 위한 간결한 가이드.

## Quick Reference

| 다이어그램 | 용도 |
|-----------|------|
| **Flowchart** | 프로세스, 결정 트리 |
| **Sequence** | 상호작용, API 흐름 |
| **Class** | 클래스 관계, 구조 |
| **ER** | 데이터베이스 스키마 |
| **State** | 상태 머신 |
| **C4** | 시스템 아키텍처 |

## Flowchart

```mermaid
flowchart TD
    A[Start] --> B{Is valid?}
    B -->|Yes| C[Process]
    B -->|No| D[Error]
    C --> E[End]
    D --> E
```

### 노드 형태

```mermaid
flowchart LR
    A[Rectangle] --> B(Rounded)
    B --> C{Diamond}
    C --> D([Stadium])
    D --> E[[Subroutine]]
    E --> F[(Database)]
```

### 서브그래프

```mermaid
flowchart TB
    subgraph Frontend
        A[React App] --> B[API Client]
    end
    subgraph Backend
        C[API Server] --> D[Database]
    end
    B --> C
```

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant App
    participant API
    participant DB

    User->>App: Click Login
    App->>API: POST /auth/login
    API->>DB: Query user
    DB-->>API: User data
    API-->>App: JWT Token
    App-->>User: Redirect to Dashboard
```

### 조건분기

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Client->>Server: Request
    alt Success
        Server-->>Client: 200 OK
    else Error
        Server-->>Client: 500 Error
    end
```

## Class Diagram

```mermaid
classDiagram
    class User {
        +String id
        +String name
        +String email
        +login()
        +logout()
    }

    class Post {
        +String id
        +String title
        +String content
        +publish()
    }

    User "1" --> "*" Post : writes
```

## ER Diagram

```mermaid
erDiagram
    USER ||--o{ POST : writes
    USER ||--o{ COMMENT : creates
    POST ||--o{ COMMENT : has

    USER {
        uuid id PK
        string name
        string email UK
        timestamp created_at
    }

    POST {
        uuid id PK
        uuid author_id FK
        string title
        text content
    }

    COMMENT {
        uuid id PK
        uuid user_id FK
        uuid post_id FK
        text content
    }
```

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review : Submit
    Review --> Published : Approve
    Review --> Draft : Reject
    Published --> Archived : Archive
    Archived --> [*]
```

## C4 Architecture

```mermaid
C4Context
    title System Context Diagram

    Person(user, "User", "Application user")

    System(webapp, "Web Application", "Next.js frontend")
    System(api, "API Server", "Backend service")

    System_Ext(stripe, "Stripe", "Payment processing")
    System_Ext(sendgrid, "SendGrid", "Email service")

    Rel(user, webapp, "Uses")
    Rel(webapp, api, "API calls")
    Rel(api, stripe, "Payments")
    Rel(api, sendgrid, "Emails")
```

## Gantt Chart

```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD

    section Planning
    Requirements    :a1, 2024-01-01, 7d
    Design          :a2, after a1, 5d

    section Development
    Backend         :b1, after a2, 14d
    Frontend        :b2, after a2, 14d

    section Testing
    QA              :c1, after b1, 7d
```

## Pie Chart

```mermaid
pie showData
    title Technology Stack
    "TypeScript" : 45
    "Python" : 30
    "Go" : 15
    "Other" : 10
```

## Git Graph

```mermaid
gitGraph
    commit
    branch feature
    checkout feature
    commit
    commit
    checkout main
    merge feature
    commit
```

## Best Practices

- **단순하게**: 노드 20-30개 이하로 유지
- **방향성**: TD(위→아래) 또는 LR(왼→오) 일관성
- **레이블**: 모든 연결에 명확한 레이블
- **색상**: 필요시만 스타일 적용
- **서브그래프**: 관련 노드 그룹화

## 문서 내 사용

````markdown
```mermaid
flowchart LR
    A --> B --> C
```
````

---

Last Updated: 2026-01-21
Version: 2.0.0
