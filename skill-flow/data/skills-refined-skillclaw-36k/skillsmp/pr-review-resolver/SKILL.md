---
name: pr-review-resolver
description: PR 코드 리뷰 코멘트를 체계적으로 해결하는 skill. 사용자가 (1) PR 리뷰 코멘트 해결을 요청하거나, (2) 코드 리뷰 피드백을 반영하려고 하거나, (3) "리뷰 코멘트", "PR 코멘트", "코드 리뷰" 관련 수정을 언급할 때 사용. 1 코멘트 → 1 작업 → 1 테스트 → 1 커밋의 원칙으로 진행하며 진행 상황을 YAML로 추적.
---

# PR Review Resolver

PR에 달린 코드 리뷰 코멘트를 체계적으로 해결한다.

## Workflow

### 0. GitHub 상태 조회

GraphQL API로 review thread 상태 조회 (쿼리는 `references/graphql-queries.md` 참조)

### 1. Progress 파일 재사용 판단

`.pr-review-progress.yaml` 파일이 존재하면:
1. GraphQL로 미해결 코멘트 ID 목록 조회 (`isResolved: false` AND `isOutdated: false`)
2. progress 파일의 pending 코멘트 ID 목록과 비교
3. **일치**: 기존 progress 파일 재사용
4. **불일치**: progress 파일 재작성

### 2. 코멘트 수집 (필요시)

progress 파일이 없거나 상태 불일치 시, **미해결 코멘트만** 수집한다.

**제외 대상**:
- `isResolved: true` - GitHub에서 이미 해결됨
- `isOutdated: true` - 코드 변경으로 더 이상 유효하지 않음

### 3. 진행 상황 추적 파일 생성

`.pr-review-progress.yaml` 파일 생성 (템플릿은 `references/progress-template.md` 참조)

### 4. 반복 실행 (1 코멘트 → 1 작업 → 1 테스트 → 1 커밋)

각 코멘트에 대해:
1. **작업 시작**: status를 `in_progress`로 변경
2. **코드 수정**: 코멘트에서 제안한 수정 사항 반영
3. **테스트 실행**: 관련 테스트 실행하여 수정 검증
4. **커밋 생성**: 단일 커밋 생성 (아래 형식)
5. **상태 업데이트**: status를 `resolved`로 변경, commit_sha 기록

```text
fix: <간단한 설명>

<상세 설명 (선택)>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### 5. 스킵 기준

다음 경우 `skipped`로 표시하고 `skip_reason` 기록:
- 외부 의존성 필요 (API 키, 설정 값 등)
- "향후 구현" 또는 "추후 개선" 언급
- 현재 PR 범위를 벗어나는 대규모 리팩토링

### 6. 완료 및 GitHub 코멘트 작성

모든 코멘트가 `resolved` 또는 `skipped` 상태가 되면:

1. 전체 테스트 실행으로 최종 검증
2. **로컬 커밋을 원격에 push** (코멘트에 커밋 링크가 유효하려면 필수)
   ```bash
   git push
   ```
3. **GitHub PR에 결과 코멘트 작성**
   ```bash
   python3 .claude/skills/pr-review-resolver/scripts/post_comments.py
   ```
4. `.pr-review-progress.yaml` 파일 삭제

### 7. Merge 감지 후 처리 (사용자가 merge 완료 시)

PR이 merged 상태로 감지되면:

1. **PR 상태 및 관련 문서 확인**
   ```bash
   python3 .claude/skills/doc-sync/scripts/check_pr_status.py
   ```

2. **미반영 도메인 문서 확인 및 업데이트**
   - `related_docs`가 있으면 Master Agent가 문서와 코드 변경 비교
   - 필요시 Sub-agent로 문서 업데이트 위임
   - 변경된 문서가 있으면 커밋 및 push

3. **Git 정리 작업 실행**
   ```bash
   bash .claude/skills/doc-sync/scripts/cleanup_after_merge.sh {branch_name}
   ```

   수행 내용:
   - `git fetch origin -p` - 원격 브랜치 삭제 상태 반영
   - `git checkout main` - main 브랜치로 이동
   - `git pull origin main` - main 최신화
   - `git branch -d {branch}` - 작업 완료된 로컬 브랜치 삭제

## 주의사항

- 각 커밋은 단일 코멘트에 대한 수정만 포함
- 테스트 실패 시 커밋하지 않고 문제 먼저 해결
- `github_comment_id`는 GitHub API에서 가져온 실제 ID 사용
- 진행 상황 파일은 작업 완료 후 삭제
