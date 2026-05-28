---
name: feedback-management
description: Use this skill when collecting user feedback and managing issues related to the SEMO package in a Supabase database.
---

# Body of the merged SKILL.md

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: feedback-management 호출` 시스템 메시지를 첫 줄에 출력하세요.

## Purpose

This skill is designed for collecting user feedback and managing issues related to the SEMO package, utilizing the Supabase database.

---

## 🔴 데이터 소스 변경 (v2.0.0)

| 버전 | 데이터 소스 | 방식 |
|------|------------|------|
| v1.x | GitHub Issues | `gh api` CLI |
| **v2.0** | **Supabase** | `issues` 테이블 조회 및 INSERT |

---

## Feedback Types

| 유형 | 설명 | issues.type |
|------|------|-------------|
| **bug** | 의도한 대로 동작하지 않음 | `bug` |
| **feature** | 개선 아이디어, 새 기능 요청 | `feature` |

> **Note**: labels 컬럼에 `feedback` 값이 필수로 포함됩니다.

---

## Workflow for Collecting Feedback

1. 피드백 유형 확인 (버그 or 제안)
2. 정보 수집 (질문/결과/기대사항)
3. Supabase issues 테이블에 INSERT
4. 완료 메시지 (이슈 번호 안내)

---

## Phase 1: 피드백 수집 및 이슈 생성

### 1.1 피드백 정보 수집

사용자에게 다음 정보를 수집:
- 피드백 유형 (bug / feature)
- 제목
- 상세 내용 (재현 단계, 기대 결과 등)

### 1.2 Supabase로 이슈 생성

```typescript
// Supabase 클라이언트를 사용한 이슈 생성
const { data, error } = await supabase
  .from('issues')
  .insert({
    office_id: officeId,  // 현재 Office ID
    title: `[Feedback] ${title}`,
    body: body,
    type: feedbackType,  // 'bug' or 'feature'
    state: 'open',
    status: 'backlog',
    labels: ['feedback', packageName]
  })
  .select('number')
  .single();
```

### 1.3 SQL 직접 사용 (MCP Server)

```sql
-- 피드백 이슈 생성
INSERT INTO issues (office_id, title, body, type, state, status, labels)
VALUES (
  '{office_uuid}',
  '[Feedback] {제목}',
  '{본문}',
  '{피드백 유형}',
  'open',
  'backlog',
  ARRAY['feedback', 'semo-skills']
)
RETURNING number;
```

---

## Phase 2: 피드백 분석 및 우선순위 추천

### 2.1 Supabase로 피드백 이슈 조회

```typescript
// Supabase 클라이언트를 사용한 피드백 조회
const { data: feedbacks, error } = await supabase
  .from('issues')
  .select(`
    number,
    title,
    body,
    type,
    status,
    labels,
    created_at,
    assignee:agent_personas(name)
  `)
  .eq('state', 'open')
  .contains('labels', ['feedback'])
  .order('created_at', { ascending: false });
```

### 2.2 분석 기준

| 항목 | 확인 내용 |
|------|----------|
| **유효성** | 요청이 명확하고 실현 가능한가? |
| **중복 여부** | 기존 이슈와 중복되는가? 이미 반영된 기능인가? |
| **반영 위치** | 어떤 패키지/스킬을 수정해야 하는가? |
| **난이도** | 수정 범위와 복잡도는 어느 정도인가? |
| **영향도** | 다른 기능에 미치는 영향은? |

### 2.3 우선순위 추천

| 우선순위 | 기준 | 예시 |
|----------|------|------|
| 🔴 **높음** | 버그, 사용자 경험 저하, 빠른 수정 가능 | 오류 수정, 중요 기능 누락 |
| 🟡 **중간** | 기능 개선, 적절한 난이도 | 워크플로우 개선, 새 옵션 추가 |
| 🟢 **낮음** | 선택적 개선, 높은 난이도 | 대규모 리팩토링, 선택적 기능 |
| ⚪ **보류** | 추가 논의 필요, 불명확한 요구사항 | 요구사항 불명확, 기술적 제약 |

---

## Phase 3: 처리 권유

> **분석 완료 후 사용자에게 처리 여부를 확인합니다.**

### 3.1 권유 메시지

```markdown
---

## 💡 다음 단계

위 분석 결과를 바탕으로 피드백을 처리할 수 있습니다.

**처리 옵션**:
1. `"전체 처리해줘"` - 우선순위 순서대로 전체 처리
2. `"#104 처리해줘"` - 특정 이슈만 처리
3. `"#101, #103 처리해줘"` - 여러 이슈 선택 처리
```

### 3.2 체이닝: process-feedback 호출

```text
[feedback-management] 분석 및 우선순위 추천
    ↓
사용자: "처리해줘" / "#104 반영해줘"
    ↓
[자동] skill:process-feedback 호출
    ↓
피드백 처리 완료
```

---

## Output Format

### 전체 출력 예시

```markdown
[SEMO] Skill: feedback-management 호출

## 📋 SEMO 피드백 현황

| # | 제목 | 유형 | 상태 | 생성일 |
|---|------|------|------|--------|
| #104 | [Feature] 기능 요청 | feature | backlog | 2024-12-29 |

---

### 📊 피드백 분석

#### #104 [Feature] 기능 요청
- **유효성**: ✅ | **중복**: ❌ | **난이도**: 🟡 중간

---

## 💡 다음 단계

피드백을 처리하시겠습니까?

- `"전체 처리해줘"` - 우선순위대로 전체 처리
- `"#101 처리해줘"` - 특정 이슈만 처리
```

---

## GitHub CLI Fallback

Supabase 연결이 불가능한 경우 GitHub CLI로 폴백:

```bash
# Fallback: GitHub API로 이슈 조회
gh api repos/semicolon-devteam/semo/issues \
  --jq '.[] | select(.state == "open") | select(.labels | any(.name == "feedback"))'
```

---

## 🔴 피드백 수정 완료 후 슬랙 알림 (NON-NEGOTIABLE)

> **피드백 이슈 수정 완료 후, 문의자에게 반드시 슬랙 알림을 전송합니다.**
>
> 상세 프로세스는 [process-feedback Skill](../process-feedback/SKILL.md#phase-6-이슈-종료-및-알림) 참조

---

## References

- [issues 테이블 마이그레이션](../../../semo-repository/supabase/migrations/20260113003_issues_discussions.sql)
- [process-feedback Skill](../process-feedback/SKILL.md) - 피드백 처리 (체이닝 대상)
- [Slack 설정](../../semo-core/_shared/slack-config.md)