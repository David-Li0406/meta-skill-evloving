# PRD Creation Skill

A skill for creating self-verifying Product Requirements Documents (PRDs) optimized for autonomous AI execution. This skill guides intelligent interviews to gather requirements and generates structured PRDs with phased implementation plans.

## What This Skill Does

This skill transforms user ideas into executable PRDs through:

1. **Intelligent Interviewing** - Adapts questioning based on task type and complexity
2. **Category-Specific Workflows** - Applies appropriate methodologies for features, bugs, research, QA, maintenance, DevOps, or general tasks
3. **Structured Output** - Generates both human-readable PRD.md and machine-readable prd.json
4. **Verification-First Design** - Every task includes clear acceptance criteria and testing strategies

## When to Use

Trigger this skill when users want to:
- Create a PRD or product requirements document
- Plan a feature implementation
- Structure a bug fix approach
- Design a research spike
- Organize maintenance work
- Plan a deployment

**Trigger phrases:** "create a prd", "prd for", "plan a feature", "plan this", "write prd", "ralph prd", or any request for structured planning.

## How It Works

```
1. User invokes skill
2. Identify task category (feature, bug, research, QA, maintenance, devops, general)
3. Gather brain dump - let user share everything they know
4. Ask clarifying questions - adapt to what's actually needed
5. Present understanding and get approval
6. Generate PRD.md and prd.json
7. Provide execution guidance
```

## File Structure

```
prd/
├── README.md                    # This file - overview
├── SKILL.md                     # Entry point (loaded on invocation)
├── AGENTS.md                    # Comprehensive reference document
├── interview/                   # Interview process guidance
│   ├── _overview.md             # How interviews work
│   ├── brain-dump.md            # Gathering initial information
│   ├── clarifying-questions.md  # Formulating good questions
│   └── confirmation.md          # Validating understanding
└── categories/                  # Task-type specific guidance
    ├── _overview.md             # Category selection
    ├── feature-development.md   # New features and enhancements
    ├── bug-fixing.md            # Investigation and fixes
    ├── research-planning.md     # Exploration and architecture
    ├── quality-assurance.md     # Testing and audits
    ├── maintenance.md           # Cleanup and refactoring
    ├── devops.md                # Deployment and infrastructure
    └── general.md               # Adaptive approach
```

## Key Principles

**Guidelines over templates** - This skill provides thinking frameworks, not scripts to follow. The model decides how to adapt based on the specific situation.

**Progressive disclosure** - SKILL.md provides entry-point guidance and references deeper documentation only when needed.

**Agent Browser CLI integration** - Browser verification is emphasized throughout for any visual or interactive work.

**Intelligent adaptation** - The number of interview rounds, depth of questions, and verification approach all depend on task complexity.

## Output Format

### PRD.md (Human-readable)
- Overview and goals
- Non-goals and scope boundaries
- Technical approach
- Phase summary
- Testing strategy
- Risks and mitigations

### prd.json (Machine-readable)
Structured format for Ralph TUI execution with user stories, tasks, acceptance criteria, and dependencies.

## Quick Reference

| File | Purpose |
|------|---------|
| `SKILL.md` | Entry point - high-level guidance |
| `AGENTS.md` | Deep reference - comprehensive details |
| `interview/*.md` | Interview phase guidance |
| `categories/*.md` | Task-type specific principles |

## Related Tools

- **Ralph TUI** - Executes prd.json files autonomously
- **Agent Browser CLI** - Visual/interactive verification
