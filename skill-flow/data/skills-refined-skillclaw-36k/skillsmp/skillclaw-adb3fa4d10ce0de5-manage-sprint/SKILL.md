---
name: manage-sprint
description: Use this skill when you need to start or close a Sprint, set goals, and summarize retrospectives.
---

# Skill body

## Purpose

Manage the lifecycle of a Sprint (Iteration) by starting it with defined goals and closing it with a retrospective summary.

## Workflow

```
Sprint 관리 요청
    ↓
1. Sprint 시작 또는 종료 요청 확인
    ├─ Sprint 시작:
    │   1. 현재/다음 Iteration 조회
    │   2. Sprint Issue 생성
    │   3. Sprint 목표 설정
    │   4. 알림 전송 (선택)
    └─ Sprint 종료:
        1. Iteration의 완료/미완료 Task 집계
        2. Velocity 계산
        3. 회고 요약 생성
        4. Sprint Issue에 회고 추가
        5. 미완료 Task → 다음 Iteration 이관
        6. sprint-current 라벨 제거
```

## Input for Starting a Sprint

```yaml
iteration_title: "12월 1/4"           # 필수 (GitHub Projects Iteration 이름)
goals:                                # 선택
  - "댓글 기능 완성"
  - "알림 연동 시작"
notify_slack: true                    # 선택
```

## Input for Closing a Sprint

```yaml
iteration_title: "11월 4/4"
next_iteration: "12월 1/4"
retrospective:
  good: ["API 개발 순조로움"]
  improve: ["테스트 커버리지 부족"]
```

## Output for Starting a Sprint

```markdown
[SEMO] Skill: manage-sprint 완료

✅ Sprint "12월 1/4" 시작

**기간**: 2025-12-01 ~ 2025-12-07 (1주)
**Sprint Issue**: [#123](issue_url)
```

## Output for Closing a Sprint

```markdown
✅ Sprint "11월 4/4" 종료 완료

**완료**: 8/10 Task (80%)
**Velocity**: 24pt
**미완료 이관**: 2 Task → 12월 1/4
```

## API Calls

### Iteration 조회 (GraphQL)

```bash
gh api graphql -f query='
{
  organization(login: "semicolon-devteam") {
    projectV2(number: 1) {
      field(name: "이터레이션") {
        ... on ProjectV2IterationField {
          configuration {
            iterations {
              id
              title
              startDate
              duration
            }
          }
        }
      }
    }
  }
}'
```

### Sprint Issue 생성

```bash
gh issue create \
  --repo semicolon-devteam/docs \
  --title "🏃 Sprint: {iteration_title}" \
  --label "sprint,sprint-current" \
  --body "$(cat <<'EOF'
# 🏃 Sprint: {iteration_title}

**Iteration**: {iteration_title}
**기간**: {start_date} ~ {end_date}

## 🎯 Sprint 목표
{goals_list}

## 📋 포함된 Task
> GitHub Projects "이슈관리" → 이터레이션 "{iteration_title}" 필터로 확인

[📊 Projects 보기]
EOF
)"
```

### 이전 Sprint Issue 정리

```bash
# 이전 sprint-current 라벨 제거
gh issue list \
  --repo semicolon-devteam/docs \
  --label "sprint-current" \
  --json number \
  | jq -r '.[].number' \
  | xargs -I {} gh issue edit {} --remove-label "sprint-current" --add-label "sprint-closed"
```