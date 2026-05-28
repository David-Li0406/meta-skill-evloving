# Smart-Dev: Feature Development Workflow

A systematic 5-phase workflow for feature development with dual-mode execution, 95% readiness gating, and iteration control.

## Overview

This skill provides a structured approach to feature development:

1. **Discovery** - Clarify requirements, make product decisions
2. **Exploration** - Understand existing codebase patterns
3. **Documentation & Readiness Gate** - Create spec documents with 95% confidence check before implementation
4. **Implementation** - Build incrementally with verification
5. **Review & PR** - Ensure quality and submit

## Execution Modes

### Dev Mode (Single-Shot)
Execute the full workflow once with readiness gating:
```
/smart-dev:dev "Add user profile feature"
```

**Features**:
- One-time execution through all 5 phases
- 95% readiness gate at Phase 3c (blocks implementation until spec is complete)
- Verification retry (max 3 attempts)
- Graceful failure reporting

### Loop Mode (Iterative)
Continuous iteration until completion or timeout:
```
/smart-dev:loop "Add GraphQL subscriptions" --max-iterations 20
```

**Features**:
- Automatic retry until verification passes
- Stop hook prevents premature exit
- Iteration budget (default: 20)
- Completion promise detection ("DONE")
- Graceful cancellation: `/smart-dev:cancel {feature-name}`

## Key Features

### 95% Readiness Gate (Phase 3c)
**Dual-track scoring** before implementation:

- **Track A (Structural)**: Deterministic checks (0-100 points)
  - Structure completeness (25 pts)
  - Testability criteria (25 pts)
  - Interface definitions (15 pts)
  - Constraint specifications (15 pts)
  - Verification plan (20 pts)
  - Penalties for placeholders, TODOs, missing sections

- **Track B (Semantic)**: LLM-based sufficiency check
  - Goal clarity and measurability
  - Success criteria alignment with user intent
  - Edge case coverage
  - Evidence-based evaluation with citations

**Question Budget**: Max 2 Q&A rounds to prevent infinite loops
**Fallback**: Assumptions pack when budget exhausted (user accepts/rejects)

### Other Features

- **Multi-model agents**: Right model for each task
  - Opus for deep product thinking
  - Haiku for fast exploration and semantic checks
  - Sonnet for architecture, implementation, and review
- **Progress persistence**: Resume interrupted work seamlessly
- **Fork context**: Agents don't pollute main session context
- **Spec lock enforcement**: Write guard prevents spec edits after readiness gate passes
- **Documentation-first**: Spec documents validated before code

## Installation

Add this skill to your Claude Code marketplace:

```bash
claude plugin marketplace add royisme/agent-skills
claude plugin install feature-development-workflow
```

Or add to `.claude/settings.json`:

```json
{
  "plugins": {
    "marketplaces": ["royisme/agent-skills"]
  }
}
```

## Usage

### Commands

**Dev Mode (Single-Shot)**:
```bash
/smart-dev:dev "Feature description" [--confidence-threshold 95] [--question-rounds 2]
```

**Loop Mode (Iterative)**:
```bash
/smart-dev:loop "Feature description" [--max-iterations 20] [--confidence-threshold 95]
```

**Cancel Loop**:
```bash
/smart-dev:cancel [feature-name]
```

### Automatic Invocation

The skill also auto-triggers when you say:
- "implement a feature"
- "add new feature"
- "use /smart-dev"

Example:
```
User: I want to add user authentication with OAuth
Claude: [Launches smart-dev skill in dev mode]
        Let me help you implement this feature systematically...
```

## File Structure

The skill creates spec files in `.works/spec/{feature-name}/`:

```
.works/spec/{feature-name}/
├── progress.md            # Progress tracking (YAML frontmatter + markdown)
├── README.md              # Index + decisions
├── contracts.md           # Data contracts
├── tasks.md               # Task breakdown
├── PR.md                  # PR template
├── qa.md                  # Q&A log (question rounds)
├── score.json             # Readiness scoring results (Track A)
├── semantic-check.json    # Semantic sufficiency check (Track B)
├── verification.log       # Test/build output history
├── assumptions.md         # Assumptions pack (if question budget exhausted)
└── spec.lock              # Spec freeze marker (created after readiness gate passes)
```

## Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `product-thinker` | Opus | Deep product decisions, UX analysis |
| `codebase-explorer` | Haiku | Fast codebase exploration |
| `architect` | Sonnet | Architecture design |
| `reviewer` | Sonnet | Code quality review |
| `react-coder` | Sonnet | Code writer |

## Scripts

| Script | Purpose |
|--------|---------|
| `init.sh {name}` | Initialize feature workspace (creates 11 files) |
| `check-progress.sh` | Check for incomplete features |
| `update-progress.sh` | Update progress state (supports --set-field) |
| `update-changelog.sh` | Update CHANGELOG.md |
| `score-spec.ts {feature}` | Run Track A structural scoring |
| `check-semantic.ts {feature}` | Run Track B semantic sufficiency check |
| `loop-stop.sh` | Stop hook for iteration control (blocks premature exit) |
| `guard-writes.sh` | PreToolUse hook for spec-lock enforcement |

## Requirements

- Claude Code 2.1.0+ (for `context: fork` support)
- Git repository
- Project with existing codebase

## License

MIT
