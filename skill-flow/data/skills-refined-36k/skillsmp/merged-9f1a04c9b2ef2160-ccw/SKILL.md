---
name: ccw
description: Use this skill when you need a stateless workflow orchestrator that auto-selects optimal workflows based on task intent.
---

# CCW - Claude Code Workflow Orchestrator

CCW is a stateless workflow orchestrator that automatically selects the optimal workflow based on task intent.

## Workflow System Overview

CCW provides two workflow systems: **Main Workflow** and **Issue Workflow**, covering the complete software development lifecycle.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Main Workflow                                  │
│                                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │
│  │   Level 1   │ → │   Level 2   │ → │   Level 3   │ → │   Level 4   │     │
│  │   Rapid     │   │ Lightweight │   │  Standard   │   │ Brainstorm  │     │
│  │             │   │             │   │             │   │             │     │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘     │
│                                                                             │
│  Complexity: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━▶  │
│              Low                                                    High    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ After development
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Issue Workflow                                 │
│                                                                             │
│     ┌──────────────┐         ┌──────────────┐         ┌──────────────┐     │
│     │  Accumulate  │    →    │    Plan      │    →    │   Execute    │     │
│     │  Discover &  │         │    Batch     │         │   Parallel   │     │
│     │   Collect    │         │   Planning   │         │  Execution   │     │
│     └──────────────┘         └──────────────┘         └──────────────┘     │
│                                                                             │
│     Supplementary role: Maintain main branch stability, worktree isolation  │
└─────────────────────────────────────────────────────────────────────────────┘

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  CCW Orchestrator (CLI-Enhanced + Requirement Analysis)         │
├─────────────────────────────────────────────────────────────────┤
│  Phase 1    │ Input Analysis (rule-based, fast path)            │
│  Phase 1.5  │ CLI Classification (semantic, smart path)         │
│  Phase 1.75 │ Requirement Clarification (clarity < 2)           │
│  Phase 2    │ Level Selection (intent → level → workflow)       │
│  Phase 2.5  │ CLI Action Planning (high complexity)             │
│  Phase 3    │ User Confirmation (optional)                      │
│  Phase 4    │ TODO Tracking Setup                               │
│  Phase 5    │ Execution Loop                                    │
└─────────────────────────────────────────────────────────────────┘

## Level Quick Reference

| Level | Name | Workflows | Artifacts | Execution |
|-------|------|-----------|-----------|-----------|
| **1** | Rapid | `lite-lite-lite` | None | Direct execute |
| **2** | Lightweight | `lite-plan`, `lite-fix`, `multi-cli-plan` | Memory/Lightweight files | → `lite-execute` |
| **3** | Standard | `plan`, `tdd-plan`, `test-fix-gen` | Session persistence | → `execute` / `test-cycle-execute` |
| **4** | Brainstorm | `brainstorm:auto-parallel` → `plan` | Multi-role analysis + Session | → `execute` |
| **-** | Issue | `discover` → `plan` → `queue` → `execute` | Issue records | Worktree isolation (optional) |

## Workflow Selection Decision Tree

```
Start
  │
  ├─ Is it post-development maintenance?
  │     ├─ Yes → Issue Workflow
  │     └─ No ↓
  │
  ├─ Are requirements clear?
  │     ├─ Uncertain → Level 4 (brainstorm:auto-parallel)
  │     └─ Clear ↓
  │
  ├─ Need persistent Session?
  │     ├─ Yes → Level 3 (plan / tdd-plan / test-fix-gen)
  │     └─ No ↓
  │
  ├─ Need multi-perspective / solution comparison?
  │     ├─ Yes → Level 2 (multi-cli-plan)
  │     └─ No ↓
  │
  ├─ Is it a bug fix?
  │     ├─ Yes → Level 2 (lite-fix)
  │     └─ No ↓
  │
  ├─ Need planning?
  │     ├─ Yes → Level 2 (lite-plan)
  │     └─ No → Level 1 (lite-lite-lite)
```

## Intent Classification

### Priority Order (with Level Mapping)

| Priority | Intent | Patterns | Level | Flow |
|----------|--------|----------|-------|------|
| 1 | bugfix/hotfix | `urgent,production,critical` + bug | L2 | `bugfix.hotfix` |
| 1 | bugfix | `fix,bug,error,crash,fail` | L2 | `bugfix.standard` |
| 2 | issue batch | `issues,batch` + `fix,resolve` | Issue | `issue` |
| 3 | exploration | `不确定,explore,研究,what if` | L4 | `full` |
| 3 | multi-perspective | `多视角,权衡,比较方案,cross-verify` | L2 | `multi-cli-plan` |
| 4 | quick-task | `快速,简单,small,quick` + feature | L1 | `lite-lite-lite` |
| 5 | ui design | `ui,design,component,style` | L3/L4 | `ui` |
| 6 | tdd | `tdd,test-driven,先写测试` | L3 | `tdd` |
| 7 | test-fix | `测试失败,test fail,fix test` | L3 | `test-fix-gen` |
| 8 | review | `review,审查,code review` | L3 | `review-fix` |
| 9 | documentation | `文档,docs,readme` | L2 | `docs` |
| 99 | feature | complexity-based | L2/L3 | `rapid`/`coupled` |

### Quick Selection Guide

| Scenario | Recommended Workflow | Level |
|----------|---------------------|-------|
| Quick fixes, config adjustments | `lite-lite-lite` | 1 |
| Clear single-module features | `lite-plan → lite-execute` | 2 |
| Bug diagnosis and fix | `lite-fix` | 2 |
| Production emergencies | `lite-fix --hotfix` | 2 |
| Technology selection, solution comparison | `multi-cli-plan → lite-execute` | 2 |
| Multi-module changes, refactoring | `plan → verify → execute` | 3 |
| Test-driven development | `tdd-plan → execute → tdd-verify` | 3 |
| Test failure fixes | `test-fix-gen → test-cycle-execute` | 3 |
| New features, architecture design | `brainstorm:auto-parallel → plan → execute` | 4 |
| Post-development issue fixes | Issue Workflow | - |

### Complexity Assessment

```javascript
function assessComplexity(text) {
  let score = 0
  if (/refactor|重构|migrate|迁移|architect|架构|system|系统/.test(text)) score += 2
  if (/multiple|多个|across|跨|all|所有|entire|整个/.test(text)) score += 2
  if (/integrate|集成|api|database|数据库/.test(text)) score += 1
  if (/security|安全|performance|性能|scale|扩展/.test(text)) score += 1
  return score >= 4 ? 'high' : score >= 2 ? 'medium' : 'low'
}
```

| Complexity | Flow |
|------------|------|
| high | `coupled` (plan → verify → execute) |
| medium/low | `rapid` (lite-plan → lite-execute) |

### Dimension Extraction (WHAT/WHERE/WHY/HOW)

Extract four dimensions from user input for requirement clarification and workflow selection:

| Dimension | Extracted Content | Example Patterns |
|-----------|-------------------|------------------|
| **WHAT**  | action + target   | `创建/修复/重构/优化/分析` + target object |
| **WHERE** | scope + paths     | `file/module/system` + file path |
| **WHY**   | goal + motivation  | `为了.../因为.../目的是...` |
| **HOW**   | constraints + preferences | `必须.../不要.../应该...` |

**Clarity Score** (0-3):
- +0.5: Clear action
- +0.5: Specific target
- +0.5: File path
- +0.5: Scope is not unknown
- +0.5: Clear goal
- +0.5: Constraints present
- -0.5: Contains uncertain terms (`不知道/maybe/怎么`)

### Requirement Clarification

When `clarity_score < 2`, trigger requirement clarification:

```javascript
if (dimensions.clarity_score < 2) {
  const questions = generateClarificationQuestions(dimensions)
  // Generate questions: What is the target? What is the scope? What are the constraints?
  AskUserQuestion({ questions })
}
```

**Clarification Question Types**:
- Unclear target → "What do you want to operate on?"
- Unclear scope → "What is the scope of the operation?"
- Unclear purpose → "What is the main goal of this operation?"
- Complex operation → "Are there any special requirements or constraints?"

## TODO Tracking Protocol

### CRITICAL: Append-Only Rule

Todos created by CCW **must be appended to existing lists** and cannot overwrite the user's other todos.

### Implementation

```javascript
// 1. Use CCW prefix to isolate workflow todos
const prefix = `CCW:${flowName}`

// 2. Create new todos using prefix format
TodoWrite({
  todos: [
    ...existingNonCCWTodos,  // Preserve user's todos
    { content: `${prefix}: [1/N] /command:step1`, status: "in_progress", activeForm: "..." },
    { content: `${prefix}: [2/N] /command:step2`, status: "pending", activeForm: "..." }
  ]
})

// 3. Update status by modifying only matching prefix todos
```

### Todo Format

```
CCW:{flow}: [{N}/{Total}] /command:name
```

### Visual Example

```
✓ CCW:rapid: [1/2] /workflow:lite-plan
→ CCW:rapid: [2/2] /workflow:lite-execute
  User's own todos (remain unchanged)
```

### Status Management

- Start workflow: Create all step todos, first step `in_progress`
- Complete step: Current step `completed`, next step `in_progress`
- End workflow: All CCW todos marked `completed`

## Execution Flow

```javascript
// 1. Check explicit command
if (input.startsWith('/workflow:') || input.startsWith('/issue:')) {
  SlashCommand(input)
  return
}

// 2. Classify intent
const intent = classifyIntent(input)  // See command.json intent_rules

// 3. Select flow
const flow = selectFlow(intent)  // See command.json flows

// 4. Create todos with CCW prefix
createWorkflowTodos(flow)

// 5. Dispatch first command
SlashCommand(flow.steps[0].command, args: input)
```

## CLI Tool Integration

CCW automatically injects CLI calls under specific conditions:

| Condition | CLI Inject |
|-----------|------------|
| Large code context (≥50k chars) | `gemini --mode analysis` |
| High complexity task | `gemini --mode analysis` |
| Bug diagnosis | `gemini --mode analysis` |
| Multi-task execution (≥3 tasks) | `codex --mode write` |

### CLI Enhancement Phases

**Phase 1.5: CLI-Assisted Classification**

When rule matches are ambiguous, use CLI-assisted classification:

| Trigger Condition | Description |
|-------------------|-------------|
| matchCount < 2    | Multiple intent patterns matched |
| complexity = high  | High complexity task |
| input > 100 chars  | Long input requires semantic understanding |

**Phase 2.5: CLI-Assisted Action Planning**

Workflow optimization for high complexity tasks:

| Trigger Condition | Description |
|-------------------|-------------|
| complexity = high  | High complexity task |
| steps >= 3        | Multi-step workflow |
| input > 200 chars  | Complex requirement description |

CLI can return suggestions: `use_default` | `modify` (adjust steps) | `upgrade` (upgrade workflow)

## Continuation Commands

User control commands during workflow execution:

| Command | Effect |
|---------|--------|
| `continue` | Proceed to the next step |
| `skip` | Skip the current step |
| `abort` | Terminate the workflow |
| `/workflow:*` | Switch to specified command |
| Natural language | Re-analyze intent |

## Workflow Flow Details

### Issue Workflow (Supplementary Mechanism to Main Workflow)

The Issue Workflow is a **supplementary mechanism** to the Main Workflow, focusing on ongoing maintenance after development.

#### Design Philosophy

| Aspect | Main Workflow | Issue Workflow |
|--------|---------------|----------------|
| **Purpose** | Main development cycle | Post-development maintenance |
| **Timing** | Feature development phase | After main workflow completion |
| **Scope** | Complete feature implementation | Targeted fixes/enhancements |
| **Parallelism** | Dependency analysis → Agent parallelism | Worktree isolation (optional) |
| **Branch Model** | Current branch work | Can use isolated worktree |

#### Why doesn't the Main Workflow automatically use Worktree?

**Dependency analysis has resolved parallelism issues**:
1. Planning phase (`/workflow:plan`) performs dependency analysis
2. Automatically identifies task dependencies and critical paths
3. Divides into **parallel groups** (independent tasks) and **serial chains** (dependent tasks)
4. Agent executes independent tasks in parallel without file system isolation

#### Two-Phase Lifecycle

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Phase 1: Accumulation (积累阶段)                  │
│                                                                     │
│   Triggers: Task completion reviews, code review findings, test failures |
│                                                                     │
│   ┌────────────┐     ┌────────────┐     ┌────────────┐             │
│   │ discover   │     │ discover-  │     │    new     │             │
│   │ Auto-find  │     │ by-prompt  │     │  Manual    │             │
│   └────────────┘     └────────────┘     └────────────┘             │
│                                                                     │
│   Continuously accumulate issues into the pending queue              │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               │ After sufficient accumulation
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  Phase 2: Batch Resolution (批量解决阶段)            │
│                                                                     │
│   ┌────────────┐     ┌────────────┐     ┌────────────┐             │
│   │   plan     │ ──→ │   queue    │ ──→ │  execute   │             │
│   │ --all-     │     │ Optimize   │     │  Parallel  │             │
│