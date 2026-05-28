---
name: assign-task
description: |
  이슈 업무 할당 및 작업량 자동 산정 (Supabase DB 기반). Use when (1) Issue assignee 지정,
  (2) 작업량(Point) 자동 계산, (3) 이슈 본문 체크리스트 추가, (4) 상태 업데이트,
  (5) Slack 담당자 알림.
tools: [Supabase, Bash, Read, Edit, mcp__semo-integrations__semo_get_slack_token]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: assign-task 호출 - #{issue_number} → @{assignee}` 시스템 메시지를 첫 줄에 출력하세요.

# assign-task Skill

> 이슈 업무 할당 + 작업량 자동 산정 + Slack 알림 (Supabase DB 기반)

## 🔴 데이터 소스 변경 (v2.0.0)

| 버전 | 데이터 소스 | 방식 |
|------|------------|------|
| v1.x | GitHub Issues + Projects | GraphQL API |
| **v2.0** | **Supabase** | `issues` 테이블 UPDATE |

---

## Purpose

이슈에 담당자를 할당하고, 작업량을 자동으로 산정하여 이슈 본문과 상태를 업데이트합니다.

### 핵심 기능

| 기능 | 설명 |
|------|------|
| **Assignee 지정** | issues.assignee_id 업데이트 |
| **작업량 산정** | Estimation Guide 기반 Point 자동 계산 |
| **이슈 본문 업데이트** | 체크리스트 형식으로 작업량 명세 추가 |
| **estimation_point 갱신** | 총점 숫자 저장 |
| **Slack 알림** | 담당자에게 업무 할당 알림 발송 |

## Input

```javascript
skill: assign-task({
  issue: 123,                    // Issue 번호 (필수)
  assignee: "username",          // 담당자 ID (필수)
  tasks: [                       // 작업 목록 (선택 - 미입력시 이슈 분석)
    { name: "API 엔드포인트 구현", point: 2 },
    { name: "DTO 클래스 작성", point: 1 }
  ],
  notify: true                   // Slack 알림 여부 (기본: true)
});
```

## Execution Flow

```text
1. Issue 정보 조회 (Supabase)
   ↓
2. 작업 목록 분석 (입력값 또는 이슈 본문 파싱)
   ↓
3. 작업량 산정 (Estimation Guide 기준)
   ↓
4. Issue 업데이트 (assignee_id + body + estimation_point)
   ↓
5. 상태 변경 (status → 'todo')
   ↓
6. Slack 알림 발송 (선택)
```

### Step 1: Issue 정보 조회

```sql
-- 이슈 정보 조회
SELECT
  i.id,
  i.number,
  i.title,
  i.body,
  i.type,
  i.status,
  i.labels,
  ap.name AS assignee_name
FROM issues i
LEFT JOIN agent_personas ap ON i.assignee_id = ap.id
WHERE i.number = 123
  AND i.office_id = '{office_uuid}';
```

### Step 2: 담당자 ID 조회

```sql
-- agent_personas에서 담당자 조회
SELECT id, name, slack_id
FROM agent_personas
WHERE name = '{assignee_name}'
  AND office_id = '{office_uuid}';
```

### Step 3: 작업량 산정

> **Reference**: [estimation-guide.md](references/estimation-guide.md)

각 작업에 Point를 부여:
- 기존 Point가 있으면 그대로 사용
- 없으면 작업 유형별 기본값 적용

### Step 4: Issue 업데이트

```sql
-- 담당자 할당 및 작업량 업데이트
UPDATE issues
SET
  assignee_id = '{assignee_uuid}',
  estimation_point = 4,
  body = body || E'\n\n---\n\n## 📊 작업량 산정\n\n- [ ] API 엔드포인트 구현: 2점\n- [ ] DTO 클래스 작성: 1점\n- [ ] 테스트 코드 작성: 1점\n\n**총점: 4점** (예상 소요: 2일)',
  status = 'todo',
  updated_at = NOW()
WHERE number = 123
  AND office_id = '{office_uuid}'
RETURNING number, title, status, estimation_point;
```

```typescript
// Supabase 클라이언트 사용
const { data, error } = await supabase
  .from('issues')
  .update({
    assignee_id: assigneeId,
    estimation_point: totalPoints,
    body: updatedBody,
    status: 'todo'
  })
  .eq('number', 123)
  .eq('office_id', officeId)
  .select()
  .single();
```

### Step 5: Slack 알림 발송

> **Reference**: [slack-template.md](references/slack-template.md)

```bash
# Token 획득
TOKEN=$(mcp__semo-integrations__semo_get_slack_token)

# 담당자 Slack ID는 agent_personas.slack_id에서 조회

# 메시지 발송
curl -s -X POST 'https://slack.com/api/chat.postMessage' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d @- << 'EOF'
{
  "channel": "{slack_id}",
  "text": "📋 새 업무가 할당되었습니다: #{issue_number}",
  "blocks": [...]
}
EOF
```

## Output Format

```markdown
[SEMO] Skill: assign-task 완료

## ✅ 업무 할당 완료

**Issue**: #123 - [Task 제목]
**담당자**: @username

### 📊 작업량 산정

| 작업 | Point |
|------|-------|
| API 엔드포인트 구현 | 2 |
| DTO 클래스 작성 | 1 |
| 테스트 코드 작성 | 1 |
| **총점** | **4** |

**예상 소요**: 2일 (1 Point = 0.5일)

### 업데이트 내역

- [x] Assignee 지정: @username
- [x] 이슈 본문 작업량 체크리스트 추가
- [x] estimation_point: 4
- [x] status: todo
- [x] Slack 알림 발송
```

## Error Handling

| 에러 | 처리 |
|------|------|
| Issue not found | 에러 메시지 출력 후 종료 |
| Invalid assignee | 유효한 담당자 ID 요청 |
| Supabase 연결 오류 | 에러 메시지, GitHub CLI 폴백 안내 |
| Slack ID 미발견 | 경고 출력, 할당은 계속 진행 |

## GitHub CLI Fallback

Supabase 연결이 불가능한 경우:

```bash
# Fallback: GitHub CLI로 담당자 할당
gh issue edit 123 --add-assignee {username} --repo {owner}/{repo}
```

## References

- [issues 테이블 마이그레이션](../../../semo-repository/supabase/migrations/20260113003_issues_discussions.sql)
- [Estimation Guide](references/estimation-guide.md) - 작업량 산정 기준
- [Slack Template](references/slack-template.md) - 알림 메시지 템플릿

## Related Skills

- [notify-slack](../notify-slack/SKILL.md) - Slack 알림 공통 스킬
- [project-status](../project-status/SKILL.md) - 상태 변경
- [start-task](../start-task/SKILL.md) - 작업 시작
