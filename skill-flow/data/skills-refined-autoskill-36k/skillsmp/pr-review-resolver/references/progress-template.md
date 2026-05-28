# Progress File Template

## 파일 위치

`.pr-review-progress.yaml` (저장소 루트)

## 템플릿

```yaml
pr_number: 123
total_comments: 2
resolved: 0
comments:
  - id: 1
    thread_id: "PRT_xxx"           # GraphQL thread ID (상태 조회용)
    github_comment_id: 2686928751  # REST API comment ID (답글 작성용)
    file: backend/app/lesson/view.py
    line: 47
    summary: "video_url 유효성 검사 누락"
    status: pending                # pending | in_progress | resolved | skipped
    commit_sha: null
    skip_reason: null

  - id: 2
    thread_id: "PRT_yyy"
    github_comment_id: 2686928752
    file: backend/app/ticket/repository.py
    line: 58
    summary: "timezone-aware datetime 비교 불일치"
    status: pending
    commit_sha: null
    skip_reason: null
```

## 필드 설명

| 필드 | 설명 |
|------|------|
| `thread_id` | GraphQL thread ID (상태 조회용) |
| `github_comment_id` | REST API comment ID (답글 작성용, GitHub API에서 가져온 실제 ID) |
| `status` | `pending` → `in_progress` → `resolved` 또는 `skipped` |
| `commit_sha` | resolved 시 커밋 해시 기록 |
| `skip_reason` | skipped 시 사유 기록 |
