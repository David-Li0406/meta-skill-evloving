---
name: bmad-autopilot-skill
description: Autonomous BMAD development orchestration
allowed-tools: Bash,Read
version: "1.2.1"
---

# BMAD Autopilot Skill

This skill provides autonomous development capabilities following the BMAD (Breakthrough Method for Agile Development) methodology.

## When to Use

Activate this skill when the user wants to:
- Automatically process BMAD epics end-to-end
- Develop stories following TDD principles
- Create and manage pull requests automatically
- Handle CI feedback and code reviews
- Run the full BMAD development pipeline

## BMAD Workflow Phases

```
CHECK_PENDING_PR → FIND_EPIC → CREATE_BRANCH → DEVELOP_STORIES
       ↓                                              ↓
   (resume)                                    CODE_REVIEW
                                                     ↓
DONE ← MERGE_PR ← WAIT_COPILOT ← CREATE_PR ← (approved)
       ↓              ↓
    BLOCKED      FIX_ISSUES
```

## Essential Commands

### Start BMAD Autopilot

```bash
# Initialize claude-threads
ct init

# Create BMAD workflow thread
ct thread create bmad-main \
  --mode automatic \
  --template bmad-autopilot.yaml \
  --context '{"epic_pattern": "", "base_branch": "main"}'

# Start the thread
ct thread start bmad-main
```

### Process Specific Epics

```bash
# Single epic with isolated worktree
ct thread create bmad-7a \
  --template bmad-developer.md \
  --worktree \
  --context '{"epic_id": "7A"}'

# Multiple epics in parallel (each gets own worktree)
ct thread create bmad-7a --template bmad-developer.md --worktree --context '{"epic_id": "7A"}'
ct thread create bmad-8a --template bmad-developer.md --worktree --context '{"epic_id": "8A"}'
ct thread create bmad-10b --template bmad-developer.md --worktree --context '{"epic_id": "10B"}'

# Pattern matching
ct thread create bmad-all-10 \
  --template bmad-autopilot.yaml \
  --context '{"epic_pattern": "10.*"}'
```

### Monitor Progress

```bash
# Check thread status
ct thread status bmad-main

# View logs
ct thread logs bmad-main -f

# List all BMAD events
ct event list --type "EPIC_*,STORY_*,PR_*"

# List active worktrees
ct worktree list
```

## Agent Threads

The BMAD workflow spawns specialized agent threads:

| Agent | Template | Purpose |
|-------|----------|---------|
| Coordinator | `planner.md` | Find epics, manage workflow |
| Developer | `bmad-developer.md` | Implement stories with TDD |
| Reviewer | `bmad-reviewer.md` | Code review before PR |
| PR Manager | `bmad-pr-manager.md` | Create/manage pull requests |
| Fixer | `bmad-fixer.md` | Fix CI/review issues |
| Monitor | `pr-monitor.md` | Watch for PR status changes |

## Review Process

The BMAD workflow includes two review stages:

### Internal Code Review (CODE_REVIEW Phase)

After all stories in an epic are implemented, the Reviewer agent performs an internal code review before creating a PR.

**Review Checklist:**

#### Code Quality
- Code follows project style guide
- No unused imports or variables
- Functions are small and focused
- Error handling is appropriate
- No hardcoded values that should be config

#### Testing
- Tests cover the main functionality
- Edge cases are tested
- Tests are readable and maintainable
- No flaky tests introduced

#### BMAD Compliance
- Story requirements are fully implemented
- Acceptance criteria are met
- Documentation is updated if needed
- Breaking changes are documented

#### Security
- No sensitive data exposed
- Input validation present
- No SQL injection vulnerabilities
- Authentication/authorization correct

#### Performance
- No obvious performance issues
- Database queries are optimized
- No N+1 query patterns
- Caching used appropriately

**Review Outcomes:**

- **Approved**: Code meets all criteria → proceeds to CREATE_PR
- **Changes Requested**: Issues found → transitions to FIX_ISSUES phase

The reviewer publishes a `REVIEW_COMPLETED` event with status and any issues found.

### External Review (WAIT_COPILOT Phase)

After PR creation, the workflow waits for:
- GitHub Copilot review
- CI checks to pass
- All review threads resolved

**Auto-Approval Conditions:**

PRs are auto-approved when:
1. 10+ minutes since last push
2. Copilot review exists
3. All review threads resolved
4. All CI checks passed

**Review Commands:**

```bash
# View all changes
gh pr diff <pr_number>

# View specific file
gh pr diff <pr_number> -- path/to/file

# Check CI status
gh pr checks <pr_number>

# View PR details
gh pr view <pr_number>
```

## Event Types

Events published during BMAD execution:

| Event | Description |
|-------|-------------|
| `NEXT_EPIC_READY` | Coordinator found next epic |
| `BRANCH_CREATED` | Feature branch created |
| `WORKTREE_CREATED` | Isolated worktree created |
| `STORY_STARTED` | Developer starting story |
| `STORY_COMPLETED` | Story implementation done |
| `DEVELOPMENT_COMPLETED` | All stories finished |
| `REVIEW_COMPLETED` | Code review done |
| `WORKTREE_PUSHED` | Changes pushed from worktree |
| `PR_CREATED` | Pull request opened |
| `CI_PASSED` / `CI_FAILED` | CI status update |
| `COPILOT_REVIEW` | Copilot review received |
| `FIXES_NEEDED` | Issues require fixing |
| `PR_APPROVED` | PR approved |
| `PR_MERGED` | PR merged successfully |
| `WORKTREE_DELETED` | Worktree cleaned up |
| `EPIC_COMPLETED` | Epic fully processed |

## Configuration

In `.claude-threads/config.yaml`:

```yaml
bmad:
  epic_pattern: ""          # Process all, or specify "7A 8A"
  base_branch: main
  auto_merge: true          # Merge when approved
  max_concurrent_prs: 2     # Limit parallel PRs
  check_interval: 300       # PR check interval (seconds)

worktrees:
  enabled: true             # Enable worktree isolation
  max_age_days: 7           # Auto-cleanup after N days
  auto_cleanup: true        # Cleanup when thread completes
  default_base_branch: main # Default base for new worktrees
  auto_push: true           # Push changes on completion

pr_shepherd:
  max_fix_attempts: 5       # Max fix attempts per PR
  ci_poll_interval: 30      # CI check interval
  auto_merge: false         # Auto-merge when approved
```

## Story File Locations

BMAD stories are typically in:
- `_bmad-output/stories/epic-{id}/`
- `docs/stories/{id}/`

## Commit Message Format

```
feat(epic-{id}): implement story X.Y

Story {id}.{story}:
- Change description
- Another change
```

## Handling Blocked State

If autopilot becomes blocked:

```bash
# Check why
ct thread status bmad-main --verbose

# View recent events
ct event list --source bmad-main --limit 20

# Check logs
ct thread logs bmad-main

# Resume manually
ct thread resume bmad-main
```

## GitHub Integration

For automatic PR status updates:

```bash
# Start webhook server
ct webhook start --port 31338

# GitHub webhook settings:
# URL: http://your-server:31338/webhook
# Events: Pull requests, Check runs, Reviews
```

## Auto-Approval Workflow

The project has an `auto-approve.yml` workflow that handles PR approval automatically.

### Triggering Auto-Approval

```bash
# Trigger auto-approve for a specific PR
gh workflow run auto-approve.yml -f pr_number=<PR_NUMBER>

# Or use the manual approve-pr workflow with options
gh workflow run approve-pr.yml -f pr_number=<PR_NUMBER> [-f skip_ci_check=false] [-f comment="Optional message"]
```

### Auto-Approval Conditions

PRs are auto-approved when:
1. 2+ minutes since last push
2. Copilot review exists (at least 1 review from copilot-pull-request-reviewer)
3. All review threads resolved (0 unresolved)
4. All CI checks passed (both check runs and commit statuses)

### Proactive Review State Detection

**IMPORTANT**: Do NOT wait passively for review comments. Proactively check:

```bash
# Check for unresolved review threads IMMEDIATELY after Copilot review
gh api graphql -f query='query {
  repository(owner: "hanibalsk", name: "property-management") {
    pullRequest(number: <PR_NUMBER>) {
      reviewThreads(first: 100) {
        nodes { isResolved path comments(first: 1) { nodes { body } } }
      }
    }
  }
}' | jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)]'

# If unresolved > 0, spawn review-comment-handler agent immediately
# DO NOT wait for the auto-approve workflow to fail
```

### Quick PR Status Check

```bash
# Combined status check for a PR
gh pr view <PR_NUMBER> --json mergeable,mergeStateStatus,reviewDecision,statusCheckRollup | jq '{
  mergeable,
  mergeStateStatus,
  reviewDecision,
  ci_in_progress: [.statusCheckRollup[] | select(.status == "IN_PROGRESS")] | length,
  ci_failures: [.statusCheckRollup[] | select(.conclusion == "FAILURE")] | length
}'
```

## Parallel vs Sequential Mode

**Sequential** (default):
- One epic at a time
- Simpler state management
- Good for small teams

**Parallel** (with worktrees):
- Multiple epics concurrently
- Each thread gets isolated git worktree
- No conflicts between parallel development
- Higher throughput
- Configure with `max_concurrent_prs`

```bash
# Parallel development with worktrees
ct thread create epic-7a --mode automatic --template bmad-developer.md --worktree --context '{"epic_id": "7A"}'
ct thread create epic-8a --mode automatic --template bmad-developer.md --worktree --context '{"epic_id": "8A"}'
ct orchestrator start

# Each thread works in isolation
ct worktree list
```

## PR Shepherd Integration

The PR Shepherd automatically handles CI failures and review comments with worktree isolation:

```bash
# Watch a PR - creates isolated worktree for fixes
ct pr watch 123

# Shepherd automatically:
# - Creates worktree for PR branch
# - Spawns fix threads when CI fails
# - Fix threads work in isolated worktree
# - Pushes fixes from worktree
# - Cleans up worktree when PR merges

ct pr status 123
ct pr daemon  # Run as background service
```
