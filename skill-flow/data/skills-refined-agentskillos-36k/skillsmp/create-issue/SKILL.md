---
name: create-issue
description: Create GitHub issues with proper format and templates. Use when creating new issues, writing issue descriptions, or setting up issue tracking. Triggers on "create issue", "new issue", "이슈 생성", "이슈 만들기".
---

# Create Issue

This skill guides you through creating GitHub issues with proper format and templates.

## Issue Format

### Title (English)

Use Conventional Commits format:
```
<type>(<scope>): <description>
```

**Examples:**
- `feat(auth): add OAuth2 login support`
- `fix(api): resolve timeout issue in data sync`
- `chore(setup): add pre-commit configuration`

### Body (Korean)

Structure:
- **목적 (Purpose):** What problem this issue solves
- **배경 (Background):** Why this work is needed
- **상세 내용 (Details):** Specific requirements, constraints
- **완료 조건 (Acceptance Criteria):** How to verify completion

### Labels

**Priority:**
- `priority:critical`, `priority:high`, `priority:medium`, `priority:low`

**Type:**
- `type:bug`, `type:feature`, `type:refactor`, `type:docs`

### Related Issues

- `Blocks #123` - This issue blocks another
- `Blocked by #456` - This issue is blocked by another
- `Related to #789` - Related but not blocking

## Command

```bash
gh issue create \
  --title "Type(scope): Description" \
  --body "Issue body" \
  --label "enhancement" \
  --assignee "@me"
```

## Template

```markdown
## 목적
[What problem this issue solves or what goal it achieves]

## 배경
- [Why this work is needed]
- [Current situation and pain points]
- Related to #XXX (if applicable)

## 상세 내용
- [Specific requirement 1]
- [Specific requirement 2]
- [Constraints or references]

## 완료 조건
- [ ] [Acceptance criteria 1]
- [ ] [Acceptance criteria 2]
- [ ] [Acceptance criteria 3]

## 참고 자료
- [Links to documentation]
- [Architecture diagrams if needed]
```

## User Confirmation

**IMPORTANT:** Before creating an issue:
1. Propose title, body, labels, and priority to user
2. Wait for user approval
3. Create only after confirmation
