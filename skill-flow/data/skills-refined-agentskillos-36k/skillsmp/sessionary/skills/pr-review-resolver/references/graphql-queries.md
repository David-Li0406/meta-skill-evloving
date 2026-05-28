# GraphQL Queries for PR Review

## 상태 조회 (간략)

```bash
OWNER=$(gh repo view --json owner -q .owner.login)
REPO=$(gh repo view --json name -q .name)
PR_NUM=<PR번호>

gh api graphql -f query="query { repository(owner: \"$OWNER\", name: \"$REPO\") { pullRequest(number: $PR_NUM) { reviewThreads(first: 100) { nodes { id isResolved isOutdated comments(first: 1) { nodes { databaseId } } } } } } }"
```

## 미해결 코멘트 상세 조회

```bash
OWNER=$(gh repo view --json owner -q .owner.login)
REPO=$(gh repo view --json name -q .name)
PR_NUM=<PR번호>

gh api graphql -f query="query { repository(owner: \"$OWNER\", name: \"$REPO\") { pullRequest(number: $PR_NUM) { reviewThreads(first: 100) { nodes { id isResolved isOutdated path line comments(first: 1) { nodes { databaseId body author { login } } } } } } } }" --jq '.data.repository.pullRequest.reviewThreads.nodes | map(select(.isResolved == false and .isOutdated == false))'
```

## 참고

- gh CLI의 `:owner`, `:repo` 플레이스홀더는 REST API에서만 작동
- GraphQL 변수 문법 (`$owner`)은 쉘 변수와 충돌하므로 직접 값 삽입
- `isResolved`: GitHub UI에서 "Resolve conversation"으로 해결됨
- `isOutdated`: 해당 코드 라인이 변경되어 outdated 됨
