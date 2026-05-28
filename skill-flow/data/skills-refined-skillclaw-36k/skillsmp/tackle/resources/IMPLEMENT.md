# Implementation Phase

Covers: plan creation, branch setup, and code implementation.

## Plan Phase

Create an implementation plan based on:
- Issue requirements
- Upstream context (from cached research)
- Cached research (patterns, conventions)

### Check: Upstream Issue Required?

From cached research, check if upstream requires an issue first:
```yaml
guidelines:
  requires_issue_first:
    - "Larger changes"
    - "New features"
```

If this change qualifies as "larger" (significant new feature, architectural change, etc.):
1. Check if a related upstream issue already exists (from pre-molecule research)
2. If not, consider creating one first: `gh issue create --repo <upstream>`
3. Reference the upstream issue in the PR

For small bug fixes, docs, or focused changes - proceed without upstream issue.

### Plan Structure

```markdown
## Implementation Plan for <issue-id>

### Goal
<What we're fixing/implementing>

### Files to Modify
- `path/to/file1.go` - <what changes>
- `path/to/file2.go` - <what changes>

### Approach
<Step-by-step implementation approach>

### Upstream Alignment
- Following pattern from: <recent PR or file>
- Commit style: <per guidelines>
- Test approach: <per guidelines>

### Risks
- <Any potential issues>
- <Hot areas to be careful with>
```

### Update Molecule

```yaml
phase: "gate-plan"
plan:
  goal: "<goal>"
  files:
    - path: "path/to/file.go"
      changes: "description"
  approach: "<approach>"
```

Then **STOP** - proceed to gate-plan (see SKILL.md).

## Working Directory

**IMPORTANT**: Work in YOUR rig - the directory you were spawned in.

```bash
pwd  # Verify you're in your own rig before making changes
```

Don't edit files in other agents' directories. If unsure about the directory structure, consult https://github.com/steveyegge/gastown/blob/main/docs/design/architecture.md#directory-structure

## Branch Phase

After plan approval, create clean branch from upstream.

### Fetch Latest

```bash
git fetch $UPSTREAM_REMOTE
```

### Create Branch

Use upstream and default branch (see SKILL.md "Detect Upstream"):

```bash
git checkout -b <type>/<issue-id>-<description> $UPSTREAM_REF
```

Branch naming: `<type>/<issue-id>-<short-description>`

**Issue ID preference:** Use upstream issue number (e.g., `123`) if available, otherwise fall back to local beads ID (e.g., `hq-1234`). Upstream issue numbers are more meaningful in the PR context.

Types:
- `fix/` - Bug fixes
- `feat/` - New features
- `docs/` - Documentation
- `refactor/` - Refactoring
- `test/` - Test additions

Examples:
```bash
# With upstream issue
git checkout -b fix/123-doctor-indent upstream/main

# Without upstream issue (local beads ID)
git checkout -b fix/hq-1234-doctor-indent upstream/main
```

### Update Molecule

```yaml
phase: "implement"
branch: "fix/hq-1234-doctor-indent"
branch_base: "upstream/main"
```

## Implement Phase

Write the code following upstream conventions.

### Guidelines

1. **Follow cached research**:
   - Use detected formatter (`gofmt`, `prettier`, etc.)
   - Follow commit message format
   - Match coding style

2. **Atomic commits**:
   - Each commit should be a logical unit
   - Conventional commit messages: `type(scope): description`
   - Reference issue (prefer upstream issue number if available):
     - With upstream issue: `fix(doctor): correct indentation (#123)`
     - Without upstream issue: `fix(doctor): correct indentation (hq-1234)`

3. **Stay focused**:
   - Only change what's needed for the issue
   - Don't fix unrelated things
   - Don't refactor beyond scope
   - Don't add features not requested

4. **Test as you go**:
   - Run tests frequently
   - Add tests for new functionality
   - Don't break existing tests

### Commit Format

From cached research (stored in cache bead description, see PROJECT-RESEARCH sub-agent output):
```yaml
commits:
  tense: "present"
  subject_max_length: 72
  issue_reference_format: "(#xxx)"  # or "(hq-xxx)" if no upstream issue
```

Examples:
```bash
# With upstream issue number (preferred)
git commit -m "fix(doctor): correct indentation in database check (#123)"

# Without upstream issue (fallback to local beads ID)
git commit -m "fix(doctor): correct indentation in database check (hq-1234)"
```

### Progress Updates

During implementation, update molecule with progress:
```yaml
phase: "implement"
commits:
  - hash: "abc1234"
    message: "fix(doctor): correct indentation"
  - hash: "def5678"
    message: "test(doctor): add indentation test"
```

### Completion

When implementation is complete:
1. Ensure all changes are committed
2. Run quick local test
3. Update molecule: `phase: "validate"`
4. Proceed to validation phase

## Isolation Principle

**Critical**: Each PR should address ONE concern.

Before completing implementation, verify:
- [ ] All changes relate to the issue
- [ ] No unrelated fixes snuck in
- [ ] No drive-by refactoring
- [ ] Commit history is clean and focused

If you noticed other issues while implementing:
- Create new beads issues for them
- Do NOT fix them in this PR
- Note them for future work

```bash
# Create separate issue for discovered problems
bd create --title "Fix unrelated thing noticed during hq-1234" --type task
```
