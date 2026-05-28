---
name: project-setup
description: Use this skill when initializing or synchronizing project documentation and settings, ensuring consistency and adherence to project guidelines.
---

# Skill body

## Trigger Conditions

Use this skill in the following scenarios:
- When initializing a new project without existing CLAUDE.md or .claude/ directory.
- When updates or organization of the project documentation are requested.

## Execution Steps

### 1. Check Current State

```bash
# Check for CLAUDE.md
cat CLAUDE.md 2>/dev/null || echo "CLAUDE.md not found"
wc -l CLAUDE.md 2>/dev/null

# Check documentation structure
ls -la .claude/ 2>/dev/null
ls -la docs/ 2>/dev/null

# Check user-level settings
cat ~/.claude/CLAUDE.md
ls ~/.claude/context/
```

### 2. Analyze Differences

Confirm the following:

| Item | Check |
|------|-------|
| CLAUDE.md line count | Is it 60 lines or less? |
| Variable definitions | Are MEMORY_DIR and BASE_BRANCH present? |
| Quality checks | Are lint/format/typecheck/test commands available? |
| @references | Are details delegated to context/? |
| Separation principle | Are human-facing and agent-facing documents separated? |

### 3. Create Update Proposal (if CLAUDE.md exists)

If CLAUDE.md is present and needs updates, create a proposal:

```markdown
## Update Proposal

### CLAUDE.md
**Current:** XX lines
**Proposal:** Simplify as follows

```markdown
# <Project Name>

## Variables
MEMORY_DIR=.local/
BASE_BRANCH=develop

## Quality Checks
```bash
npm run lint
npm run format
npm run typecheck
npm test
```

## Special Notes
- [Project-specific rules]
```

### 4. Create CLAUDE.md (if not exists)

If CLAUDE.md does not exist, create it in the project root with the following content:

```markdown
# <Project Name>

## Variables
MEMORY_DIR=.local/
BASE_BRANCH=develop

## Quality Checks
```bash
npm run lint      # or appropriate command
npm run format
npm run typecheck
npm test
```

## Special Notes
- [Project-specific rules]
```

### 5. Configure gitignore

Ensure `.local/` is not tracked by git:

```bash
# Check if .local/ is in global gitignore
if git config --global core.excludesfile &>/dev/null; then
  GLOBAL_GITIGNORE=$(git config --global core.excludesfile)
  if grep -q "^\.local/$" "$GLOBAL_GITIGNORE" 2>/dev/null; then
    echo ".local/ is already excluded in global gitignore"
  else
    # Check if inside a git repository
    if git rev-parse --git-dir &>/dev/null; then
      echo ".local/" >> "$(git rev-parse --git-dir)/info/exclude"
      echo "Added .local/ to .git/info/exclude"
    else
      echo "Skipping gitignore setup as outside of git repository"
    fi
  fi
fi
```

### 6. User Confirmation

Use AskUserQuestion to confirm:
1. Approval of update proposals
2. Memory directory location (adjust for monorepos)
3. Quality check commands
4. Project-specific rules

### 7. Execute Changes

Upon approval, execute the following:
1. Update CLAUDE.md (if necessary)
2. Remove unnecessary files
3. Move/rename files as needed
4. Create .claude/context/ (if required)

### 8. Verification

```bash
# Check line count
wc -l CLAUDE.md

# Verify structure
ls -la .claude/

# Manually check @references functionality
```

## Documentation Separation Principle

### 60 Lines Rule
- Delegate details to `@.claude/context/`
- Utilize Progressive Disclosure

### Required Sections
```markdown
# <Project Name>

## Variables
MEMORY_DIR=<path>
BASE_BRANCH=<branch>

## Quality Checks
[List of commands]

## Special Notes
[Project-specific rules - concisely]
```

### Optional Sections (if necessary)
- Architecture overview (briefly)
- Naming conventions
- Prohibited items

## Criteria for Unnecessary Files

| Decision | Condition |
|----------|-----------|
| **Delete** | Old agent definitions, duplicate documents, empty files |
| **Move** | Agent-facing content in docs/ → .claude/context/ |
| **Consolidate** | Multiple files with similar content → 1 file |
| **Retain** | Human-facing documents (README, docs/), project-specific settings |

## Checklist

- [ ] CLAUDE.md is 60 lines or less
- [ ] Variables (MEMORY_DIR, BASE_BRANCH) are defined
- [ ] Quality check commands are documented
- [ ] Documentation separation principle is followed
- [ ] Unnecessary files are deleted
- [ ] @references are correctly set