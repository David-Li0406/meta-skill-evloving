# RLS (Row Level Security) 정책 패턴

Supabase에서 자주 사용되는 RLS 정책 패턴 모음입니다.

## 기본 설정

```sql
-- 테이블에 RLS 활성화 (필수!)
ALTER TABLE public.{table_name} ENABLE ROW LEVEL SECURITY;

-- 기본 거부 (RLS 활성화 시 자동 적용)
-- 정책이 없으면 모든 접근 차단
```

## 패턴 1: 본인 데이터만 접근

가장 일반적인 패턴. 사용자가 자신의 데이터만 접근 가능.

```sql
-- SELECT
CREATE POLICY "Users can view own data"
  ON public.profiles FOR SELECT
  USING (auth.uid() = user_id);

-- INSERT
CREATE POLICY "Users can insert own data"
  ON public.profiles FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- UPDATE
CREATE POLICY "Users can update own data"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- DELETE
CREATE POLICY "Users can delete own data"
  ON public.profiles FOR DELETE
  USING (auth.uid() = user_id);

-- 또는 한번에 모든 작업
CREATE POLICY "Users can manage own data"
  ON public.profiles FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);
```

## 패턴 2: 공개 읽기 + 본인만 수정

블로그 포스트, 공개 프로필 등에 적합.

```sql
-- 누구나 읽기 가능
CREATE POLICY "Public read access"
  ON public.posts FOR SELECT
  USING (true);

-- 본인만 생성
CREATE POLICY "Users can create own posts"
  ON public.posts FOR INSERT
  WITH CHECK (auth.uid() = author_id);

-- 본인만 수정
CREATE POLICY "Users can update own posts"
  ON public.posts FOR UPDATE
  USING (auth.uid() = author_id);

-- 본인만 삭제
CREATE POLICY "Users can delete own posts"
  ON public.posts FOR DELETE
  USING (auth.uid() = author_id);
```

## 패턴 3: 역할 기반 접근 (RBAC)

관리자, 편집자 등 역할별 접근 제어.

```sql
-- 역할 확인 함수
CREATE OR REPLACE FUNCTION public.get_user_role()
RETURNS TEXT AS $$
  SELECT role FROM public.profiles WHERE id = auth.uid()
$$ LANGUAGE sql SECURITY DEFINER;

-- 관리자는 모든 권한
CREATE POLICY "Admins have full access"
  ON public.posts FOR ALL
  USING (public.get_user_role() = 'admin');

-- 편집자는 읽기/쓰기
CREATE POLICY "Editors can read and write"
  ON public.posts FOR SELECT
  USING (public.get_user_role() IN ('admin', 'editor'));

CREATE POLICY "Editors can insert"
  ON public.posts FOR INSERT
  WITH CHECK (public.get_user_role() IN ('admin', 'editor'));

-- 일반 사용자는 읽기만
CREATE POLICY "Users can only read"
  ON public.posts FOR SELECT
  USING (true);
```

## 패턴 4: 팀/조직 기반 접근

같은 팀/조직 멤버만 접근 가능.

```sql
-- 팀 멤버십 확인 함수
CREATE OR REPLACE FUNCTION public.is_team_member(team_id UUID)
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.team_members
    WHERE team_id = $1 AND user_id = auth.uid()
  )
$$ LANGUAGE sql SECURITY DEFINER;

-- 팀 데이터 접근
CREATE POLICY "Team members can access team data"
  ON public.team_documents FOR SELECT
  USING (public.is_team_member(team_id));

CREATE POLICY "Team members can create documents"
  ON public.team_documents FOR INSERT
  WITH CHECK (public.is_team_member(team_id));
```

## 패턴 5: 시간 기반 접근

특정 시간 동안만 접근 가능 (이벤트, 프로모션 등).

```sql
CREATE POLICY "Access during event period"
  ON public.event_data FOR SELECT
  USING (
    NOW() BETWEEN start_date AND end_date
  );
```

## 패턴 6: 상태 기반 접근

published, draft 등 상태에 따른 접근.

```sql
-- 공개된 것만 모두에게 표시
CREATE POLICY "Published posts are public"
  ON public.posts FOR SELECT
  USING (status = 'published' OR auth.uid() = author_id);

-- 작성자는 모든 상태의 자신 글 접근
CREATE POLICY "Authors can see all own posts"
  ON public.posts FOR SELECT
  USING (auth.uid() = author_id);
```

## 패턴 7: 계층적 접근 (부모-자식)

부모 데이터에 접근 권한이 있으면 자식도 접근.

```sql
-- 프로젝트에 접근 가능하면 태스크도 접근
CREATE POLICY "Project members can access tasks"
  ON public.tasks FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.project_members pm
      WHERE pm.project_id = tasks.project_id
      AND pm.user_id = auth.uid()
    )
  );
```

## 패턴 8: 조건부 필드 접근

특정 조건에서만 민감 필드 표시.

```sql
-- 뷰로 민감 필드 숨김
CREATE VIEW public.users_public AS
SELECT
  id,
  username,
  avatar_url,
  CASE
    WHEN id = auth.uid() THEN email
    ELSE NULL
  END as email,
  CASE
    WHEN id = auth.uid() THEN phone
    ELSE NULL
  END as phone
FROM public.profiles;
```

## Storage RLS

```sql
-- 버킷별 정책
-- 공개 읽기
CREATE POLICY "Public read for avatars"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'avatars');

-- 본인 폴더에만 업로드
CREATE POLICY "Users can upload to own folder"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'avatars' AND
    (storage.foldername(name))[1] = auth.uid()::text
  );

-- 본인 파일만 삭제
CREATE POLICY "Users can delete own files"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'avatars' AND
    (storage.foldername(name))[1] = auth.uid()::text
  );
```

## 디버깅

```sql
-- 현재 사용자 ID 확인
SELECT auth.uid();

-- 현재 역할 확인
SELECT auth.role();

-- 테이블의 모든 정책 확인
SELECT * FROM pg_policies WHERE tablename = 'your_table';

-- 정책 상세 확인
SELECT
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies
WHERE tablename = 'your_table';
```

## 주의사항

1. **RLS 활성화 필수**: `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`
2. **service_role 키**: RLS 우회 가능 - 서버에서만 사용
3. **SECURITY DEFINER 함수**: 생성자 권한으로 실행 - 주의 필요
4. **성능**: 복잡한 정책은 쿼리 성능에 영향
5. **테스트**: 각 역할별로 접근 테스트 필수
