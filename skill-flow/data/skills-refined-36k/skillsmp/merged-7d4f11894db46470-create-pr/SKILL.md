---
name: create-pr
description: Use this skill to create GitHub pull requests with properly formatted titles that pass validation checks. Ideal for submitting changes for review or when the user requests a pull request.
---

# Create Pull Request

Creates GitHub PRs with titles that adhere to specified formatting rules.

## PR Title Format

```
<type>(<scope>): <summary>
```

### Types (required)

| Type       | Description                                      | Changelog |
|------------|--------------------------------------------------|-----------|
| `feat`     | New feature                                      | Yes       |
| `fix`      | Bug fix                                          | Yes       |
| `perf`     | Performance improvement                          | Yes       |
| `test`     | Adding/correcting tests                          | No        |
| `docs`     | Documentation only                               | No        |
| `refactor` | Code change (no bug fix or feature)              | No        |
| `build`    | Build system or dependencies                     | No        |
| `ci`       | CI configuration                                 | No        |
| `chore`    | Routine tasks, maintenance                       | No        |

### Scopes (optional but recommended)

- `API` - Public API changes
- `benchmark` - Benchmark CLI changes
- `core` - Core/backend/private API
- `editor` - Editor UI changes
- `* Node` - Specific node (e.g., `Slack Node`, `GitHub Node`)

### Summary Rules

- Use imperative present tense: "Add" not "Added"
- Capitalize first letter
- No period at the end
- Be concise but descriptive
- No ticket IDs (e.g., N8N-1234)
- Add `(no-changelog)` suffix to exclude from changelog

## Steps

1. **Check current state**:
   ```bash
   git status
   git diff --stat
   git log origin/master..HEAD --oneline
   ```

2. **Analyze changes** to determine:
   - Type: What kind of change is this?
   - Scope: Which package/area is affected?
   - Summary: What does the change do?

3. **Determine ID**:
   - Attempt to extract an ID from the current branch name or use the branch type (feature, fix) if no ID is present.

4. **Validate Plan Completion**:
   - Locate the relevant `plan.md` (usually in `specs/<ID>-<name>/plan.md`).
   - Ensure all checkboxes in the plan are marked as completed (`[x]`).

5. **Push branch if needed**:
   ```bash
   git push -u origin HEAD
   ```

6. **Create PR** using gh CLI with the template:
   ```bash
   gh pr create --draft --title "<type>(<scope>): <summary>" --body "$(cat <<'EOF'
   ## Description

   <Describe what the PR does and how to test. Photos and videos are recommended.>

   ## Type of change

   - [ ] Bug fix
   - [ ] New feature
   - [ ] Improvement
   - [ ] Breaking change

   ## How Has This Been Tested?

   - [ ] Unit tests
   - [ ] Integration tests
   - [ ] Manual testing

   ## Checklist:

   - [ ] My code follows the style guidelines of this project
   - [ ] I have performed a self-review of my own code
   - [ ] I have commented my code, particularly in hard-to-understand areas
   - [ ] I have made corresponding changes to the documentation
   - [ ] I have updated the implementation plan (plan.md)
   - [ ] New and existing unit tests pass locally with my changes
   - [ ] I have checked my code and corrected any misspellings
   EOF
   )"
   ```

## Validation

The PR title must match this pattern:
```
^(feat|fix|perf|test|docs|refactor|build|ci|chore|revert)(\([a-zA-Z0-9 ]+( Node)?\))?!?: [A-Z].+[^.]$
```

Key validation rules:
- Type must be one of the allowed types
- Scope is optional but must be in parentheses if present
- Exclamation mark for breaking changes goes before the colon
- Summary must start with a capital letter
- Summary must not end with a period