---
name: create-pull-request
description: Use this skill to create concise and useful pull requests with clear descriptions.
---

# Create Pull Request Skill

Create pull requests (PRs) with concise, useful descriptions.

## Philosophy

- **Be brief**: No walls of text. Reviewers skim.
- **Be specific**: Focus on what changed and why, not how (the code shows how).
- **No fluff**: Skip test plans, checklists, and boilerplate sections.

## PR Title

Use the format: `<type>: <short description>`

Types: `fix`, `feat`, `refactor`, `docs`, `chore`, `test`

**Examples:**
- `fix: handle null user in session lookup`
- `feat: add workspace pause/resume`
- `refactor: extract terminal manager from agent`

## PR Description

Keep it short. Aim for 2-5 bullet points max.

```markdown
## Summary

- <what changed>
- <why it changed>
- <any notable decisions or tradeoffs>
```

Avoid sections like "Test Plan" or "Screenshots" unless truly necessary.

## Steps to Create a PR

1. **Check changed files**:
   ```bash
   git diff --name-only main...HEAD
   ```

2. **Run validation and reviews in parallel**:
   - Run `bun run validate` (background).
   - Spawn review agents based on changed files:
     | Changed files | Agent to spawn |
     |---------------|----------------|
     | `src/agent/`, auth, user input, data handling | `security-review` |
     | Loops, data fetching, DB queries, heavy computation | `perf-review` |
     | `web/` or `mobile/` (.tsx/.jsx files) | `react-review` |

3. **Fix any issues** found by validation or review agents before proceeding.

4. **Create PR** (only after validation passes and reviews are addressed):
   ```bash
   gh pr create --title "<type>: <description>" --body "$(cat <<'EOF'
   ## Summary

   - <what>
   - <why>
   EOF
   )"
   ```

## When to Add More

Only add extra sections if genuinely useful:
- **Breaking changes**: If API/behavior changes affect users.
- **Migration**: If users need to do something.
- **Screenshots**: Only for UI changes, and only if they help.

## Anti-patterns

- Long descriptions nobody reads.
- Copy-pasting commit messages as bullets.
- "This PR does X" (we know, it's a PR).
- Test plan sections (CI runs tests).
- Checklists (use CI for enforcement).