---
name: task-planner
version: "1.0.0"
description: "Use when: multi-step tasks, 'plan this', 'orchestrate', 'break down', complex features needing wave-based execution. Decomposes tasks, assigns agents, creates GitHub Issue for tracking, manages wave-based execution with hooks."
tools: [Read, Glob, Grep, Bash, Write, AskUserQuestion, TodoWrite, Skill, Task]
---

# Task Planner - Orchestration Skill

Orchestrates multi-step implementations: decomposition, agent assignment, wave scheduling, GitHub Issue tracking, hook-based execution management.

**This is an ORCHESTRATION skill** - delegates design to `/architecture-tech-lead`, implementation to appropriate agents. Never implement code directly.

---

## Arguments

- `/task-planner "description"` - Start new plan
- `/task-planner --status` - Show current task graph status
- `/task-planner --complete` - Finalize, clean up state
- `/task-planner --abort` - Cancel mid-execution, clean state

---

## Workflow

### 1. Parse Intent

Understand what user wants to achieve:
- What is the goal?
- What are success criteria?
- What codebase areas involved?

### 2. Analyze Complexity

**Simple** (decompose directly):
- Clear scope, <3 tasks
- No architecture decisions needed
- Single feature addition

**Complex** (delegate to arch-lead):
- Multiple components affected
- Architecture decisions required
- Design patterns to choose
- >3 implementation tasks

For complex tasks:
```
Invoke: /architecture-tech-lead
Result: Detailed plan with architecture, code examples, phases
Output: .claude/plans/{YYYY-MM-DD}-{slug}.md
```

### 3. Extract Implementation Tasks

Parse plan into tasks. **Design = the plan itself, NOT a tracked task**. Tasks start at implementation:

```
T1: Create User domain model
T2: Implement JWT service
T3: Add login endpoint
T4: Write tests
```

### 4. Assign Agents

Match task keywords to wrapper agents (these preload the corresponding skills):

| Agent (subagent_type) | Triggers |
|-------|----------|
| code-implementer-agent | implement, create, build, add, write code, model |
| architecture-agent | design, architecture, pattern, refactor |
| java-test-agent | test, junit, jqwik, property-based (Java) |
| ts-test-agent | vitest, playwright, react test (TypeScript) |
| security-agent | security, auth, jwt, oauth, vulnerability |
| code-reviewer | review, quality check |
| dotfiles-agent | nix, nixos, home-manager, sops |
| k8s-agent | kubernetes, k8s, kubectl, helm, argocd, deploy, pod, ingress, service, external-secrets, cert-manager, metallb, cloudflared |
| keycloak-agent | keycloak, realm, oidc, abac, authorization services |
| frontend-agent | frontend, ui, react, next.js, component, styling |

Fallback: `general-purpose` if no match.

### 5. Schedule Waves

Dependency-based wave scheduling:

```
Wave 1: Tasks with no dependencies (run parallel)
Wave 2: Tasks depending on Wave 1
Wave N: Tasks depending on Wave N-1
```

Example:
```
Wave 1: [T1: model, T2: service]     (parallel)
Wave 2: [T3: endpoint]               (depends on T1, T2)
Wave 3: [T4: tests]                  (depends on T3)
```

### 6. User Approval

Present plan summary:
- Task breakdown with agents
- Wave schedule
- GitHub Issue will be created

Ask: "Proceed with this plan?"

### 7. Create Artifacts

On approval, create three artifacts:

**A. Local Plan** (already exists from arch-lead or step 2):
```
.claude/plans/{YYYY-MM-DD}-{slug}.md
```

**B. GitHub Issue**:
```bash
gh issue create \
  --title "Plan: {title}" \
  --body "$(cat .claude/plans/{slug}.md)"
```

Store returned issue number.

**C. State File**: `.claude/state/active_task_graph.json`

See `templates.md` for full schema. Key fields:
- `current_wave`, `executing_tasks`, `tasks[]` (id, status, wave, review_status)
- `wave_gates[N]` (impl_complete, tests_passed, reviews_complete, blocked)

### 8. Orchestrate Execution

For each wave:

1. Get pending tasks in current wave
2. Spawn ALL wave tasks in parallel (single message, multiple Task calls):
   - Update state: add to `executing_tasks`, `status = "in_progress"`
   - Build agent prompt with context (see Agent Context Template)
   - SubagentStop hook: status → "implemented", removes from executing_tasks
3. Wait for all wave tasks to reach "implemented"
4. Run **Wave Gate Sequence** (see 8a) before advancing

### 8a. Wave Gate Sequence

After all wave tasks reach "implemented", the SubagentStop hook outputs:

```
=========================================
  Wave N implementation complete
=========================================

Run: /wave-gate

(Tests + parallel code review + advance)
```

**Invoke `/wave-gate`** - it handles everything:
1. Run integration tests
2. Spawn task-reviewer per task (parallel, uses /review-pr)
3. Aggregate findings (critical blocks, advisory logged)
4. Post GH comment with review summary
5. Advance to next wave (or block if critical findings)

If blocked, fix issues and run `/wave-gate` again - it re-reviews only blocked tasks.

### Helper Scripts (used by /wave-gate)

Located in `~/.claude/hooks/helpers/`:

| Script | Purpose |
|--------|---------|
| `mark-tests-passed.sh` | Mark wave tests passed/failed |
| `store-review-findings.sh` | Store critical/advisory per task |
| `complete-wave-gate.sh` | Mark complete, update GH, advance |

---

## Agent Context Template

See `templates.md` for full template. Key elements:
- `**Task ID:** TX` (required for hooks to track)
- Task description + relevant plan context
- Constraints: follow plan, write tests, tests must pass

---

## State Management

### On `/task-planner "description"`:
1. Create `.claude/state/active_task_graph.json`
2. Hooks become active (they check for this file)

### On `/task-planner --status`:
```bash
cat .claude/state/active_task_graph.json | jq
```
Show: current wave, completed tasks, pending tasks.

### On `/task-planner --complete`:
1. Verify all tasks completed
2. Optionally close GitHub Issue
3. Remove `.claude/state/active_task_graph.json`
4. Hooks deactivate

### On `/task-planner --abort`:
1. Ask: close issue or leave open?
2. Remove `.claude/state/active_task_graph.json`
3. Hooks deactivate

---

## GitHub Issue Format

See `templates.md` for full format. Key requirements:
- Checkbox tasks: `- [ ] T1: description` (hooks update these)
- Wave groupings with dependencies noted
- Execution order table

---

## Hook Integration

Hooks auto-activate when `active_task_graph.json` exists:

| Hook | Purpose |
|------|---------|
| `block-direct-edits.sh` | BLOCKS Edit/Write - forces Task tool |
| `validate-task-execution.sh` | Validates wave order + review gate |
| `update-task-status.sh` | Marks "implemented", prompts /wave-gate |

---

## Constraints

- **NEVER use Edit/Write directly** - blocked by `block-direct-edits.sh` hook
- **MUST use Task tool** to spawn agents for ALL implementation work
- Delegate design to /architecture-tech-lead for complex tasks
- Must get user approval before creating issue
- Must populate TodoWrite with task breakdown
- Task IDs must match `- [ ] T1:` format in issue for checkbox updates

---

## CRITICAL: Parallel Execution

**Multiple Task calls in ONE message** = parallel execution within wave.

Each Task call needs: subagent_type, description, prompt with `**Task ID:** TX`
