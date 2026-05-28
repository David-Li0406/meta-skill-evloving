# GitHub Templates Reference

Quick copy-paste templates for common GitHub operations.

## Commit Message Templates

### Feature
```
feat(<scope>): <description>

<Why this feature is needed>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Bug Fix
```
fix(<scope>): <description>

<What was broken and how this fixes it>

Fixes #<issue-number>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Refactor
```
refactor(<scope>): <description>

<Why this refactoring improves the code>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Documentation
```
docs(<scope>): <description>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Pull Request Template

```markdown
## Summary
<!-- 1-3 sentence description of what this PR does -->

## Changes
<!-- Bullet list of specific changes -->
-

## Testing
- [ ] Builds for ESP32-S3 (`idf.py build`)
- [ ] Unit tests pass (if applicable)
- [ ] Tested on hardware (if applicable)
- [ ] No new compiler warnings

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated (if needed)
- [ ] No heap allocation after init
- [ ] Thread-safe (if shared state)

## Notes
<!-- Any additional context, trade-offs, or follow-up work -->

---
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Issue Templates

### Bug Report
```markdown
## Bug Description
<!-- Clear description of the bug -->

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
<!-- What should happen -->

## Actual Behavior
<!-- What actually happens -->

## Environment
- ESP-IDF version:
- Chip: ESP32-S3
- Hardware revision:

## Additional Context
<!-- Logs, screenshots, etc. -->
```

### Feature Request
```markdown
## Feature Description
<!-- Clear description of the feature -->

## Use Case
<!-- Why is this feature needed? -->

## Proposed Solution
<!-- How might this be implemented? -->

## Alternatives Considered
<!-- Other approaches you've thought about -->

## Additional Context
<!-- Mockups, examples, references -->
```

## Review Comment Templates

### Suggestion
```
**Suggestion:** Consider using `X` here instead of `Y` because <reason>.

Example:
\`\`\`cpp
// suggested code
\`\`\`
```

### Question
```
**Question:** I'm not sure I understand the intent here. Could you explain why <specific thing>?
```

### Blocking Issue
```
**Blocking:** This will cause <problem> because <reason>.

Suggested fix:
\`\`\`cpp
// fix
\`\`\`
```

### Praise
```
Nice! This is a clean solution for <problem>.
```

## gh CLI Command Templates

### Create Feature PR
```bash
gh pr create \
  --title "feat(<scope>): <description>" \
  --body "## Summary
<description>

## Changes
- <change 1>
- <change 2>

## Testing
- [ ] Builds for ESP32-S3
- [ ] Tested on hardware

---
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### Create Bug Fix PR
```bash
gh pr create \
  --title "fix(<scope>): <description>" \
  --body "## Summary
Fixes #<issue>

## Changes
- <what was fixed>

## Testing
- [ ] Bug no longer reproduces
- [ ] Builds for ESP32-S3

---
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### Create Issue
```bash
gh issue create \
  --title "Bug: <description>" \
  --body "## Description
<description>

## Steps to Reproduce
1.
2.

## Expected vs Actual
Expected:
Actual: "
```
