---
name: manage-sprint
description: Use this skill when you need to create, close, or manage a Sprint (Iteration) in GitHub Projects.
---

# manage-sprint Skill

> Sprint(Iteration) 목표 설정, 종료 및 회고 정리

## Purpose

이 Skill은 GitHub Projects에서 Sprint를 생성하고 종료하며, 회고를 정리하는 데 사용됩니다. Sprint 목표를 설정하고, 완료된 Task를 집계하며, 미완료 Task를 다음 Iteration으로 이관합니다.

## Workflow

### Sprint 시작

```
Sprint 시작 요청
    ↓
1. 현재/다음 Iteration 조회
2. Sprint Issue 생성 (docs 레포)
3. Sprint 목표 설정
4. 알림 전송 (선택)
    ↓
완료
```

### Sprint 종료

```
Sprint 종료 요청
    ↓
1. Iteration의 완료/미완료 Task 집계
2. Velocity 계산
3. 회고 요약 생성
4. Sprint Issue에 회고 추가
5. 미완료 Task → 다음 Iteration 이관
6. sprint-current 라벨 제거
```

## Input

### Sprint 시작

```yaml
iteration_title: "12월 1/4"           # 필수 (GitHub Projects Iteration 이름)
goals:                                # 선택
  - "댓글 기능 완성"
  - "알림 연동 시작"
notify_slack: true                    # 선택
```

### Sprint 종료

```yaml
iteration_title: "11월 4/4"            # 필수 (종료할 Iteration 이름)
next_iteration: "12월 1/4"            # 필수 (다음 Iteration 이름)
retrospective:
  good: ["API 개발 순조로움"]         # 선택 (회고에서 긍정적인 점)
  improve: ["테스트 커버리지 부족"]   # 선택 (회고에서 개선할 점)
```

## Output

### Sprint 시작

```markdown
[SEMO] Skill: manage-sprint 완료

✅ Sprint "{iteration_title}" 시작

**기간**: 2025-12-01 ~ 2025-12-07 (1주)
**Sprint Issue**: [#123](issue_url)
```

### Sprint 종료

```markdown
✅ Sprint "{iteration_title}" 종료 완료

**완료**: 8/10 Task (80%)
**Velocity**: 24pt
**미완료 이관**: 2 Task → {next_iteration}
```

## API 호출

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

[📊 Projects 보기](https://github.com/orgs/semicolon-devteam/projects/1/views/1?filterQuery=iteration:"{iteration_title}")

## 📈 진행 현황
| 상태 | 개수 |
|------|------|
| 작업중 | {in_progress} |
| 완료 | {done} |
| 대기 | {todo} |
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

## 완료 메시지

```markdown
[SEMO] Skill: manage-sprint 완료

✅ **Sprint "{iteration_title}"** 시작

| 항목 | 값 |
|------|-----|
| Iteration | {iteration_title} |
| 기간 | {start_date} ~ {end_date} |
| Sprint Issue | [#{issue_number}]({issue_url}) |

다음 단계: `/SEMO:sprint add` 명령어로 Task를 Sprint에 할당하세요.
```