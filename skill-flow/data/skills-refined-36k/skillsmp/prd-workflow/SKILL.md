---
name: prd-workflow
description: |
  This skill should be used when the user asks to "plan a feature", "create PRD",
  "interview me about requirements", "define stories", "write a spec", "break down
  feature into tasks", "create implementation plan", "help me scope this feature",
  "what questions should I answer", or discusses feature planning. Covers the PRD
  interview process, spec structure, story atomization, and phased workflow from
  idea to implementable stories.
version: 1.0.0
---

# PRD Workflow - Feature Planning

**Current branch:** !`git branch --show-current 2>/dev/null || echo "not in git repo"`
**Existing plans:** !`ls plans/ 2>/dev/null | head -5 || echo "none"`

The PRD (Product Requirements Document) workflow transforms ideas into atomic,
implementable stories through structured interview, research, and specification.

## When to Use PRD Workflow

- Starting a new feature from scratch
- Turning a vague idea into concrete tasks
- Need thorough requirements gathering
- Want AI-assisted research and review

## The Phased Approach

The PRD workflow progresses through six phases:

| Phase | Name | Purpose |
|-------|------|---------|
| 1 | Input Classification | Identify feature name and type |
| 2 | Deep Interview | Gather requirements through questions |
| 2.5 | Research | Parallel research (codebase, external, git history) |
| 3 | Spec Write | Create comprehensive specification |
| 3.5 | Review Gate | Parallel expert reviews |
| 4-6 | PRD Generation | Create atomic stories, prepare for implementation |

## Starting the Workflow

```bash
/prd "Add user authentication"           # From idea
/prd path/to/existing/code               # From codebase
/prd                                     # Interactive discovery
```

## Interview Philosophy

**"Be annoyingly thorough."**

The interview phase asks 8-15 questions across multiple waves:

- **Wave 1** (3-4 questions): Core problem, success criteria, MVP scope
- **Research break**: Parallel agents gather context
- **Waves 2-5**: Technical details, UX, edge cases, tradeoffs

Focus on **non-obvious** details - edge cases, error states, and tradeoffs that
will bite during implementation.

## Output Structure

The workflow produces two files in `plans/<feature>/`:

```
plans/auth-feature/
├── spec.md        # Comprehensive specification
└── prd.json       # Atomic stories with embedded progress log
```

## Story Atomization Rules

Each story must be completable in ONE iteration (~15-30 min):

- **Max 7 verification steps** - If more, split the story
- **Max 3 files touched** - If more, consider splitting
- **No "and" in title** - "User can X and Y" = two stories
- **Independently testable** - Can verify in isolation
- **Cleanly revertible** - Can undo without cascade

## After PRD Completion

The workflow ends with a choice:

1. **Run `/go` now** - Start implementing immediately
2. **Run `/go --once`** - Single iteration to test
3. **Done** - Review PRD first, implement later

## Command Reference

```bash
/prd "feature description"     # Start from idea
/prd path/to/code             # Start from codebase
/cancel-prd                   # Cancel in-progress PRD
```

## Additional Resources

### Reference Files

- **`references/story-schema.md`** - PRD JSON schema and examples
