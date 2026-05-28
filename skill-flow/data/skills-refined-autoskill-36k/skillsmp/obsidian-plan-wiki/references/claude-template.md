# CLAUDE.md and AGENTS.md Templates

## CLAUDE.md (Symlink)

CLAUDE.md should be a **symlink** to AGENTS.md, not a file with content:

```bash
# From within the wiki directory
ln -s AGENTS.md CLAUDE.md
```

**Why symlink?** The `@filename` convention in file contents causes some tools to ignore the file entirely. A symlink ensures CLAUDE.md is always read as the actual AGENTS.md content.

## AGENTS.md (Actual Instructions)

Copy and customize this template for each plan wiki:

```markdown
# [Plan Name] - Agent Instructions

## Plan Structure

This is an Obsidian-compatible modular plan.

\`\`\`
plan-name/
├── README.md           # Index - start here
├── CLAUDE.md           # Symlink → AGENTS.md
├── AGENTS.md           # This file - rules for agents
├── changelog.md        # Amendment history
├── deferred.md         # Preserved deferred work
├── phases/             # High-level phase overviews
├── tasks/              # Individual task specifications
├── reference/          # Supporting documentation
└── research/           # Oracle/Delphi research outputs
\`\`\`

## Rules

### 1. Progressive Disclosure

**DO:** Read only the files you need for the current task.
**DON'T:** Load the entire plan into context.

\`\`\`
User asks about X → Read tasks/X.md
User asks about Phase N → Read phases/0N-name.md
User asks for overview → Read README.md only
\`\`\`

### 2. Open Task Tracking

Tasks are tracked with Obsidian comment checkboxes using emoji prefixes and block references:

\`\`\`markdown
%% [ ] 🙋‍♂️: human task or instruction %% ^q-scope-descriptor

%% [ ] 🤖: agent question needing human input %% ^q-scope-question

%% [x] 🤖: resolved → answer here %% ^q-scope-resolved
\`\`\`

**CRITICAL: Blank lines required.** Each question MUST be separated by a blank line. Obsidian treats consecutive lines as a single block—only the LAST block ID works.

**WHO ANSWERS WHAT:**
| Emoji | Who wrote it | Who should answer/action |
|-------|--------------|--------------------------|
| 🙋‍♂️ | Human | **Agent** (this is work for you!) |
| 🤖 | Agent | **Human** (skip this, you asked it) |

**Conversation threading:** Questions can have inline replies. The **LAST emoji** determines whose turn:
\`\`\`
%% [ ] 🤖: Should we cache? 🙋‍♂️ yes 🤖: what limit? %% ^q-cache
\`\`\`
Last emoji is 🤖 → Human's turn. When \`[x]\` → Done.

- \`^q-{scope}-{descriptor}\` = block ID for Obsidian navigation

**Finding open tasks:**
\`\`\`bash
grep -rn '%% \[ \]' path/to/plan/      # all open
grep -rn '🤖:' path/to/plan/           # agent questions
grep -rn '🙋‍♂️:' path/to/plan/          # human tasks
grep -rn '%% \[ \].*%%$' path/to/plan/ # missing block IDs
\`\`\`

**When completing a task:**
1. Mark \`[x]\` in the comment (or convert \`🤖:\` to \`🙋‍♂️:\` if now actionable)
2. Add answer after \`→\`
3. Add entry to changelog.md

**Agent responsibility:** When encountering questions missing block IDs, agents MUST add them immediately. Generate an ID based on the file's scope and the question topic.

### 3. Research Workflow

When a \`%% [ ] 🙋‍♂️:\` or \`%% [ ] 🤖:\` comment needs research:

1. **Simple question:** Use single oracle
2. **Complex/uncertain:** Use Delphi (3 parallel oracles + synthesis)

**Research outputs go to:** \`research/\` directory

**Link format after research:**
\`\`\`markdown
%% [x] question → Delphi complete: [[research/topic-delphi]] %%
> **Research:** See [[research/topic]] for details
\`\`\`

### 4. Changelog Protocol

**Every change to the plan must be logged in changelog.md.**

Format:
\`\`\`markdown
## YYYY-MM-DD

### Added
- [[path/to/file]] - Description

### Changed
- [[path/to/file]] - What changed and why

### Research
- [[research/topic]] - Summary of findings
\`\`\`

### 5. Version Preservation

Before major amendments:
1. Copy current file to \`{filename}.v{n}.md\`
2. Continue editing main file
3. Reference old version in changelog

### 6. Wiki-Link Format

Use Obsidian wiki-links for all internal references:

\`\`\`markdown
[[tasks/1.1-project-structure]]           # Same directory
[[../research/topic]]                     # Relative path
[[tasks/4.1-name|Display Name]]           # With display text
\`\`\`

### 7. Key Decisions Made

| Decision | Research | Recommendation |
|----------|----------|----------------|
| [Topic] | [[research/topic]] | **Choice** - reason |

### 8. Deferred Work

Deferred items are preserved in [[deferred]] for future implementation.
Do not delete deferred content - it may be needed later.

### 9. Task File Structure

Each task file should have:

\`\`\`markdown
# Task X.Y: Title

**Phase:** N - Phase Name
**Commit:** \`type(scope): description\`

%% [ ] 🤖: any open questions for human %%

> **Research:** See [[../research/topic]] if applicable

## Overview (if needed)
## Files
## Steps
## Success Criteria
\`\`\`

### 10. When Adding New Tasks

1. Create file in \`tasks/\` with format \`{phase}.{task}-{slug}.md\`
2. Add to phase file's task table
3. Add to README.md task index
4. Add changelog entry
```
