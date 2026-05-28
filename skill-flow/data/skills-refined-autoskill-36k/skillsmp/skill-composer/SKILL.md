---
name: skill-composer
description: "Create and improve Claude Code Skills following official best practices. Use when creating a skill, improving skill descriptions, fixing skill activation issues, or structuring skill directories."
---

# Skill Composer

Create well-structured, discoverable skills that Claude Code can activate automatically.

## Core Principles

Four official best practices determine if skills activate correctly:

### 1. Keep Skills Focused

One capability per skill.

**Focused** (discoverable):
- "PDF form filling"
- "Excel data analysis"
- "Git commit messages"

**Too broad** (won't activate predictably):
- "Document processing"
- "Data tools"

Claude can't discover vague capabilities. Focused skills have clear activation patterns.

### 2. Write Clear Descriptions

Description is Claude's discovery mechanism. Must include **what** it does and **when** to use it.

**Vague description** (Claude won't know when to use it):
```yaml
description: "Helps with documents"
```

**Clear description** (Claude knows exactly when to activate):
```yaml
description: "Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction."
```

**Include**:
- File types (`.xlsx`, `PDF files`, `package.json`)
- Action verbs (`extract`, `analyze`, `generate`)
- User terminology (words they actually say)

### 3. Test with Your Team

Real usage reveals what documentation misses.

**Test for**:
- Activates when expected?
- Activates when NOT expected? (false positives)
- Instructions clear enough to follow?
- Edge cases documented?

Gather feedback before considering skill complete.

### 4. Document Skill Versions

Track changes so team understands evolution:

```markdown
## Version History
- v2.0.0 (2025-10-01): Breaking changes to API
- v1.1.0 (2025-09-15): Added new features
- v1.0.0 (2025-09-01): Initial release
```

Skills change over time. Version history shows what changed and when.

## Creating a Skill

### Step 1: Choose Scope

**Project/Local Skills**: `.claude/skills/` (Recommended)
- Team-shared via git
- Project-specific workflows
- Available to all team members automatically
- Committed to repository

```bash
mkdir -p .claude/skills/skill-name
```

**Global Skills**: `/Users/Shared/data/claude/ccc-files/skills`
- Cross-project workflows
- System-wide capabilities
- Available in all projects
- Not project-specific

```bash
mkdir -p /Users/Shared/data/claude/ccc-files/skills/skill-name
```

### Step 2: Create SKILL.md

Every skill requires a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: "skill-name"
description: "What it does and when to use it"
---

# Skill Name

## Instructions

Clear, step-by-step guidance for Claude.

## Examples

Concrete examples of using this skill.

## Version History

- v1.0.0 (2025-11-03): Initial version
```

**Field requirements** (see REFERENCE.md for details):
- `name`: lowercase, letters/numbers/hyphens only, max 64 characters
- `description`: max 1024 characters, MUST include what AND when

### Step 3: Write Discovery-Optimized Description

The description determines if Claude activates your skill.

**Pattern**: `[What it does]. Use when [trigger conditions].`

**Example descriptions**:

```yaml
# Good - specific triggers
description: "Generate conventional commit messages following standard formats (feat, fix, refactor). Use when committing changes or when asked for commit message help."

# Good - includes file types and actions
description: "Analyze Excel spreadsheets, create pivot tables, generate charts. Use when working with Excel files, spreadsheets, or analyzing tabular data in .xlsx format."

# Bad - no triggers
description: "Helps with files"

# Bad - missing when-to-use
description: "Process PDF documents"
```

**Include**:
- Specific file extensions
- Action verbs users say
- Domain terminology
- "Use when..." clause

### Step 4: Write Instructions

Clear, explicit, step-by-step guidance.

**Example structure**:

```markdown
## Instructions

1. Run `git diff --staged` to see changes
2. Generate commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components
3. Use present tense
4. Explain what and why, not how
```

No ambiguity. No assumptions about what Claude knows.

### Step 5: Consider Tool Restrictions

Use `allowed-tools` to restrict capabilities when appropriate:

```yaml
---
name: "code-reviewer"
description: "Review code without modifying files"
allowed-tools: Read, Grep, Glob
---
```

**When to restrict**:
- Read-only analysis (code review, security audit)
- Data-only operations (search, research)
- Safety-critical workflows

See REFERENCE.md for available tools.

### Step 6: Add Supporting Files (Optional)

For complex skills, add REFERENCE.md for technical specs, EXAMPLES.md for code samples, scripts/ for utilities, or templates/ for file generation.

**CRITICAL**: All files MUST be inside the skill folder. Never reference external files - they break when moved or changed.

**Progressive disclosure**: Claude loads supporting files only when needed. See [REFERENCE.md](REFERENCE.md#directory-structure-patterns) for structure patterns.

### Step 7: Add Version History

Document the skill's evolution using semantic versioning:

```markdown
## Version History

- v1.0.0 (2025-11-03): Initial version
```

See [REFERENCE.md](REFERENCE.md#version-history-format) for semantic versioning guidelines.

### Step 8: Test Activation

Ask questions that should trigger the skill:

**Example test queries**:
- For commit-message skill: "Help me write a commit message"
- For code-reviewer skill: "Review this code for issues"
- For pdf-processor skill: "Extract text from this PDF"

Verify Claude activates the skill without explicit invocation.

## Skill Patterns

See [REFERENCE.md](REFERENCE.md) for detailed directory structure patterns and [Skill Examples](REFERENCE.md#skill-examples) for real-world pattern comparison and selection guide.

## Troubleshooting Checklist

Quick checks when skill doesn't activate:

- [ ] Description includes **what** it does and **when** to use it
- [ ] YAML frontmatter valid (opening/closing `---`, spaces not tabs)
- [ ] Name is lowercase, letters/numbers/hyphens only
- [ ] File at `.claude/skills/skill-name/SKILL.md` or global location
- [ ] Scripts have execute permissions if used
- [ ] Version history present

**Debug mode**: `claude --debug`

See [REFERENCE.md](REFERENCE.md#troubleshooting-reference) for detailed troubleshooting guide.

## Quality Criteria

Skills should be: **Discoverable** (clear description), **Focused** (single capability), **Specific** (file types/use cases), **Documented** (clear instructions), **Testable** (can verify activation), **Maintainable** (version history), **Secure** (tool restrictions when needed), **Shared** (team access via git).

See [REFERENCE.md](REFERENCE.md#quality-criteria-details) for detailed criteria.

## Version History

- v2.0.0 (2025-11-15): Renamed from write-skills to skill-composer, restructured to remove duplications with REFERENCE.md, updated skill locations (removed personal, added global), merged examples/INDEX.md into REFERENCE.md
- v1.0.0 (2025-11-03): Initial version based on official Claude Code documentation
