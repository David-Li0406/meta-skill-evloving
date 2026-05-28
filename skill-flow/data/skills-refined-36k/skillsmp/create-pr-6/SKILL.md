---
name: create-pr
description: Create pull requests with proper format, templates, and checklists. Use when creating PRs, writing PR descriptions, or preparing code for review. Triggers on "create PR", "pull request", "PR 생성", "PR 만들기".
---

# Create Pull Request

This skill guides you through creating pull requests with proper format and templates.

## PR Format

### Title (English)

Use Conventional Commits format:
```
<type>(<scope>): <description>
```

**Examples:**
- `feat(connector): add TikTok Ads API integration`
- `fix(sync): handle rate limit errors gracefully`
- `refactor(api): optimize response structure`

### Body (Korean)

Structure:
- **목적 (Purpose):** What this PR accomplishes
- **배경 (Background):** Why this change is needed, related issues
- **변경 사항 (Changes):** Summary of what was modified
- **Breaking Changes:** Note any backward-incompatible changes
- **테스트 (Testing):** How the changes were verified

### Linked Issues

- `Closes #123` - Automatically closes issue when PR is merged
- `Fixes #456` - Automatically closes bug issue when PR is merged
- `Resolves #789` - Automatically closes issue when PR is merged

### Screenshots

- Required for UI changes (Before/After comparison)
- Include relevant terminal output for CLI changes

## Command

```bash
gh pr create \
  --title "feat(scope): description" \
  --body "PR body" \
  --assignee "@me"
```

## Template

```markdown
## 목적
[Brief description of what this PR accomplishes]

## 배경
- Closes #XXX
- [Context: why this change is needed]
- [Related issues or discussions]

## 변경 사항
- `path/to/file.py` - [What was changed]
- `tests/test_file.py` - [Tests added/modified]

## Breaking Changes
- None
<!-- Or describe:
- [Breaking change description]
- Migration guide: [steps to migrate]
-->

## 스크린샷
- N/A
<!-- Or attach Before/After images -->

## Self-review Checklist
- [ ] Code follows project style guidelines
- [ ] No unnecessary commented code or debug statements
- [ ] All lint checks pass
- [ ] Documentation updated if needed
- [ ] No secrets or credentials in code

## 테스트
- [ ] 단위 테스트 통과
- [ ] 로컬 환경에서 테스트 완료
- [ ] 기존 테스트 영향 없음 확인
```

## After PR Creation

1. Wait for CI checks to complete
2. Review any automated feedback
3. Address review comments (with user approval)
4. Request merge approval from user
5. **NEVER merge without explicit user approval**
