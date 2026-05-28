---
name: postgres-schema
description: PostgreSQL 스키마 설계 가이드. DDL 작성, 테이블 설계, 인덱스 전략, 마이그레이션 시 참조. "schema", "ddl", "table", "migration", "index", "constraint" 키워드로 트리거.
---

# PostgreSQL Schema Design Guide

## Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                     Schema Design Principles                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. TEXT 기본 → VARCHAR 예외 (RFC 표준만)                         │
│  2. TIMESTAMPTZ 필수 (타임존 보존)                                │
│  3. ENUM 선택적 (고정 값 집합만)                                   │
│  4. Partial Index 활용 (NULL 제외)                                │
│  5. CASCADE 명시적 설정                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| **Schema** | 도메인 소문자 | `chat`, `users`, `auth` |
| **Table** | snake_case 복수형 | `sessions`, `social_accounts` |
| **Column** | snake_case | `user_id`, `created_at` |
| **PK** | `id` | `id UUID PRIMARY KEY` |
| **FK Column** | `{entity}_id` | `session_id`, `user_id` |
| **Index** | `idx_{table}_{columns}` | `idx_sessions_user_updated` |
| **Constraint** | `{type}_{table}_{column}` | `fk_user`, `chk_role` |

## Column Type Strategy

### 1. TEXT 기본 원칙

```sql
-- 좋은 예: 길이 불확실한 컬럼은 TEXT
content TEXT NOT NULL,
title TEXT NOT NULL,
description TEXT,

-- 나쁜 예: 임의 길이 제한
title VARCHAR(255) NOT NULL,  -- 왜 255인가?
```

### 2. VARCHAR 예외 (RFC/표준 기반만)

```sql
-- 이메일: RFC 5321 (64 + 1 + 255 = 320)
email VARCHAR(320) NOT NULL,

-- 전화번호: E.164 표준 (최대 15자리 + 국가코드)
phone_number VARCHAR(20) UNIQUE,

-- ISO 코드류
country_code CHAR(2),        -- ISO 3166-1 alpha-2
currency_code CHAR(3),       -- ISO 4217
language_code VARCHAR(5),    -- BCP 47 (ko-KR)
```

### 3. ENUM 사용 기준

```sql
-- 좋은 예: 값 집합이 고정되고 변경이 드문 경우
role VARCHAR(10) NOT NULL CHECK (role IN ('user', 'assistant')),
type VARCHAR(20) NOT NULL CHECK (type IN ('text', 'image', 'generated_image')),

-- 대안: PostgreSQL ENUM 타입 (마이그레이션 주의)
CREATE TYPE message_role AS ENUM ('user', 'assistant');
```

**ENUM vs CHECK 비교:**

| 방식 | 장점 | 단점 |
|------|------|------|
| CHECK | 마이그레이션 쉬움, 값 추가 간단 | 오타 가능성 |
| ENUM TYPE | 타입 안전성, 저장 공간 효율 | 값 추가 시 ALTER TYPE 필요 |

## Timestamp Rules

```sql
-- 필수: TIMESTAMPTZ 사용 (타임존 보존)
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

-- 금지: TIMESTAMP WITHOUT TIME ZONE
created_at TIMESTAMP NOT NULL,  -- 타임존 정보 손실
```

**SQLAlchemy에서 자동 갱신:**

```python
updated_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=True),
    server_default=func.now(),
    onupdate=func.now(),
)
```

## Constraint Patterns

### Foreign Key

```sql
-- CASCADE: 부모 삭제 시 자식도 삭제 (1:N 종속 관계)
CONSTRAINT fk_session FOREIGN KEY (session_id)
    REFERENCES chat.sessions(id) ON DELETE CASCADE,

-- SET NULL: 부모 삭제 시 NULL로 설정 (선택적 참조)
CONSTRAINT fk_assignee FOREIGN KEY (assignee_id)
    REFERENCES users.accounts(id) ON DELETE SET NULL,

-- RESTRICT: 자식 있으면 부모 삭제 방지 (보호)
CONSTRAINT fk_owner FOREIGN KEY (owner_id)
    REFERENCES users.accounts(id) ON DELETE RESTRICT,
```

### Check Constraints

```sql
-- 값 검증
CONSTRAINT chk_role CHECK (role IN ('user', 'assistant')),
CONSTRAINT chk_type CHECK (type IN ('text', 'image', 'generated_image')),

-- 범위 검증
CONSTRAINT chk_message_count CHECK (message_count >= 0),
```

### Unique Constraints

```sql
-- 단일 유니크
email VARCHAR(320) UNIQUE NOT NULL,

-- 복합 유니크 (명명된 제약조건)
CONSTRAINT uq_social_provider UNIQUE (provider, provider_user_id),
```

## Index Strategy

### 기본 인덱스

```sql
-- 조회 패턴 기반 인덱스
CREATE INDEX idx_sessions_user_updated
    ON chat.sessions(user_id, updated_at DESC);

-- 히스토리 조회용
CREATE INDEX idx_messages_session_ts
    ON chat.messages(session_id, timestamp DESC);
```

### Partial Index (조건부 인덱스)

```sql
-- NULL 제외로 인덱스 크기 최적화
CREATE INDEX idx_accounts_nickname
    ON users.accounts(nickname)
    WHERE nickname IS NOT NULL;

-- Soft delete 지원
CREATE INDEX idx_sessions_active
    ON chat.sessions(user_id, updated_at DESC)
    WHERE is_deleted = FALSE;
```

## Soft Delete Pattern

```sql
-- 권장: Boolean 플래그
is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

-- 대안: 삭제 시간 기록
deleted_at TIMESTAMPTZ,

-- 인덱스에서 삭제된 행 제외
CREATE INDEX idx_sessions_user_updated
    ON chat.sessions(user_id, updated_at DESC)
    WHERE is_deleted = FALSE;
```

## Standard DDL Template

```sql
-- 1. Schema 생성
CREATE SCHEMA IF NOT EXISTS {schema_name};

-- 2. Table 생성
CREATE TABLE {schema_name}.{table_name} (
    -- PK
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- FK
    {parent}_id UUID NOT NULL,

    -- Data columns
    {column} {TYPE} [NOT NULL] [DEFAULT value],

    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Soft delete (선택)
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

    -- Constraints
    CONSTRAINT fk_{parent} FOREIGN KEY ({parent}_id)
        REFERENCES {parent_schema}.{parent_table}(id) ON DELETE CASCADE,
    CONSTRAINT chk_{column} CHECK ({column} IN ('val1', 'val2'))
);

-- 3. Index 생성
CREATE INDEX idx_{table}_{columns}
    ON {schema_name}.{table_name}({columns})
    [WHERE condition];

-- 4. Comment (선택)
COMMENT ON TABLE {schema_name}.{table_name} IS '테이블 설명';
COMMENT ON COLUMN {schema_name}.{table_name}.{column} IS '컬럼 설명';
```

## Migration Structure

```
migrations/schemas/
├── 001_users_schema.sql      # users 스키마
├── 002_auth_schema.sql       # auth 스키마
├── 003_chat_schema.sql       # chat 스키마 (신규)
└── README.md                 # 마이그레이션 가이드
```

## Review Checklist

DDL 리뷰 시 확인할 항목:

- [ ] **TEXT vs VARCHAR**: VARCHAR는 RFC 표준 기반인가?
- [ ] **TIMESTAMPTZ**: 모든 시간 컬럼이 타임존 포함인가?
- [ ] **FK CASCADE**: 삭제 동작이 명시적으로 설정되었는가?
- [ ] **Index**: 주요 조회 패턴에 인덱스가 있는가?
- [ ] **Partial Index**: Soft delete나 NULL 컬럼에 조건부 인덱스 적용?
- [ ] **Naming**: 컨벤션을 따르는가?
- [ ] **NOT NULL**: 필수 컬럼에 NOT NULL 제약이 있는가?
- [ ] **DEFAULT**: 적절한 기본값이 설정되었는가?

## Reference Files

- **DDL conventions**: See [ddl-conventions.md](./references/ddl-conventions.md)
- **Index strategy**: See [index-strategy.md](./references/index-strategy.md)

## Eco² Project Notes

- 블로그 참조: https://rooftopsnow.tistory.com/132
- 기존 스키마: `migrations/schemas/users_schema.sql`
- ORM: SQLAlchemy 2.0 with asyncpg
