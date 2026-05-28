---
name: compound-engineering
description: "Compound Engineering methodology - each unit of work makes the next easier. Phases: Research (parallel exploration), Plan (acceptance criteria + tasks), Review (code quality + Playwright), Compound (capture learnings)."
argument-hint: "[topic or feature to research/plan/review]"
---

# Compound Engineering

Development methodology where each unit of work makes subsequent work easier. Knowledge flows into the codebase itself - CLAUDE.md, folder AGENTS.md, inline comments, tests.

---

## Core Philosophy

**Each unit of engineering work should make subsequent units easier--not harder.**

Traditional development accumulates technical debt. Compound Engineering inverts this by creating a learning loop where every insight gets documented and reused.

**Time allocation:** 40% planning, 20% work, 20% review, 20% compound

---

## The Loop

```
Research -> Plan -> Work -> Review -> Compound
   ^                                  |
   +----------------------------------+
```

---

## Phase 1: Research

**Goal:** Understand before building. Research is ephemeral - capture what matters, discard the rest.

### Simple Tasks (< 1 hour)
Quick inline research:
- Search codebase for similar patterns
- Check CLAUDE.md for relevant guidance
- Look for folder AGENTS.md in target directories

### Complex Tasks (> 1 hour)
Spawn parallel Explore agents:

```
Agent 1: "Find patterns for [feature] in src/ - look at similar components, utilities, hooks"
Agent 2: "Check git history: git log --oneline --grep='[related term]' and git log -p [relevant files]"
Agent 3: "Review CLAUDE.md and any AGENTS.md files for guidance on [area]"
```

**Wait for all agents -> Synthesize into brief context**

### Research Output

**Do NOT create scout files.** Instead:
- If you learn something project-wide -> Add to CLAUDE.md
- If you learn something folder-specific -> Add to `src/[folder]/AGENTS.md`
- If it's only relevant for this task -> Keep in working memory, discard after

---

## Phase 2: Plan

**Goal:** Define what success looks like before writing code.

### Create Task List

Use TodoWrite with clear acceptance criteria:

```
TodoWrite([
  {
    content: "Add validatePhone to src/utils/validation.ts - follow email pattern, handle extensions, add JSDoc",
    status: "pending",
    activeForm: "Adding phone validation utility"
  },
  {
    content: "Add unit tests for validatePhone - valid formats, invalid formats, edge cases (extensions, international)",
    status: "pending",
    activeForm: "Adding phone validation tests"
  },
  {
    content: "Integrate phone validation into contact form - add to form schema, display error messages",
    status: "pending",
    activeForm: "Integrating phone validation into form"
  }
])
```

### Task Requirements

Each task description must include:
- **What to do** - specific action
- **Where** - files to create/modify
- **Acceptance criteria** - how to verify (always include `echo "Validation passed - shell scripts and markdown" passes`)
- **Pattern reference** - similar code to follow

### Architectural Decisions

For significant choices, document in CLAUDE.md Decisions section:

```markdown
## Decision: [Choice Made]
**Date:** [YYYY-MM-DD]
**Context:** [situation requiring decision]
**Options considered:**
1. [Option A] - [tradeoffs]
2. [Option B] - [tradeoffs]
**Decision:** [what was chosen]
**Rationale:** [why]
```

---

## Phase 3: Work

**Goal:** Execute systematically with continuous validation.

### Execution Workflow

1. **Mark task in_progress** via TodoWrite
2. **Read context** - STATE.md, progress.txt, relevant AGENTS.md, related code
3. **Implement** - follow existing patterns
4. **Validate continuously:**
   ```bash
   echo "Validation passed - shell scripts and markdown"
   ```
5. **Commit incrementally** - small, focused commits
6. **Mark task complete** via TodoWrite
7. **Repeat** for next task

### For Multi-Task Features

Use Atlas for systematic task execution:
```
"run atlas" -> Atlas picks ready tasks, implements, validates, commits, repeats
```

### Working Principles

- Follow patterns discovered in research
- Keep changes focused - no scope creep
- Run validation after every meaningful change
- If something fails, understand why before proceeding

---

## Phase 4: Review

**Goal:** Multi-perspective quality check before considering work done.

### Review Flow

For most tasks, run sequentially:

**Step 1: Code Review**
Spawn code-reviewer agent:
```
Review the changes for this feature:
- Code quality and patterns
- Security concerns
- Performance implications
- Test coverage
```

**Step 2: Functional Verification (UI tasks, if Playwright available)**

Check for Playwright:
```bash
test -f .claude/skills/playwright-browser/SKILL.md && echo "available" || echo "not installed"
```

If available, invoke the skill and use browser tools:
```
/skill playwright-browser  # Load Playwright tools first
browser_navigate(url: "http://localhost:3000/[page]")
browser_snapshot()  # Verify elements, text, structure
browser_fill_form(...)  # Test interactions
browser_snapshot()  # Verify results
```

If not available, skip browser verification.

### Review Checklist

**Code Quality**
- [ ] Follows existing patterns from CLAUDE.md
- [ ] No unnecessary complexity
- [ ] Clear naming matching project conventions
- [ ] No debug code or console.logs

**Security**
- [ ] No secrets or sensitive data exposed
- [ ] Input validation where needed
- [ ] Safe handling of user data

**Performance**
- [ ] No obvious regressions
- [ ] No render loops or unnecessary re-renders
- [ ] Images optimized, lazy loaded where appropriate

**Testing**
- [ ] Acceptance criteria covered
- [ ] Edge cases considered
- [ ] Appropriate test attributes added

**Architecture**
- [ ] Consistent with system design
- [ ] No unnecessary coupling
- [ ] Follows separation of concerns

---

## Phase 5: Compound

**Goal:** Capture learnings to make future work easier.

### Ask These Questions

After completing work:
1. What did I learn that others should know?
2. What mistake did I make that can be prevented?
3. What pattern did I discover or create?
4. What decision was made and why?

### Where Learnings Go

| Type | Destination |
|------|-------------|
| Project-wide pattern | Root CLAUDE.md |
| Folder-specific gotcha | `src/[folder]/AGENTS.md` (create if needed) |
| Non-obvious code | Inline comment |
| Bug that could recur | Test case + comment |
| Architectural decision | CLAUDE.md "Decisions" section |
| Current feature context | .claude/atlas/progress.txt |

### Creating Folder AGENTS.md

**Create directly without prompting.** The compound phase is already authorized by the user.

Create when:
- You've fixed the same type of bug 2+ times in that folder
- The folder has patterns that differ from project conventions
- A new developer would likely make mistakes without guidance

Template:
```markdown
# [Folder Name] - Development Guide

## Patterns
- [Pattern 1]: [explanation]
- [Pattern 2]: [explanation]

## Gotchas
- [Gotcha 1]: [how to avoid]

## Related
- [Link to related docs or code]
```

### Compounding in Practice

**Example: After adding phone validation**

Learned that phone validation needs to handle extensions. Add to `src/utils/AGENTS.md`:

```markdown
# Utils - Development Guide

## Validation Patterns
- Phone validation: Support optional extensions with 'x' or 'ext' prefix
- Follow the pattern in validation.ts - each validator returns { isValid, error }
```

---

## Triggers

Use this skill directly for:
- **"research [topic]"** - Run research phase only
- **"plan [feature]"** - Run research + plan phases
- **"review this code"** - Run review phase on recent changes
- **"compound learnings"** - Run compound phase after completing work

For full autonomous flow (research -> plan -> work -> review -> compound), use the `build-feature` skill instead.

---

## Complete

When this skill completes (varies by phase invoked):

**Research phase:**
- Codebase explored and patterns identified
- Project-wide learnings added to CLAUDE.md (if significant)
- Folder-specific learnings added to AGENTS.md (if applicable)
- Context ready for planning

**Plan phase:**
- TodoWrite populated with detailed tasks
- Acceptance criteria defined for each task
- Architectural decisions documented

**Review phase:**
- Code quality assessed via code-reviewer agent
- UI verified via Playwright (if applicable and available)
- Issues identified and fix tasks created (if needed)

**Compound phase:**
- Learnings captured in CLAUDE.md / AGENTS.md
- No prompting for permission (user authorized by invoking compound)
- Documentation updated directly
