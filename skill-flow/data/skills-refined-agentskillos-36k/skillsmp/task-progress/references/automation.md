# Automation Actions

## Draft PR 자동 생성

Feature 브랜치 존재 but Draft PR 없을 때:

```bash
# 빈 커밋 생성
git commit --allow-empty -m ":tada: #32 Draft PR생성을 위한 빈 커밋"

# 푸시
git push -u origin feature/32-add-comments

# Draft PR 생성
gh pr create --draft --title "[Draft] #32 댓글 기능 추가" --body "작업 진행 중..."
```

## GitHub Project 상태 자동 변경

```bash
# 작업 시작 시 (검수완료 → 작업중)
gh project item-edit --id {item_id} --field-id {status_field_id} --project-id {project_id} --text "작업중"

# dev 머지 후 (작업중 → 리뷰요청)
gh project item-edit --id {item_id} --field-id {status_field_id} --project-id {project_id} --text "리뷰요청"
```

## 날짜 속성 자동 설정

| 상태 변경 | 설정 속성 | 설명 |
|----------|----------|------|
| → **작업중** | `시작일` | 실제 작업 시작 시점 기록 |
| → **리뷰요청** | `종료일` | dev 소스 머지 및 리뷰 요청 시점 기록 |

```bash
# 시작일 설정 (작업중 상태 변경 시)
gh api graphql -f query='
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $date: Date!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId, itemId: $itemId, fieldId: $fieldId,
    value: { date: $date }
  }) { projectV2Item { id } }
}' -f projectId="{project_id}" -f itemId="{item_id}" -f fieldId="{시작일_field_id}" -f date="$(date +%Y-%m-%d)"

# 종료일 설정 (리뷰요청 상태 변경 시)
gh api graphql -f query='
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $date: Date!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId, itemId: $itemId, fieldId: $fieldId,
    value: { date: $date }
  }) { projectV2Item { id } }
}' -f projectId="{project_id}" -f itemId="{item_id}" -f fieldId="{종료일_field_id}" -f date="$(date +%Y-%m-%d)"
```

> **📖 상세 API**: [project-board/references/api-commands.md](../../project-board/references/api-commands.md)

## SEMO 메타데이터 업데이트

작업 시작 시 `~/.claude.json` 업데이트:

```json
{
  "SEMO": {
    "role": "parttimer",
    "position": "developer",
    "boarded": true,
    "participantProjects": ["cm-office"],
    "currentTask": {
      "issueNumber": 32,
      "repo": "cm-office",
      "title": "댓글 기능 추가",
      "startedAt": "2025-11-25T10:30:00Z",
      "branch": "feature/32-add-comments",
      "prNumber": 145
    }
  }
}
```

## 출력 형식

```markdown
=== 작업 진행도 (cm-office#32: 댓글 기능 추가) ===

- [x] 업무할당 (cm-office#32)
- [x] GitHub Project 상태: 작업중
- [x] Feature 브랜치 (feature/32-add-comments)
- [x] Draft PR 생성 (#145)
- [x] Spec 작성 (specs/comments/spec.md)
- [x] Plan 작성 (specs/comments/plan.md)
- [ ] Tasks 작성 (specs/comments/tasks.md)
- [ ] Tasks GitHub Issue 연동
- [ ] 테스트코드 작성
- [ ] 린트 및 빌드 통과
- [ ] 푸시 및 리뷰 진행
- [ ] dev 머지
- [ ] GitHub Project 상태: 리뷰요청

=== 다음 단계 ===
📝 Tasks 작성을 진행하시겠습니까? (/speckit.tasks)

=== 자동화 가능 작업 ===
💡 다음 작업을 자동으로 수행할 수 있습니다:
- Tasks 작성 후 GitHub Issues 연동 (sync-tasks)
- 린트 에러 자동 수정 (npm run lint -- --fix)
- Draft PR → Ready for review 전환 (gh pr ready)
```
