# Supabase Migration Guide

> Semicolon 팀 마이그레이션 가이드

## 마이그레이션 기본

### 파일 생성

```bash
# Supabase CLI로 마이그레이션 파일 생성
supabase migration new create_purchases_table

# 생성되는 파일: supabase/migrations/20251215143052_create_purchases_table.sql
```

### 파일 네이밍 컨벤션

```
YYYYMMDD_description.sql
```

| 작업 | 접두사 | 예시 |
|------|--------|------|
| 테이블 생성 | `create_` | `20251215_create_purchases_table.sql` |
| 컬럼 추가 | `add_` | `20251215_add_purchases_status.sql` |
| 컬럼 수정 | `alter_` | `20251215_alter_purchases_amount_type.sql` |
| 인덱스 생성 | `create_idx_` | `20251215_create_idx_purchases_user_id.sql` |
| 함수 생성 | `add_fn_` | `20251215_add_fn_purchase_item.sql` |
| RLS 정책 | `add_rls_` | `20251215_add_rls_purchases.sql` |
| 트리거 | `add_trigger_` | `20251215_add_trigger_purchases_updated.sql` |
| 삭제 | `drop_` | `20251215_drop_legacy_table.sql` |

---

## 테이블 생성 템플릿

### 기본 테이블

```sql
-- 20251215_create_purchases_table.sql

-- 테이블 생성
CREATE TABLE purchases (
    -- Primary Key
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Foreign Keys
    user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,

    -- Data Columns
    item_name text NOT NULL,
    amount integer NOT NULL CHECK (amount > 0),
    status text DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'cancelled')),

    -- Timestamps
    created_at timestamptz DEFAULT now() NOT NULL,
    updated_at timestamptz DEFAULT now() NOT NULL
);

-- 인덱스
CREATE INDEX idx_purchases_user_id ON purchases(user_id);
CREATE INDEX idx_purchases_status ON purchases(status);
CREATE INDEX idx_purchases_created_at ON purchases(created_at DESC);

-- RLS 활성화
ALTER TABLE purchases ENABLE ROW LEVEL SECURITY;

-- RLS 정책
CREATE POLICY "Users can view own purchases" ON purchases
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own purchases" ON purchases
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- updated_at 자동 갱신 트리거
CREATE TRIGGER update_purchases_updated_at
    BEFORE UPDATE ON purchases
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 코멘트
COMMENT ON TABLE purchases IS '사용자 구매 내역';
COMMENT ON COLUMN purchases.status IS '구매 상태: pending, completed, cancelled';
```

### updated_at 트리거 함수 (공통)

```sql
-- 20251201_create_common_functions.sql

-- updated_at 자동 갱신 함수
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## 컬럼 수정

### 컬럼 추가

```sql
-- 20251216_add_purchases_notes.sql

ALTER TABLE purchases
ADD COLUMN notes text;

COMMENT ON COLUMN purchases.notes IS '구매 메모';
```

### 컬럼 타입 변경

```sql
-- 20251216_alter_purchases_amount_type.sql

-- integer → numeric 변경 (소수점 지원)
ALTER TABLE purchases
ALTER COLUMN amount TYPE numeric(10, 2);
```

### 컬럼 제약조건 추가

```sql
-- 20251216_add_purchases_constraints.sql

-- NOT NULL 제약조건 추가
ALTER TABLE purchases
ALTER COLUMN notes SET NOT NULL;

-- CHECK 제약조건 추가
ALTER TABLE purchases
ADD CONSTRAINT purchases_amount_positive CHECK (amount > 0);
```

### 컬럼 삭제

```sql
-- 20251216_drop_purchases_legacy_column.sql

ALTER TABLE purchases
DROP COLUMN IF EXISTS legacy_field;
```

---

## 인덱스 관리

### 인덱스 생성

```sql
-- 20251216_create_idx_purchases_compound.sql

-- 복합 인덱스
CREATE INDEX idx_purchases_user_status
ON purchases(user_id, status);

-- 부분 인덱스 (조건부)
CREATE INDEX idx_purchases_pending
ON purchases(created_at)
WHERE status = 'pending';

-- 유니크 인덱스
CREATE UNIQUE INDEX idx_purchases_external_id
ON purchases(external_id)
WHERE external_id IS NOT NULL;
```

### 인덱스 삭제

```sql
-- 20251216_drop_unused_indexes.sql

DROP INDEX IF EXISTS idx_purchases_legacy;
```

---

## 함수 및 트리거

### 비즈니스 로직 함수

```sql
-- 20251216_add_fn_purchase_item.sql

CREATE OR REPLACE FUNCTION purchase_item(
    p_user_id uuid,
    p_item_id uuid,
    p_quantity integer DEFAULT 1
)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_item record;
    v_purchase_id uuid;
    v_total_amount numeric;
BEGIN
    -- 아이템 조회
    SELECT * INTO v_item
    FROM items
    WHERE id = p_item_id;

    IF NOT FOUND THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Item not found'
        );
    END IF;

    -- 총 금액 계산
    v_total_amount := v_item.price * p_quantity;

    -- 구매 기록 생성
    INSERT INTO purchases (user_id, item_name, amount)
    VALUES (p_user_id, v_item.name, v_total_amount)
    RETURNING id INTO v_purchase_id;

    RETURN jsonb_build_object(
        'success', true,
        'purchase_id', v_purchase_id,
        'amount', v_total_amount
    );
END;
$$;
```

### 트리거 함수

```sql
-- 20251216_add_trigger_purchases_log.sql

-- 로그 테이블
CREATE TABLE purchase_logs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    purchase_id uuid REFERENCES purchases(id),
    action text NOT NULL,
    old_data jsonb,
    new_data jsonb,
    created_at timestamptz DEFAULT now()
);

-- 트리거 함수
CREATE OR REPLACE FUNCTION log_purchase_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO purchase_logs (purchase_id, action, new_data)
        VALUES (NEW.id, 'INSERT', to_jsonb(NEW));
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO purchase_logs (purchase_id, action, old_data, new_data)
        VALUES (NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW));
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO purchase_logs (purchase_id, action, old_data)
        VALUES (OLD.id, 'DELETE', to_jsonb(OLD));
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- 트리거 연결
CREATE TRIGGER purchases_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON purchases
    FOR EACH ROW
    EXECUTE FUNCTION log_purchase_changes();
```

---

## 롤백 전략

### 롤백 스크립트 작성

각 마이그레이션에 대응하는 롤백 스크립트 준비:

```sql
-- rollback/20251215_create_purchases_table.sql

-- 역순으로 삭제
DROP TRIGGER IF EXISTS update_purchases_updated_at ON purchases;
DROP TRIGGER IF EXISTS purchases_audit_trigger ON purchases;
DROP TABLE IF EXISTS purchase_logs;
DROP TABLE IF EXISTS purchases;
```

### 안전한 롤백 패턴

```sql
-- 테이블 삭제 전 백업
CREATE TABLE purchases_backup AS SELECT * FROM purchases;

-- 삭제
DROP TABLE purchases;

-- 롤백 필요 시 복구
CREATE TABLE purchases AS SELECT * FROM purchases_backup;
DROP TABLE purchases_backup;
```

---

## 마이그레이션 실행

### 로컬 개발

```bash
# 마이그레이션 상태 확인
supabase migration list

# 마이그레이션 실행
supabase db push

# 로컬 DB 리셋 (주의: 데이터 삭제됨)
supabase db reset
```

### 프로덕션

```bash
# Linked 프로젝트에 마이그레이션 적용
supabase db push --linked

# 또는 SQL Editor에서 직접 실행
```

---

## 주의사항

1. **순서 보장**: 마이그레이션 파일은 타임스탬프 순으로 실행됨
2. **멱등성**: 가능한 `IF NOT EXISTS`, `IF EXISTS` 사용
3. **트랜잭션**: 복잡한 마이그레이션은 트랜잭션으로 감싸기
4. **테스트**: 로컬에서 먼저 테스트 후 프로덕션 적용
5. **백업**: 프로덕션 변경 전 백업 필수

---

## References

- [Supabase Migrations](https://supabase.com/docs/guides/cli/local-development#database-migrations)
- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
