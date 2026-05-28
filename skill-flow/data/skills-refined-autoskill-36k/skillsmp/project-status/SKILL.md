---
name: project-status
description: |
  이슈 Status 변경 (Supabase DB 기반). Use when (1) "상태 변경해줘", "Status 바꿔줘",
  (2) "작업중으로 변경", "완료 처리", (3) Epic/태스크 상태 일괄 변경.
tools: [Supabase, Bash, Read]
model: inherit
---

> **호출 시 메시지**: 이 Skill이 호출되면 반드시 `[SEMO] Skill: project-status` 시스템 메시지를 첫 줄에 출력하세요.

# project-status Skill

> 이슈 Status 필드 변경 (Supabase DB 기반)

## 🔴 데이터 소스 변경 (v2.0.0)

| 버전 | 데이터 소스 | 방식 |
|------|------------|------|
| v1.x | GitHub Projects | GraphQL mutation |
| **v2.0** | **Supabase** | `issues.status` UPDATE |

---

## Purpose

Supabase `issues` 테이블의 `status` 컬럼을 업데이트합니다.
상태 변경 이력은 `issue_status_history` 테이블에 자동 기록됩니다.

---

## Status 옵션

| Status | 설명 |
|--------|------|
| backlog | 초기 상태 |
| todo | 할 일 목록 |
| in_progress | 개발 진행 중 |
| review | 코드 리뷰 대기 |
| testing | QA 테스트 단계 |
| done | 작업 완료 |

## Workflow

### 1. Supabase로 Status 변경

```typescript
// Supabase 클라이언트를 사용한 상태 변경
const { data, error } = await supabase
  .from('issues')
  .update({ status: 'in_progress' })
  .eq('number', 123)
  .eq('office_id', officeId)
  .select('number, title, status')
  .single();
```

### 2. SQL 직접 사용 (MCP Server)

```sql
-- 단일 이슈 상태 변경
UPDATE issues
SET status = 'in_progress',
    updated_at = NOW()
WHERE number = 123
  AND office_id = '{office_uuid}'
RETURNING number, title, status;
```

### 3. update_issue_status 함수 사용 (권장)

마이그레이션에 포함된 헬퍼 함수를 사용하면 히스토리 자동 기록:

```sql
-- 상태 변경 함수 호출 (히스토리 자동 기록)
SELECT * FROM update_issue_status(
  123,                    -- issue_number
  '{office_uuid}'::uuid,  -- office_id
  'in_progress',          -- new_status
  '{actor_uuid}'::uuid    -- changed_by (optional)
);
```

### 4. 이전 상태 확인

```sql
-- 현재 상태 확인
SELECT number, title, status
FROM issues
WHERE number = 123
  AND office_id = '{office_uuid}';

-- 상태 변경 이력 확인
SELECT *
FROM issue_status_history
WHERE issue_id = (
  SELECT id FROM issues WHERE number = 123
)
ORDER BY changed_at DESC;
```

## 상태값 Alias

사용자가 한글/영문 키워드를 사용하면 실제 status 값으로 매핑:

| 입력 | status 값 |
|------|-----------|
| 백로그, backlog | backlog |
| 할일, 작업대기, todo | todo |
| 작업중, 진행중, in_progress | in_progress |
| 리뷰요청, 리뷰, review | review |
| 테스트중, 테스트, testing | testing |
| 완료, 닫기, done | done |

## 일괄 변경 지원

```sql
-- 특정 라벨의 이슈들 일괄 상태 변경
UPDATE issues
SET status = 'in_progress',
    updated_at = NOW()
WHERE 'project:차곡' = ANY(labels)
  AND state = 'open'
  AND office_id = '{office_uuid}'
RETURNING number, title, status;
```

```typescript
// Supabase로 일괄 변경
const { data, error } = await supabase
  .from('issues')
  .update({ status: 'in_progress' })
  .contains('labels', ['project:차곡'])
  .eq('state', 'open')
  .eq('office_id', officeId)
  .select('number, title, status');
```

## 출력 포맷

```markdown
[SEMO] project-status: 상태 변경 완료

✅ Status 변경 완료

**Issue**: #123
**이전 상태**: todo
**변경 상태**: in_progress
```

## 에러 처리

### 이슈 미발견

```markdown
⚠️ **이슈 미발견**

Issue #123을 찾을 수 없습니다.
- 이슈 번호를 확인해주세요.
- Office ID가 올바른지 확인해주세요.
```

### 잘못된 상태값

```markdown
⚠️ **잘못된 상태값**

'{status}'는 유효하지 않은 상태값입니다.

사용 가능한 상태:
- backlog, todo, in_progress, review, testing, done
```

### Supabase 연결 오류

```markdown
⚠️ **Supabase 연결 오류**

상태를 변경할 수 없습니다.
- MCP 서버 설정을 확인해주세요.
```

## GitHub GraphQL Fallback

Supabase 연결이 불가능한 경우 GitHub GraphQL로 폴백:

```bash
# Fallback: GitHub Projects GraphQL
gh api graphql -f query='
  mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }) {
      projectV2Item { id }
    }
  }
' -f projectId="$PROJECT_ID" \
  -f itemId="$ITEM_ID" \
  -f fieldId="$STATUS_FIELD_ID" \
  -f optionId="$STATUS_OPTION_ID"
```

## References

- [issues 테이블 마이그레이션](../../../semo-repository/supabase/migrations/20260113003_issues_discussions.sql)
- [assign-task Skill](../assign-task/SKILL.md)
- [task-progress Skill](../task-progress/SKILL.md)
