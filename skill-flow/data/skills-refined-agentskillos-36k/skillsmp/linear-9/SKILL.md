---
name: linear
description: "Intelligent work tracking. Automatically classifies issues, gathers codebase context, and creates well-formed Linear tickets. Triggers - linear, issue, track, bug, todo, fix, question, debt."
---

# Linear Issue Management

**Iron Law:** CONTEXT IS KING. Every issue must have enough context for anyone to understand and act on it.

## How This Skill Works

This skill is **autonomous**. When invoked:

1. **Classify** - Determine issue type from context (don't ask the user)
2. **Investigate** - Use explore agent to gather codebase context
3. **Create** - Build a well-formed Linear issue with full context
4. **Confirm** - Show the user what will be created

The user should NOT need to specify "bug" or "todo" - the AI infers this.

---

## Issue Classification

Automatically determine issue type from the request:

| Signal | Classification |
|--------|----------------|
| "broken", "fails", "error", "crash", "doesn't work" | **Bug** |
| "should we", "what if", "which approach", "decide" | **Question** |
| "need to", "add", "implement", "create", "build" | **Feature** or **TODO** |
| "refactor", "clean up", "improve", "migrate", "deprecated" | **Tech Debt** |
| Multi-step work with phases | **Feature** (hierarchical) |
| Single action, quick fix | **TODO** (flat) |

### Classification Logic

```
Is something broken/failing?
├── YES → Bug
└── NO → Is it a decision/discussion?
    ├── YES → Question
    └── NO → Is it improvement to existing code?
        ├── YES → Tech Debt
        └── NO → Is it multi-phase work?
            ├── YES → Feature (hierarchical)
            └── NO → TODO (single issue)
```

**Do NOT ask the user what type it is.** Infer from context.

---

## Context Gathering

Before creating any issue, **investigate the codebase** to add relevant context.

### Step 1: Dispatch Explore Agent

```markdown
Task: @Explore (subagent_type: "Explore")

Investigate context for: "{user's request}"

Find:
1. Relevant files that will be affected
2. Existing patterns in the codebase
3. Related code or similar implementations
4. Potential dependencies or blockers

Return:
- File paths with line numbers
- Code snippets showing current state
- Pattern observations
```

### Step 2: Extract Context

From explore results, extract:

- **Files involved**: Exact paths to relevant files
- **Current state**: What exists now (for bugs/debt)
- **Patterns**: How similar things are done in the codebase
- **Dependencies**: What this work depends on or affects

### Step 3: Enrich Issue

Add gathered context to the issue description automatically.

---

## Issue Templates

Templates are stored in external files to reduce context size. Read the appropriate template when creating an issue:

| Type | Template File | Use When |
|------|---------------|----------|
| Bug | `templates/bug.md` | Something is broken or failing |
| TODO | `templates/todo.md` | Quick, standalone task |
| Question | `templates/question.md` | Decision or discussion needed |
| Tech Debt | `templates/tech-debt.md` | Improvement or refactoring |
| Feature | `templates/feature.md` | Multi-phase hierarchical work |

**To use:** Read the template file for the classified issue type, then fill in the template with gathered context.

---

## Hierarchical Feature Planning

For complex, multi-phase work, create a hierarchy. See `templates/feature.md` for full templates.

```
ENG-100: [Feature] {Feature Name}
├── ENG-101: [Phase 1] {Phase Name}
│   ├── ENG-102: {Atomic task}
│   └── ENG-103: {Atomic task}
├── ENG-104: [Phase 2] {Phase Name}
│   └── ...
└── ENG-105: [Phase N] Verification
    └── ...
```

**Key principle:** Every leaf task must be immediately executable with a single unit of work.

### CRITICAL: Use `parentId` for Sub-Issues

```
# 1. Create root feature → returns { id: "uuid-100", identifier: "ENG-100" }
# 2. Create phases with parentId:
mcp__linear-server__create_issue(parentId: "uuid-100", ...)  → ENG-101
# 3. Create tasks with parentId:
mcp__linear-server__create_issue(parentId: "uuid-101", ...)  → ENG-102
```

**DO NOT use `relatedTo`** - that creates "related" not parent-child!

---

## The Workflow

When the user mentions work that should be tracked:

### 1. Analyze Request

Read the user's message and determine:
- What type of issue is this? (Don't ask - infer)
- What area of the codebase is involved?
- Is this single-task or multi-phase?

### 2. Investigate Codebase

Dispatch explore agent:

```
Task: @Explore
Find context for: "{summary of request}"

Look for:
- Files that would be affected
- How similar things are implemented
- Patterns to follow
- Dependencies
```

### 3. Build Issue

Using the appropriate template:
- Fill in user's description
- Add auto-gathered context
- Include relevant code snippets
- Add file paths with line numbers
- Set appropriate labels and priority

### 4. Confirm with User

Show the proposed issue:

```markdown
## Proposed Linear Issue

**Type:** {Bug/TODO/Question/Tech Debt/Feature}
**Title:** {title}

{Full issue body}

---

Create this issue? I can also adjust before creating.
```

### 5. Create in Linear

Use Linear MCP to create the issue:
- Create issue with full context
- For features: create hierarchy
- Return issue ID/URL

---

## Workflow Example

**User says:** "The login form breaks when I use special characters"

**Step 1 - Classify:** Signals "breaks" → Bug

**Step 2 - Investigate:**
```
Task: @Explore - Find: login form, input validation, special character handling
```
Returns: `src/components/LoginForm.tsx:45`, `src/utils/validation.ts:12`, pattern using `sanitizeInput()`

**Step 3 - Build:** Read `templates/bug.md`, fill with gathered context

**Step 4 - Confirm:** Show proposed issue to user

**Step 5 - Create:** Use Linear MCP to create issue

See individual template files for full output examples.

---

## Quick Reference

```
CLASSIFY     -> Infer type from context (never ask user)
INVESTIGATE  -> Use explore agent for codebase context
ENRICH       -> Add file paths, code snippets, patterns
CONFIRM      -> Show user before creating
CREATE       -> Use Linear MCP with full context

BUG          -> Something broken, needs fixing
TODO         -> Quick standalone task
QUESTION     -> Decision or discussion needed
TECH DEBT    -> Improvement for later
FEATURE      -> Multi-phase hierarchical work
```

## Red Flags - STOP

- Creating issue without investigating codebase first
- Asking user "is this a bug or a TODO?"
- Issue without file paths or code context
- Vague descriptions that lack specificity
- Missing verification commands

---

## Integration

**Uses:**
- **Explore agent** - Codebase investigation
- **Linear MCP** - Issue creation

**Pairs with:**
- **tdd** - Test-first for fixes
- **session** - Track Linear progress in sessions
- **verification** - Document verification results
