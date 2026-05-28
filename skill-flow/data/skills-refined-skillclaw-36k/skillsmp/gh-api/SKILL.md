---
name: gh-api
description: GitHub API calls for discussions and draft PRs (non-standard gh CLI patterns)
---

## Draft Pull Requests

### Create a draft PR

```sh
gh api --method POST repos/:owner/:repo/pulls -f title="My new feature" -f body="Description of changes" -f head="feature-branch" -f base="main" -F draft=true
```

For cross-repo PRs, use `head="username:branch"`.

### Get PR details (check if draft)

```sh
gh api repos/:owner/:repo/pulls/<number>
```

Response includes `"draft": true|false` and `"state": "open|closed"`.

### Check if PR is draft (minimal output)

```sh
gh api repos/:owner/:repo/pulls/<number> --jq '{draft, state, title}'
```

### Convert draft to ready for review

```sh
gh api --method PATCH repos/:owner/:repo/pulls/<number> -F draft=false
```

Note: Cannot convert back to draft via API once marked ready.

### List open draft PRs

```sh
gh api repos/:owner/:repo/pulls --jq '.[] | select(.draft) | {number, title}'
```

### List my open PRs in a repo

```sh
gh api repos/:owner/:repo/pulls -f state=open --jq '.[] | select(.user.login=="USERNAME") | {number, title, draft}'
```

## PR Conversation Comments

Comments on the PR timeline (not on specific lines of code). For inline review comments, use the
`gh-pr-review` skill instead.

### List conversation comments

```sh
gh api repos/:owner/:repo/issues/<number>/comments
```

### Create a conversation comment

```sh
gh api --method POST repos/:owner/:repo/issues/<number>/comments -f body="Comment text"
```

## Discussions (GraphQL)

List discussions:

```sh
gh api graphql -f query='query($owner:String!,$repo:String!) { repository(owner:$owner,name:$repo) { discussions(first:10) { nodes { number title url } } } }' -F owner=OWNER -F repo=REPO
```

View discussion:

```sh
gh api graphql -f query='query($owner:String!,$repo:String!,$number:Int!) { repository(owner:$owner,name:$repo) { discussion(number:$number) { title body comments(first:10) { nodes { body author { login } } } } } }' -F owner=OWNER -F repo=REPO -F number=NUM
```

Search discussions:

```sh
gh api graphql -f query='query($q:String!) { search(query:$q,type:DISCUSSION,first:10) { nodes { ...on Discussion { number title url } } } }' -f q="repo:OWNER/REPO QUERY"
```
