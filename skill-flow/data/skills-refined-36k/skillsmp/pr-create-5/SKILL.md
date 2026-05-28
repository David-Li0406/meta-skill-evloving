---
name: pr-create
description: Create pull request with proper format. PR 생성, 변경사항 분석, PR 메시지 작성.
allowed-tools: Read, Bash, Grep, Glob
---

# Create Pull Request

**IMPORTANT: 모든 설명과 요약은 한국어로 작성하세요. 단, 코드 예시와 명령어는 원문 그대로 유지합니다.**

## Workflow

### 1. Analyze Changes
```bash
# Check current branch status
git status

# View commits since branching from main
git log origin/main..HEAD --oneline

# View full diff for PR description
git diff origin/main...HEAD --stat
git diff origin/main...HEAD
```

### 2. Sync with Main (if needed)
```bash
git fetch origin
git rebase origin/main
# Resolve conflicts if any, then:
git push --force-with-lease
```

### 3. Create PR
```bash
gh pr create --title "<type>(<scope>): <subject>" --body "$(cat <<'EOF'
## Summary
- Brief description of changes

## Changes
- List of specific changes made

## Test Plan
- [ ] How to verify changes work

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

## PR Title Format
```
<type>(<scope>): <subject>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
feat(auth): add OAuth2 login support
fix(api): handle null response from server
refactor(utils): simplify date formatting logic
```

## PR Message Template

```markdown
## Summary
<1-3 sentences explaining what and why>

## Changes
- Change 1
- Change 2
- Change 3

## Test Plan
- [ ] Unit tests pass
- [ ] Manual testing done
- [ ] Edge cases covered
```

## Tips

- Keep PRs small (< 400 lines)
- One feature per PR
- Write clear, descriptive titles
- Include test plan for reviewers
