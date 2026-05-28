---
name: unitwork
description: "This skill should be used when implementing features with human-in-the-loop verification. It provides the core Unit Work methodology including checkpoint-based development, confidence assessment, memory integration with Hindsight, and verification strategies. Use this skill for planning features, executing with checkpoints, reviewing code, and compounding learnings."
---

# Unit Work - Human-in-the-Loop Verification Framework

> "The largest task an AI can self-validate to 100% accuracy, that is also able to get validated by the minimum amount of human review"

## Core Philosophy

Unit Work replaces arbitrary development phases with a verification-driven approach:

1. **Front-load work** in interview and planning stages
2. **Use Hindsight memory** to compound learnings across sessions
3. **NEVER skip memory recall** - it's the foundation that makes compounding work
4. **Create checkpoints** at verifiable boundaries, not arbitrary phases
5. **Treat commits as checkpoints** with verification documents
6. **Know your gaps** and invite human verification where AI is weak

## AI Capability Awareness

**AI is strong at verifying:**
- API endpoints (especially with before/after DB state)
- Backend logic and data transformations
- Test execution and result parsing

**AI is weak at verifying:**
- Visual design and layout
- UI component placement and spacing
- Spatial relationships ("does X overlap Y")

The plugin adapts confidence and checkpoint behavior based on these strengths/weaknesses.

## Workflow Overview

```
/uw:plan -> /uw:work -> /uw:review -> /uw:compound
    |           |            |             |
  Spec.md   Checkpoints   Code Review   Learnings
            + Verify.md   + Fix Loop    to memory
                              |
                          Create PR
```

## Decision Trees

See [decision-trees.md](./references/decision-trees.md) for detailed decision flows:
- When to checkpoint
- When to ask user vs decide autonomously
- When to use each memory operation
- Which verification subagent to use

## Templates

- [Spec Template](./templates/spec.md) - Feature specification format
- [Verify Template](./templates/verify.md) - Checkpoint verification document
- [Learnings Template](./templates/learnings.md) - Compound phase output

## Directory Structure

Unit Work creates this structure in your project:

```
.unitwork/
├── specs/           # {DD-MM-YYYY}-{feature}.md
├── verify/          # {DD-MM-YYYY}-{n}-{name}.md
├── review/          # Code review findings
└── learnings/       # Compound phase output
```

## Agent Behavior Rules

### Interview Phase

See [interview-workflow.md](./references/interview-workflow.md) for the complete interview protocol including confidence-based depth assessment and stop conditions.

1. Research before asking - check Hindsight, codebase, then web docs
2. Group related questions - don't ask one at a time
3. Push back on scope - "That sounds like a separate feature"
4. Advocate once - state recommendation, then accept decision
5. No premature solutions - don't propose implementation during requirements
6. Confirm understanding - summarize before writing spec

### Implementation Phase
1. Follow the spec - it's the contract
2. Minimal changes - smallest diff that satisfies requirement
3. No drive-by refactoring - note tech debt, don't fix it
4. No drive-by bug fixes - unless critical and blocking
5. Checkpoint at boundaries - every verifiable unit
6. Document uncertainty - say so in checkpoint
7. Never skip verification - even if confident

### Verification Phase
1. Tests first - always run relevant tests
2. API safety - never call mutating endpoints without permission
3. Screenshot everything - UI changes always get screenshots
4. Explicit confidence - state percentage with rationale
5. Human QA reproducible - no LLM-dependent steps
6. Precursor state documented - if testing needs setup, document how

### Memory Rules

**CRITICAL: Memory recall is the foundation of compounding. Skip it and you lose all accumulated learnings.**

0. **NEVER skip memory recall at session start** - this is non-negotiable
1. Always async - never block on memory writes
2. Always contextualized - include repo name and work context
3. Document tracking - group by feature doc-id
4. Narrative format - write as natural language
5. Retain discoveries immediately - don't wait for phase end
6. Blind spots are critical - always retain when human finds what agent missed

## Checkpoint Protocol

See [checkpointing.md](./references/checkpointing.md) for the complete checkpointing reference including:
- **Checkpoint Commit Format** - Standard commit message format
- **When to Checkpoint** - Decision tree in [decision-trees.md](./references/decision-trees.md#when-to-checkpoint)
- **Verification Document** - Template at [templates/verify.md](./templates/verify.md)
- **Self-Correcting Review** - Protocol for fix checkpoints

## Hindsight Integration

See [hindsight-reference.md](./references/hindsight-reference.md) for complete patterns including:
- **Bank Name Derivation** - Worktree-safe bank name extraction
- **ANSI Stripping** - Required when processing output programmatically
- **Memory Operations** - Recall, retain, and reflect patterns
- **Error Handling** - Graceful degradation when Hindsight unavailable

### Quick Reference

```bash
# Bank name (worktree-safe)
BANK=$(git config --get remote.origin.url 2>/dev/null | sed 's/.*\///' | sed 's/\.git$//' || basename "$(git worktree list 2>/dev/null | head -1 | awk '{print $1}')" || basename "$(pwd)")

# Recall with ANSI stripping
hindsight memory recall "$BANK" "query" --budget mid --include-chunks 2>&1 | sed 's/\x1b\[[0-9;]*m//g'

# Retain (always async)
hindsight memory retain "$BANK" "narrative" --context "context" --doc-id "id" --async
```

## Context7 Integration

Context7 provides framework documentation lookup via MCP. Use it when implementing unfamiliar APIs.

### Usage

```
Step 1: Resolve library ID
mcp__unitwork_context7__resolve-library-id
  query: "what you're trying to implement"
  libraryName: "framework-name"

Step 2: Query documentation
mcp__unitwork_context7__query-docs
  libraryId: "/org/project"  (from step 1)
  query: "specific API or pattern"
```

### When to Use
- Unfamiliar framework APIs (check docs before guessing)
- Best practices for specific patterns
- Version-specific behavior differences
- Implementation examples from official docs

### When NOT to Use
- Project-specific patterns (use Hindsight)
- Simple/well-known APIs
- Already checked docs this session

## Verification Subagents

| Subagent/Skill | Purpose | When to Use |
|----------------|---------|-------------|
| test-runner | Execute tests | Changed test files or tested code |
| api-prober | Probe API endpoints | Changed API endpoints |
| agent-browser (skill) | UI verification | Changed UI components |

## Review Agents (Parallel)

| Agent | Focus |
|-------|-------|
| type-safety | Casting, guards, nullability |
| patterns-utilities | Existing solutions, duplication |
| performance-database | N+1, indexes, parallelization |
| architecture | Structure, coupling, boundaries |
| security | Injection, auth, data exposure |
| simplicity | Over-engineering, YAGNI |
| memory-validation | Learnings from Hindsight memory |

## Confidence Assessment

Start at 100%, subtract:
- -5% for each untested edge case
- -20% if UI layout changes
- -10% if complex state management
- -15% if external API integration

**>= 95%**: Checkpoint and continue
**< 95%**: Checkpoint and pause for human review

## Commands

- `/uw:plan` - Interview and create spec
- `/uw:work` - Execute with checkpoints
- `/uw:review` - Parallel code review
- `/uw:compound` - Extract learnings
- `/uw:bootstrap` - First-time setup
- `/uw:pr` - Create/update GitHub PRs
- `/uw:action-comments` - Resolve PR comments
- `/uw:fix-ci` - Autonomously fix failing CI
- `/uw:fix-conflicts` - Intelligent rebase conflict resolution
