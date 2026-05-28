# RLS (Row Level Security) Patterns

> Semicolon 팀 공통 RLS 정책 패턴

## 기본 패턴

### 1. 소유자 기반 접근 (Owner-based)

가장 일반적인 패턴. 사용자가 자신의 데이터만 접근 가능.

```sql
-- 테이블 생성
CREATE TABLE purchases (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid REFERENCES auth.users(id) NOT NULL,
    item_name text NOT NULL,
    amount integer NOT NULL,
    created_at timestamptz DEFAULT now()
);

-- RLS 활성화
ALTER TABLE purchases ENABLE ROW LEVEL SECURITY;

-- 정책 생성
CREATE POLICY "Users can view own purchases" ON purchases
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own purchases" ON purchases
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own purchases" ON purchases
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own purchases" ON purchases
    FOR DELETE USING (auth.uid() = user_id);
```

### 2. 역할 기반 접근 (Role-based)

JWT의 role claim을 활용한 접근 제어.

```sql
-- admin 역할만 모든 데이터 접근
CREATE POLICY "Admins have full access" ON purchases
    FOR ALL USING (auth.jwt() ->> 'role' = 'admin');

-- moderator 역할은 읽기만 가능
CREATE POLICY "Moderators can view all" ON purchases
    FOR SELECT USING (auth.jwt() ->> 'role' = 'moderator');
```

### 3. 공개/비공개 (Visibility-based)

콘텐츠의 공개 상태에 따른 접근 제어.

```sql
CREATE TABLE posts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid REFERENCES auth.users(id) NOT NULL,
    title text NOT NULL,
    content text,
    visibility text DEFAULT 'private' CHECK (visibility IN ('public', 'private', 'followers')),
    created_at timestamptz DEFAULT now()
);

ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- 공개 포스트는 누구나 볼 수 있음
CREATE POLICY "Anyone can view public posts" ON posts
    FOR SELECT USING (visibility = 'public');

-- 본인 포스트는 항상 볼 수 있음
CREATE POLICY "Users can view own posts" ON posts
    FOR SELECT USING (auth.uid() = user_id);

-- 팔로워 전용 포스트
CREATE POLICY "Followers can view follower-only posts" ON posts
    FOR SELECT USING (
        visibility = 'followers'
        AND EXISTS (
            SELECT 1 FROM follows
            WHERE follower_id = auth.uid()
            AND following_id = posts.user_id
        )
    );
```

---

## 고급 패턴

### 4. 팀/조직 기반 접근 (Team-based)

같은 팀/조직 멤버만 접근 가능.

```sql
CREATE TABLE team_documents (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id uuid REFERENCES teams(id) NOT NULL,
    title text NOT NULL,
    content text,
    created_at timestamptz DEFAULT now()
);

ALTER TABLE team_documents ENABLE ROW LEVEL SECURITY;

-- 팀 멤버만 문서 접근 가능
CREATE POLICY "Team members can view documents" ON team_documents
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM team_members
            WHERE team_members.team_id = team_documents.team_id
            AND team_members.user_id = auth.uid()
        )
    );
```

### 5. 계층적 접근 (Hierarchical)

상위 권한이 하위 데이터에 접근 가능.

```sql
-- 권한 계층: owner > admin > member > viewer
CREATE TABLE project_items (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid REFERENCES projects(id) NOT NULL,
    title text NOT NULL,
    created_at timestamptz DEFAULT now()
);

ALTER TABLE project_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Project members can view items" ON project_items
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM project_members
            WHERE project_members.project_id = project_items.project_id
            AND project_members.user_id = auth.uid()
            AND project_members.role IN ('owner', 'admin', 'member', 'viewer')
        )
    );

CREATE POLICY "Project admins can modify items" ON project_items
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM project_members
            WHERE project_members.project_id = project_items.project_id
            AND project_members.user_id = auth.uid()
            AND project_members.role IN ('owner', 'admin')
        )
    );
```

### 6. 시간 기반 접근 (Time-based)

특정 기간 동안만 접근 가능.

```sql
CREATE TABLE promotions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title text NOT NULL,
    start_at timestamptz NOT NULL,
    end_at timestamptz NOT NULL,
    created_at timestamptz DEFAULT now()
);

ALTER TABLE promotions ENABLE ROW LEVEL SECURITY;

-- 진행 중인 프로모션만 조회 가능
CREATE POLICY "Only active promotions visible" ON promotions
    FOR SELECT USING (
        now() BETWEEN start_at AND end_at
    );

-- 관리자는 모든 프로모션 관리 가능
CREATE POLICY "Admins can manage all promotions" ON promotions
    FOR ALL USING (auth.jwt() ->> 'role' = 'admin');
```

---

## 성능 최적화

### 인덱스 추가

RLS에서 자주 사용되는 컬럼에 인덱스 추가:

```sql
-- user_id 기반 조회가 많은 경우
CREATE INDEX idx_purchases_user_id ON purchases(user_id);

-- team_id 기반 조회
CREATE INDEX idx_team_documents_team_id ON team_documents(team_id);

-- 복합 조건
CREATE INDEX idx_project_members_project_user
    ON project_members(project_id, user_id);
```

### Security Definer 함수 활용

복잡한 RLS 로직은 함수로 분리:

```sql
CREATE OR REPLACE FUNCTION can_access_project(p_project_id uuid)
RETURNS boolean
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM project_members
        WHERE project_id = p_project_id
        AND user_id = auth.uid()
    );
END;
$$;

-- RLS에서 함수 사용
CREATE POLICY "Project access check" ON project_items
    FOR SELECT USING (can_access_project(project_id));
```

---

## 주의사항

1. **RLS 활성화 필수**: 테이블 생성 후 반드시 `ENABLE ROW LEVEL SECURITY` 실행
2. **Service Role 주의**: service_role key는 RLS를 우회하므로 백엔드에서만 사용
3. **성능 테스트**: 복잡한 RLS는 쿼리 성능에 영향. EXPLAIN ANALYZE로 확인
4. **기본 거부**: 정책이 없으면 모든 접근 거부됨 (deny by default)

---

## References

- [Supabase RLS Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [PostgreSQL RLS Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
