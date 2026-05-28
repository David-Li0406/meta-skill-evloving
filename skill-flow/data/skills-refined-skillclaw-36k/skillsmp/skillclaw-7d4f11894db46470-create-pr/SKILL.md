---
name: create-pr
description: Use this skill when creating GitHub pull requests with properly formatted titles that pass CI validation, ensuring clarity and completeness in your submissions.
---

# Create Pull Request

Creates GitHub PRs with titles that adhere to specified formatting rules and include necessary details.

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

3. **Push branch if needed**:
   ```bash
   git push -u origin HEAD
   ```

4. **Create PR** using gh CLI with the template from `.github/pull_request_template.md`:
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