---
name: audit-project-instructions
description: Analyze CLAUDE.md and AGENTS.md files against best practices and suggest improvements
triggers:
  - audit project instructions
  - review claude md
  - check agents md
  - audit my instruction files
  - review project instructions
---

<required_reading>
**Read before starting:**

1. references/project-instructions.md - Best practices for instruction files
</required_reading>

<objective>
Analyze the target repository's CLAUDE.md and AGENTS.md files against best practices from `references/project-instructions.md`, then present actionable suggestions without making automatic changes.
</objective>

<process>

## Step 1: Read Target Files

Read the target repository's instruction files (from repo root):

- `CLAUDE.md` (project-level instructions)
- `AGENTS.md` (mechanical rules)

If either file is missing, note this as a finding.

## Step 2: Check for Missing Files

**If CLAUDE.md is missing:**

> "**Suggestion**: Create a CLAUDE.md file to provide project context for AI assistants.
> See `skills/layton/examples/CLAUDE.md` for a template to adapt."

**If AGENTS.md is missing:**

> "**Suggestion**: Create an AGENTS.md file for quick command references and session protocols.
> See `skills/layton/examples/AGENTS.md` for a concise example."

## Step 3: Analyze Verbosity

For CLAUDE.md, check line count and content density:

- **Warning threshold**: Over 200 lines
- **Critical threshold**: Over 400 lines

**If verbose:**

> "**Consider**: Your CLAUDE.md is {N} lines. Files over 200 lines can be hard to scan.
> Move detailed code examples to separate reference docs and keep CLAUDE.md navigational."

## Step 4: Analyze Duplication

Compare CLAUDE.md and AGENTS.md for overlapping content:

- Duplicate command references
- Repeated build/test instructions
- Same rules stated twice

**If duplication found:**

> "**Consider**: The following content appears in both files:
>
> - {duplicated content summary}
>
> **Suggestion**: Keep commands in AGENTS.md only. CLAUDE.md can say 'See AGENTS.md for command reference.'"

## Step 5: Check for Missing Sections

**CLAUDE.md should have:**

- Mandatory/Important section at top
- Project description or overview
- Primary entry point
- Folder structure or key files

**AGENTS.md should have:**

- Quick reference commands
- Session completion protocol
- Critical rules

For each missing section:

> "**Suggestion**: Add a {section name} section to {file}.
> This helps agents {reason for section}."

## Step 6: Present Findings

Summarize findings in a structured format:

```markdown
## Audit Results

**Files analyzed:**
- CLAUDE.md: {exists/missing} ({N} lines)
- AGENTS.md: {exists/missing} ({N} lines)

**Findings:**

1. {Finding with severity: suggestion/consider}
2. {Finding with severity: suggestion/consider}
...

**What would you like to do?**
- Apply specific suggestions
- Get more detail on a finding
- See examples from the reference doc
```

## Step 7: User Decides Next Steps

Wait for user input. Do NOT auto-apply changes.

If user wants to apply a suggestion:

- Show the proposed edit
- Ask for confirmation before making changes

</process>

<context_adaptation>

- **If CLAUDE.md is well-structured**: Focus audit on AGENTS.md or congratulate and skip
- **If user is in a hurry**: Give top 3 suggestions only
- **If this is a new project**: Offer to help create files from examples
</context_adaptation>

<success_criteria>

- Both files (if they exist) were analyzed
- Findings presented with rationale (not just "fix this")
- No automatic modifications made
- User guided on next steps
</success_criteria>
