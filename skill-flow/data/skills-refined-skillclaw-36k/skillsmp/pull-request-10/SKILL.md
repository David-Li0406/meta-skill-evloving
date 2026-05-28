---
name: pull-request
description: |
  Create or update GitHub pull requests with theme-based commit grouping and Korean body.
  Use when user asks to create, update, or draft a pull request or PR (e.g., "PR 만들어줘", "풀리퀘스트 생성해줘", "create a pull request").
  Automatically handles branch push, commit analysis, and gh CLI operations.
  For bucketplace organization repos, adds PR-by-AI label.
---

# Create (or Update) Pull Request

## Process

### 1. Verify branch status

Check if the current branch has been pushed; if not, push it to origin.
- If the current branch is "main" or "master," confirm with the user whether this is intended before proceeding.

### 2. Analyze commits by logical themes

Instead of reviewing each commit chronologically, group commits by their logical themes and purposes. Think of commits as A → A' → B → A'' → B' being grouped into themes A and B rather than 5 separate items.

### 3. Understand the WHY

Focus on why these changes were needed, not just what was changed. If the business context or motivation is unclear, ask the user for clarification.

### 4. Draft the PR

Use the `gh` command with English subject line and Korean body.

```bash
gh pr create --title "<English title>" --body "$(cat <<'EOF'
## 개요
[Brief description that naturally explains why this change was needed and what problem it solves]

## 주요 변경사항
[Group changes by logical themes, not chronological commits]

## 영향 범위
[What systems/features are affected]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

## PR Body Guidelines

### Focus on Purpose, Not Implementation

- **Primary focus**: WHY this change was needed (business context, problem being solved)
- **Secondary focus**: WHAT was changed (grouped by logical themes)
- **Avoid**: Technical implementation details unless absolutely necessary for understanding

### Examples

**Bad** - Mechanical commit listing:
```
- [TICKET-123] feat: add ArgoCD status check
- [TICKET-123] feat: add event publishing
- [TICKET-123] feat: implement sync system
- [TICKET-123] refactor: remove deprecated methods
- [TICKET-123] test: add comprehensive tests
```

**Good** - Theme-based grouping with purpose:
```
- **배포 상태 실시간 추적**: ArgoCD 연동과 이벤트 기반 모니터링을 통해 Blue-Green 배포의 승인 대기 상황을 추적
- **코드 품질 개선**: 레거시 코드 제거 및 테스트 커버리지 강화
```

## Important Notes

- Do not include "Test plan" or similar technical sections
- If you don't understand the business context, ASK the user rather than guessing
- Technical details should support the "why", not dominate the explanation
- When creating or editing a Github pull request (PR), write body in Korean and omit the "Test plan" section
- Do not just list a series of commit messages in a PR body; instead, group commits by context
- When you create a PR request on `bucketplace` organization, add `PR-by-AI` label. If the label doesn't exist, create it first and retry.
- Return the PR URL when done, so the user can see it
