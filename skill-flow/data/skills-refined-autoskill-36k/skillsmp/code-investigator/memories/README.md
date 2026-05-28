# Code Investigation Memories

This directory stores code investigation results for future reference.

## Purpose

- Save confirmed specifications with evidence (file/line references)
- Enable quick retrieval of past investigation findings
- Avoid re-investigating the same code areas
- Build institutional knowledge about codebase specifications

## File Organization

Files are organized by date and topic using this naming convention:

```
YYYY-MM-DD__topic__short-slug.md
```

Examples:
- `2026-01-08__player__loop-behavior.md`
- `2026-01-08__auth__session-timeout.md`
- `2026-01-08__sync__conflict-resolution.md`

### Optional Categorization

For projects with many investigations, organize by feature area:

```
memories/
├── auth/
│   ├── 2026-01-08__session-timeout.md
│   └── 2026-01-09__oauth-flow.md
├── player/
│   ├── 2026-01-08__loop-behavior.md
│   └── 2026-01-10__state-management.md
└── sync/
    └── 2026-01-08__conflict-resolution.md
```

## Memory File Format

Every memory file MUST include YAML frontmatter:

```yaml
---
summary: "Brief description of investigation topic and key findings"
created: YYYY-MM-DD
updated: YYYY-MM-DD  # optional, when investigation is updated
status: confirmed | in-progress | blocked  # optional
tags: [feature-area, component-name]  # optional
related: [path/to/file.ts, path/to/other.ts]  # optional
---
```

### Status Values
- `confirmed`: Specifications fully verified from code
- `in-progress`: Partial investigation, more work needed
- `blocked`: Investigation blocked by missing information/access

## Searching Memories

Memory files are gitignored, so use `--no-ignore --hidden` flags with ripgrep:

```bash
# List all investigations
ls .claude/skills/code-investigator/memories/

# View all summaries
rg "^summary:" .claude/skills/code-investigator/memories/ --no-ignore --hidden

# Search summaries by keyword
rg "^summary:.*authentication" .claude/skills/code-investigator/memories/ --no-ignore --hidden -i

# Search by tag
rg "^tags:.*player" .claude/skills/code-investigator/memories/ --no-ignore --hidden -i

# Full-text search
rg "handleSave" .claude/skills/code-investigator/memories/ --no-ignore --hidden -i

# Find by date
ls .claude/skills/code-investigator/memories/ | grep "^2026-01"
```

## Memory Content Template

See [SKILL.md](../SKILL.md#memory-file-format) for the complete template.

Key sections:
1. **Question**: Original user question or investigation goal
2. **Confirmed Specifications**: Evidence-backed findings
3. **Implementation Evidence**: File-by-file breakdown
4. **Flow Diagram**: Mermaid diagram if applicable
5. **Open Questions**: Unconfirmed items and next steps

## Maintenance

### When to Update
- When revisiting previous investigation and finding new details
- When implementation changes and past findings become outdated
- When open questions get answered

### When to Delete
- When code area no longer exists (refactored away)
- When findings are completely superseded by new investigation
- When project area is deprecated

### Consolidation
If multiple small investigations cover related areas, consider consolidating into a single comprehensive memory file.

## Language

All memory files MUST be written in **English** for consistency with project documentation standards.

## Git Ignore

Memory files are gitignored to keep the repository clean. To ignore:

```gitignore
# In .gitignore
.claude/skills/code-investigator/memories/*.md
```

Keep this README tracked in git for documentation purposes.
