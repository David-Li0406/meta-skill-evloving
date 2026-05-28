# Quick Execution Mode

Streamlined planning and execution for simple, single-session features.

## When to Use

- Single-session implementation (~1-3 hours)
- 1-3 files affected
- No cross-cutting concerns
- Clear requirements, no discovery needed

## When NOT to Use

Use `/dev:execute-phase` instead when:
- Multi-phase features (>1 day estimated work)
- Features requiring PRD/stakeholder review
- Cross-cutting concerns affecting >5 files per layer
- Features with unclear requirements needing discovery
- Database migrations requiring careful planning

## Input Resolution

Parse `$ARGUMENTS` to determine input type:

| Pattern | Type | Action |
|---------|------|--------|
| `REQ-YYYYMMDD-*-XX` | Request Log ID | Use `/mc view` or `/mc search` |
| Starts with `./`, `/`, or `~` | File path | Read file contents directly |
| Other | Direct text | Use as feature description |

### For Request Log Input

Use `/mc` command (token-efficient):

```bash
# Get full details
meatycapture log search "REQ-ID" PROJECT

# Mark as in-progress when starting
meatycapture log item update DOC ITEM --status in-progress
```

## Phase 1: Minimal Planning

### 1.1 Pattern Discovery

Delegate to **codebase-explorer** agent:

> Find existing patterns related to the feature. Look for similar implementations, relevant file locations, import conventions, and test patterns.

### 1.2 Create Quick Plan

Generate slug from feature description (lowercase, hyphens, max 30 chars).

Write plan to `.claude/progress/quick-features/{feature-slug}.md`:

```markdown
---
type: quick-feature-plan
feature_slug: {slug}
request_log_id: {id if from REQ input, else null}
status: in-progress
created: {ISO date}
estimated_scope: small|medium
---

# {Feature Title}

## Scope
{1-2 sentences describing what this implements}

## Affected Files
- {file1}: {change description}
- {file2}: {change description}

## Implementation Steps
1. {step} → @{agent-name}
2. {step} → @{agent-name}

## Testing
- {test approach}

## Completion Criteria
- [ ] Implementation complete
- [ ] Tests pass
- [ ] Build succeeds
```

## Phase 2: Execution

### 2.1 Agent Selection

| Task Type | Agent |
|-----------|-------|
| React/UI components | ui-engineer-enhanced |
| TypeScript backend/core | backend-typescript-architect |
| Pattern discovery | codebase-explorer |
| Deep analysis | explore |
| Debugging issues | ultrathink-debugger |
| Validation/review | task-completion-validator |

### 2.2 Delegate Implementation

For each step in plan:
- Provide feature context and requirements
- Include patterns discovered by codebase-explorer
- Specify files to modify/create
- Reference @CLAUDE.md architecture patterns

Execute steps that can be parallelized together (single message, multiple Task() calls).

### 2.3 Incremental Verification

After each major step:

```bash
pnpm typecheck  # No TypeScript errors
pnpm test       # Tests pass
pnpm lint       # Lint clean
```

### 2.4 Commit Progress

After logical units of work:

```bash
git add {files}
git commit -m "feat({scope}): {description}

Refs: quick-feature/{feature-slug}"
```

## Phase 3: Quality Gates

All gates must pass before completion:

| Gate | Command |
|------|---------|
| Type checking | `pnpm typecheck` |
| Tests | `pnpm test` |
| Lint | `pnpm lint` |
| Build | `pnpm build` |

If any fail, fix before proceeding.

## Phase 4: Completion

### 4.1 Update Quick Plan

Edit `.claude/progress/quick-features/{feature-slug}.md`:
- Set `status: completed` and `completed_at: {ISO date}`
- Check all completion criteria boxes

### 4.2 Update Request Log (if applicable)

If input was a REQ ID:

```bash
# Mark item as done
meatycapture log item update DOC ITEM --status done

# Add completion note
meatycapture log note add DOC ITEM -c "Completed in quick-feature/{feature-slug}"
```

### 4.3 Capture Issues (if any)

If issues arose during implementation:

```bash
/mc capture {"title": "...", "type": "bug", "domain": "...", "notes": "Context..."}
```

## Error Recovery

If blocked:

1. Document blocker in quick plan under `## Blockers`
2. Do NOT mark as completed
3. Report to user with clear next steps needed
4. Track blocker if warranted:
   ```bash
   /mc capture {"title": "...", "type": "bug", "status": "blocked"}
   ```

## Output Summary

```
Quick Feature Complete: {feature title}

Plan: .claude/progress/quick-features/{feature-slug}.md
Files Changed: {count}
Tests: {pass count}/{total count}
Commits: {commit count}

{If from REQ: "Request log item {REQ-ID} marked as done"}
```
