# GitHub Discussions API Reference

> command-center 레포에 Discussion 생성을 위한 API 가이드

## Repository ID

```text
semicolon-devteam/command-center
Repository ID: R_kgDOOdzh9A
```

## Category IDs

| 카테고리 | ID | Slug |
|----------|-----|------|
| Meeting-Minutes | `DIC_kwDOOdzh984Cw9Lp` | meeting-minutes |
| Decision-Log | `DIC_kwDOOdzh984Cw9Lq` | decision-log |

## Discussion 생성

### GraphQL Mutation

```graphql
mutation CreateDiscussion($repoId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
  createDiscussion(input: {
    repositoryId: $repoId
    categoryId: $categoryId
    title: $title
    body: $body
  }) {
    discussion {
      number
      url
      id
    }
  }
}
```

### gh CLI 사용

```bash
# 회의록 생성
gh api graphql -f query='
mutation($repoId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
  createDiscussion(input: {
    repositoryId: $repoId
    categoryId: $categoryId
    title: $title
    body: $body
  }) {
    discussion {
      number
      url
    }
  }
}' \
  -f repoId="R_kgDOOdzh9A" \
  -f categoryId="DIC_kwDOOdzh984Cw9Lp" \
  -f title="[회의록] 2026-01-02 - 주간 회의" \
  -f body="$(cat meeting-body.md)"
```

## Discussion 조회

```bash
# 최근 Discussion 목록
gh api graphql -f query='
query {
  repository(owner: "semicolon-devteam", name: "command-center") {
    discussions(first: 10, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        number
        title
        category {
          name
        }
        url
      }
    }
  }
}' --jq '.data.repository.discussions.nodes[]'
```

## 카테고리 조회

```bash
gh api graphql -f query='
query {
  repository(owner: "semicolon-devteam", name: "command-center") {
    discussionCategories(first: 10) {
      nodes {
        id
        name
        slug
      }
    }
  }
}' --jq '.data.repository.discussionCategories.nodes[]'
```

## 에러 처리

| 에러 | 원인 | 해결 |
|------|------|------|
| `NOT_FOUND` | Repository/Category ID 오류 | ID 재확인 |
| `FORBIDDEN` | 권한 없음 | `gh auth refresh -s discussion:write` |
| `UNPROCESSABLE` | 잘못된 입력 | title/body 확인 |
