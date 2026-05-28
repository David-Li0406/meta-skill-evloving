# DDL Conventions Reference

## Column Type Decision Tree

```
컬럼 타입 결정 흐름:

길이 제한 필요?
├─ NO → TEXT
└─ YES → 표준 기반인가?
         ├─ RFC 5321 (이메일) → VARCHAR(320)
         ├─ E.164 (전화번호) → VARCHAR(20)
         ├─ ISO 3166 (국가코드) → CHAR(2)
         ├─ ISO 4217 (통화코드) → CHAR(3)
         ├─ BCP 47 (언어코드) → VARCHAR(5)
         └─ 기타 → TEXT (임의 제한 금지)
```

## VARCHAR Length Standards

| 도메인 | 표준 | 최대 길이 | 예시 |
|--------|------|----------|------|
| Email | RFC 5321 | 320 | `user@example.com` |
| Phone | E.164 | 20 | `+82-10-1234-5678` |
| Country | ISO 3166-1 | 2 | `KR`, `US` |
| Currency | ISO 4217 | 3 | `KRW`, `USD` |
| Language | BCP 47 | 5 | `ko-KR`, `en-US` |
| UUID string | RFC 4122 | 36 | `550e8400-e29b-41d4-...` |

## CHECK vs ENUM Decision

```
값 집합 특성 분석:

값이 자주 변경/추가되는가?
├─ YES → CHECK 제약조건 사용
│        예: status IN ('pending', 'processing', 'done')
│
└─ NO → 값이 몇 개인가?
        ├─ 2~5개 (고정) → ENUM 타입 고려
        │   예: role (user, assistant)
        │
        └─ 5개 이상 → VARCHAR + CHECK
            예: intent 분류 (20개+)
```

## Index Selection Guide

```
조회 패턴 분석:

1. 단일 컬럼 조회가 주인가?
   → 단일 컬럼 인덱스
   예: CREATE INDEX idx_users_email ON users(email);

2. 복합 조건 조회가 주인가?
   → 복합 인덱스 (선택도 높은 컬럼 먼저)
   예: CREATE INDEX idx_sessions_user_updated
       ON sessions(user_id, updated_at DESC);

3. NULL 값이 많은가?
   → Partial Index로 NULL 제외
   예: CREATE INDEX idx_accounts_nickname
       ON accounts(nickname) WHERE nickname IS NOT NULL;

4. Soft delete 사용?
   → Partial Index로 삭제 행 제외
   예: WHERE is_deleted = FALSE;
```

## FK ON DELETE Strategy

| 전략 | 사용 시점 | 예시 관계 |
|------|----------|----------|
| `CASCADE` | 자식이 부모에 종속 (1:N 종속) | 세션 → 메시지 |
| `SET NULL` | 선택적 참조 | 게시글 → 작성자(탈퇴 시) |
| `RESTRICT` | 무결성 보호 필수 | 주문 → 결제내역 |
| `NO ACTION` | 기본값 (트랜잭션 끝까지 검사 지연) | 특수 케이스 |

## Timestamp Best Practices

```sql
-- 항상 TIMESTAMPTZ 사용
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

-- SQLAlchemy 매핑
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

created_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=True),
    server_default=func.now(),
    nullable=False,
)

updated_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=True),
    server_default=func.now(),
    onupdate=func.now(),
    nullable=False,
)
```

## Common Anti-Patterns

### 1. 임의 VARCHAR 길이

```sql
-- 나쁜 예
title VARCHAR(255),           -- 왜 255?
description VARCHAR(1000),    -- 왜 1000?

-- 좋은 예
title TEXT,
description TEXT,
```

### 2. TIMESTAMP without timezone

```sql
-- 나쁜 예
created_at TIMESTAMP DEFAULT NOW(),  -- 타임존 손실

-- 좋은 예
created_at TIMESTAMPTZ DEFAULT NOW(),
```

### 3. FK CASCADE 누락

```sql
-- 나쁜 예: CASCADE 미지정 (기본값 NO ACTION)
FOREIGN KEY (user_id) REFERENCES users(id),

-- 좋은 예: 명시적 삭제 동작
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
```

### 4. 인덱스 없는 FK

```sql
-- 나쁜 예: FK만 있고 인덱스 없음
session_id UUID NOT NULL REFERENCES sessions(id),

-- 좋은 예: FK 컬럼에 인덱스 추가
CREATE INDEX idx_messages_session ON messages(session_id);
```

## Normalization Guidelines

| 정규화 수준 | 사용 시점 | 예시 |
|------------|----------|------|
| **3NF** | 핵심 엔티티 | accounts, sessions |
| **2NF** | 성능/편의 비정규화 | 스냅샷 데이터 포함 |
| **1NF** | 배열/JSON 허용 | metadata JSONB |

**의도적 비정규화는 반드시 문서화:**

```sql
-- 비정규화: 조회 성능을 위해 message_count 캐싱
-- 실제 값은 messages 테이블 COUNT로 계산 가능
message_count INT NOT NULL DEFAULT 0,
```
