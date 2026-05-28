# Code Investigator Skill Specification

## Overview

**Skill Name:** `code-investigator`

**Purpose:** Systematically investigate code to understand specifications and provide evidence-based reports with file/line references. All findings are saved to persistent memory for future reference.

**Target Users:** Developers who need to:
- Understand how existing code implements specifications
- Document behavior with evidence for code review or refactoring
- Build institutional knowledge about complex codebases
- Reduce time spent re-investigating the same code areas

## Goals

1. **Evidence-based specification confirmation**: Trace code to confirm actual behavior with precise file/line references
2. **Visual documentation**: Generate Mermaid diagrams for multi-file or complex flows
3. **Persistent memory**: Save investigation results in searchable format for future reuse
4. **Clarity on unknowns**: Clearly distinguish confirmed facts from uncertain/unverifiable items

## Non-Goals

- Speculation without code evidence (hypothetical behavior must be marked as such)
- Large-scale refactoring implementation (investigation only; implementation is a separate task)
- Real-time debugging (use debugger tools; this skill focuses on static code analysis)

## Trigger Conditions

### Explicit Triggers
User phrases like:
- "What does this code do?"
- "How is [feature] implemented?"
- "Where is the spec for [behavior]?"
- "Explain this behavior"
- "Show me the implementation"

### Implicit Triggers
- Requests containing: "investigate", "specification", "code reading", "behavior check", "where is this done"
- Bug investigation requiring current specification understanding
- Pre-refactoring analysis

## Input Requirements

To prevent scope drift, gather these details upfront:

1. **Target Scope**
   - Feature name / screen / CLI command / API endpoint / component

2. **Investigation Focus**
   - Specification (expected behavior)
   - Exception handling
   - Configuration values
   - Performance characteristics
   - Security aspects

3. **Output Detail Level**
   - Overview only
   - Detailed with evidence
   - Design document level

## Investigation Process

### Step 0: Plan (Brief)
State what to investigate and where to start (1-3 lines). Prevents scope drift.

### Step 1: Identify Entry Point
Locate the starting point: routing, CLI entry, UI event, main function, service initialization, etc.

### Step 2: Trace Call Chain (Shortest Path Only)
Follow function/class/module calls related to the specification. Identify:
- Data structures (DTO/Model/State) and transformation points
- Conditional logic, defaults, exception handling, retries, caching, persistence

### Step 3: Extract Confirmed Specifications
Document facts that can be determined from code:
- "When/If [condition] then [action]"
- Default values, timeout settings, retry counts, etc.

### Step 4: Handle Uncertainties
List runtime dependencies (env vars, config files, external APIs) that cannot be confirmed from code alone:
- Mark as **"Unconfirmed"**
- Suggest additional investigation methods

### Step 5: Generate Diagram (Conditional)
Create Mermaid diagram when:
- 3+ files are involved
- Async/event-driven/state transitions are present
- Dependency direction is unclear (DI, plugins, hooks)

## Output Format

All investigation reports follow this template:

```markdown
## TL;DR
[1-2 sentence conclusion]

## Confirmed Specifications
[Bulleted list, each with evidence]

- **Spec**: [When/If/Then format]
  - **Evidence**: [path/to/file.ts:L10-L42](path/to/file.ts#L10-L42) - [Why this code proves the spec]
  - **Notes**: [Optional: exceptions, config dependencies, related locations]

## Implementation Evidence
[Key implementation details by file]

### [path/to/file.ts](path/to/file.ts)
- Lines X-Y: [What this code does]
- Lines A-B: [What this code does]

## Flow Diagram (Optional)
[Mermaid diagram if applicable]

## Open Questions / Unknowns
[What could not be confirmed and why]
- [Unconfirmed item]: [What additional investigation is needed]
```

### Evidence Linking Rules
- Always link files with markdown: `[path/to/file.ts](path/to/file.ts#L10-L42)`
- Use line numbers when available: `#L10-L42`
- If line numbers unavailable, use: `#functionName` or just `(file.ts)`

## Memory Storage

All confirmed investigations are saved to: `.claude/skills/code-investigator/memories/`

### File Naming Convention
```
YYYY-MM-DD__topic__short-slug.md
```

Examples:
- `2026-01-08__player__loop-behavior.md`
- `2026-01-08__auth__session-timeout.md`

### Memory File Structure
```yaml
---
summary: "Brief description of investigation topic and key findings"
created: YYYY-MM-DD
updated: YYYY-MM-DD  # optional
status: confirmed | in-progress | blocked  # optional
tags: [feature-area, component]  # optional
related: [path/to/file.ts]  # optional
---
```

**Language**: All memory files MUST be written in **English**.

### Search Workflow
```bash
# View all summaries
rg "^summary:" .claude/skills/code-investigator/memories/ --no-ignore --hidden

# Search by keyword
rg "^summary:.*auth" .claude/skills/code-investigator/memories/ --no-ignore --hidden -i

# Search by tag
rg "^tags:.*player" .claude/skills/code-investigator/memories/ --no-ignore --hidden -i
```

## Quality Standards

### Prohibited
- **No speculation as fact**: Use "likely" / "probably" only in "Open Questions", never in "Confirmed Specifications"
- **No baseless evidence**: Every specification claim must have file:line reference

### Required
- **Primary vs supplementary evidence**: When multiple locations support one spec, separate "primary" and "supplementary" evidence
- **Config/env dependencies**: Always note when behavior depends on ENV vars, config files, or runtime values

## Diagram Types

| Scenario | Diagram Type | Reason |
|----------|--------------|--------|
| API request → response flow | `sequenceDiagram` | Shows temporal order |
| Module dependencies | `flowchart LR` | Shows static relationships |
| State machine | `stateDiagram-v2` | Shows state transitions |

**Diagram policy:**
- Show **shortest path only** (no comprehensive views)
- Use `File::Symbol` format for node names

## File Structure

```
.claude/skills/code-investigator/
├── SKILL.md                                    # Main skill instructions
├── memories/                                   # Investigation results storage
│   ├── README.md                              # Search and usage guide
│   └── YYYY-MM-DD__topic__slug.md             # Individual investigations
└── references/                                 # Detailed guidance
    ├── report-templates.md                    # Report format examples
    └── diagram-patterns.md                    # Mermaid diagram patterns
```

## Success Metrics

A successful investigation includes:

1. ✅ Clear TL;DR summarizing findings
2. ✅ Every specification backed by file:line evidence
3. ✅ Evidence descriptions explain WHY code proves the spec
4. ✅ Diagram provided when 3+ files or complex flow
5. ✅ Open questions listed when information cannot be confirmed
6. ✅ Memory file saved with proper frontmatter
7. ✅ All documentation in English

## References

- [SKILL.md](SKILL.md) - Complete skill instructions
- [references/report-templates.md](references/report-templates.md) - Detailed report examples
- [references/diagram-patterns.md](references/diagram-patterns.md) - Mermaid diagram guidance
- [memories/README.md](memories/README.md) - Memory search and management

## Version

- **Created**: 2026-01-08
- **Last Updated**: 2026-01-08
- **Version**: 1.0.0
