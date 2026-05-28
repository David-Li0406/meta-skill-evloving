<overview>
Reference guide for structuring CLAUDE.md and AGENTS.md files in knowledge repositories using Layton.

Project instruction files help AI assistants work effectively in your repository. The recommended pattern is simple:

- **CLAUDE.md**: Contains only `@AGENTS.md` to load the agent instructions
- **AGENTS.md**: Contains all instructions (context, commands, protocols)
</overview>

<why_this_pattern>

1. **Single source of truth** - All instructions in one file
2. **No duplication** - CLAUDE.md just includes AGENTS.md
3. **Easy maintenance** - Update one file, not two
</why_this_pattern>

<claude_md_structure>
CLAUDE.md should be minimal - just include the agent instructions:

```markdown
# CLAUDE.md

@AGENTS.md
```

That's it. The `@AGENTS.md` directive tells Claude Code to load the agent instructions automatically.
</claude_md_structure>

<agents_md_structure>
AGENTS.md contains everything the AI assistant needs to know.

**Required Sections:**

| Section | Purpose |
| --- | --- |
| Session Start Protocol | What to do first (e.g., run `/layton`) |
| Primary Entry Point | How to get oriented (Layton) |
| Issue Tracking | Commands for Beads (`bd ready`, etc.) |
| Session Completion | "Landing the Plane" protocol |
| Critical Rules | Hard constraints that must be followed |

**Optional Sections (Add If Relevant):**

| Section | When to Add |
| --- | --- |
| What This Repository Is | If it's not obvious from context |
| Folder Structure | If there's a specific organization (e.g., PARA) |
| Key Files | If there are important files to know about |
| Language Preferences | If responses should be in a specific language |

</agents_md_structure>

<example_structure>

```markdown
# Agent Instructions

## ⚠️ MANDATORY: Session Start Protocol
1. Run `/layton` first

## Primary Entry Point: Layton
The `/layton` skill provides checks, skills, and workflows.

## Issue Tracking with Beads
```bash
bd ready              # Find available work
bd close <id>         # Complete work
```

## Session Completion (Landing the Plane)

1. File issues for remaining work
2. Update issue status
3. PUSH TO REMOTE: `git pull --rebase && bd sync && git push`
4. Hand off context

## Critical Rules

- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing

```text
</example_structure>

<anti_patterns>
Common anti-patterns to avoid:

**Duplication Between Files:**
- ❌ **Problem**: Content in both CLAUDE.md and AGENTS.md
- ✓ **Solution**: Put everything in AGENTS.md, CLAUDE.md just has `@AGENTS.md`

**Assuming Unknown Structure:**
- ❌ **Problem**: Prescribing folder structures or key files you don't know about
- ✓ **Solution**: Only document what you actually know; omit sections that don't apply

**Missing Session Protocol:**
- ❌ **Problem**: No guidance on how to start or end sessions
- ✓ **Solution**: Always include Session Start and Session Completion sections

**Verbose Explanations:**
- ❌ **Problem**: Long paragraphs explaining concepts
- ✓ **Solution**: Terse, actionable instructions. Commands, not essays.
</anti_patterns>

<file_locations>
```text
repository/
├── CLAUDE.md           # Just contains @AGENTS.md
├── AGENTS.md           # All agent instructions
└── .layton/
    ├── config.json     # Layton configuration
    ├── skills/         # Data source integrations
    └── workflows/      # Workflow definitions

```

</file_locations>

<examples>
See the `examples/` directory for:

- `CLAUDE.md` - Minimal file with just `@AGENTS.md`
- `AGENTS.md` - Complete agent instructions (~50 lines)
</examples>
