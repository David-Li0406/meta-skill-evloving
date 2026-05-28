---
name: create-pr
description: Create a pull request from the current branch with an auto-generated summary. Use when user asks to create a PR, make a pull request, or submit changes.
allowed-tools: Bash(git:*), Bash(gh:*), Read, Grep
---

# Create Pull Request

## Instructions

1. **Verify current branch state**
   ```bash
   git status
   git log origin/main..HEAD --oneline
   git diff origin/main...HEAD
   ```

2. **Analyze all commits since divergence from main**
   - Review ALL commits that will be included (not just the latest)
   - Check file changes across the entire branch
   - Understand the complete scope of changes

3. **Generate PR title and body**
   - Title: Concise summary (50 chars max)
   - Body format:
     ```markdown
     ## Summary
     - Bullet points covering ALL changes in the branch

     ## Test plan
     - [ ] Checklist of verification steps
     - [ ] Manual testing performed
     - [ ] Automated tests added/updated

     🤖 Generated with [Claude Code](https://claude.com/claude-code)
     ```

4. **Push and create PR**
   ```bash
   # Push if needed
   git push -u origin HEAD

   # Create PR
   gh pr create --title "Title" --body "$(cat <<'EOF'
   [PR body here]
   EOF
   )"
   ```

5. **Return PR URL** to the user

## Best Practices

- Review the FULL git history, not just the last commit
- Include testing instructions in the test plan
- Mention breaking changes prominently
- Link related issues/tickets if mentioned in commits
