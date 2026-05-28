# Skill Structure Guide

## Directory Structure Standards

### Standard Skill Layout

Every skill follows this organization:

```
skill-name/
├── SKILL.md (required)
├── references/ (optional)
├── examples/ (optional)
├── scripts/ (optional)
└── assets/ (optional)
```

### Required: SKILL.md

**Location:** `skill-name/SKILL.md`
**Purpose:** Main skill file with metadata and instructions
**Format:** Markdown with YAML frontmatter

**Required frontmatter fields:**
- `name` - Skill name in Title Case
- `description` - Third-person description with specific triggers

**Optional frontmatter fields:**
- `version` - Semantic version (e.g., 0.1.0)

**Example:**
```yaml
---
name: PDF Editor
description: This skill should be used when the user asks to "rotate PDF",
"merge PDF files", "split PDF", or mentions PDF manipulation, editing, or
transformation.
version: 0.1.0
---
```

### Optional: references/

**Purpose:** Detailed documentation loaded as needed
**When to use:** Content >2,000 words, comprehensive guides, API docs
**Content types:**
- Detailed patterns and techniques
- API documentation
- Migration guides
- Troubleshooting
- Edge cases

**File naming:** Use kebab-case with descriptive names:
- `structure-guide.md`
- `trigger-patterns.md`
- `content-quality.md`

### Optional: examples/

**Purpose:** Complete, working code examples
**When to use:** Demonstrating patterns, templates, configurations
**Content types:**
- Complete scripts
- Configuration files
- Template code
- Real-world samples

**File naming:** Descriptive names with extensions:
- `basic-hook.md`
- `complete-agent.md`
- `validation-script.sh`

### Optional: scripts/

**Purpose:** Executable utilities for common tasks
**When to use:** Code repeatedly rewritten, deterministic reliability needed
**Content types:**
- Validation tools
- Testing helpers
- Parsing utilities
- Automation scripts

**Requirements:**
- Must be executable (proper permissions)
- Must be documented
- Should handle errors gracefully

**File naming:** Descriptive, action-oriented:
- `validate-skill.sh`
- `parse-settings.py`
- `test-hook.sh`

### Optional: assets/

**Purpose:** Files used in output, not loaded into context
**When to use:** Templates, images, boilerplate
**Content types:**
- Document templates (`.pptx`, `.docx`)
- Code templates (HTML, React)
- Images (`.png`, `.svg`)
- Fonts (`.ttf`)
- Sample data

## File Naming Conventions

### Directories

**Use kebab-case:**
```
✅ skill-name/
✅ pdf-editor/
✅ hook-development/

❌ skillName/
❌ pdf_editor/
❌ HookDevelopment/
```

### Files

**SKILL.md:** Always exactly `SKILL.md` (uppercase)

**References:** Descriptive kebab-case with `.md` extension:
```
✅ structure-guide.md
✅ trigger-patterns.md
✅ advanced-techniques.md

❌ StructureGuide.md
❌ trigger_patterns.md
```

**Examples:** Descriptive with appropriate extensions:
```
✅ basic-hook.md
✅ validation-script.sh
✅ agent-config.json

❌ example.md
❌ test.txt
```

**Scripts:** Action-oriented with executable extensions:
```
✅ validate-hook.sh
✅ parse-settings.py
✅ generate-report.js

❌ script.sh
❌ utility.py
```

## YAML Frontmatter Standards

### Required Fields

#### name

**Format:** Title Case, concise
**Purpose:** Identifies the skill
**Examples:**
```yaml
name: Hook Development
name: PDF Editor
name: BigQuery Integration
```

#### description

**Format:** Third person, specific triggers
**Purpose:** Determines when skill activates
**Structure:**
```yaml
description: This skill should be used when the user asks to "phrase 1",
"phrase 2", "phrase 3", or mentions concept1, concept2, or concept3.
```

**Good examples:**
```yaml
# Specific and concrete
description: This skill should be used when the user asks to "create a hook",
"add a PreToolUse hook", "validate tool use", or mentions hook events
(PreToolUse, PostToolUse, Stop).

# Covers variations
description: This skill should be used when the user asks to "create a skill",
"write a new skill", "add a skill to my plugin", or mentions skill development,
SKILL.md files, or trigger phrases.

# Domain-specific
description: This skill should be used when working with MCP servers,
mentions "add MCP integration", "configure stdio server", or discusses
Model Context Protocol, MCP tools, or server authentication.
```

**Bad examples:**
```yaml
# Too vague
description: Provides hook guidance.

# Second person
description: Use this skill when you want to work with hooks.

# No triggers
description: Load for skill development help.

# Missing context
description: PDF manipulation.
```

### Optional Fields

#### version

**Format:** Semantic versioning (MAJOR.MINOR.PATCH)
**Purpose:** Track skill evolution
**Example:**
```yaml
version: 0.1.0
```

**Versioning guidelines:**
- **0.x.x:** Initial development, API may change
- **1.0.0:** Stable, public API
- **Minor versions:** New features, backward compatible
- **Patch versions:** Bug fixes

## Markdown Body Standards

### Structure

Organize SKILL.md with clear sections:

```markdown
# Skill Name

## Overview
[Brief introduction]

## Core Concepts
[Key concepts and terminology]

## Essential Procedures
[Step-by-step workflows]

## Quick Reference
[Tables and lists]

## Additional Resources
[Links to references/]
```

### Length Guidelines

**SKILL.md target:** 1,500-2,000 words

**Breakdown:**
- Overview: 200-300 words
- Core concepts: 400-600 words
- Procedures: 600-800 words
- Quick reference: 200-300 words
- Resource links: 100-200 words

**Maximum:** 3,000 words (move detailed content to references/)

### Writing Style

**Use imperative form:**
```markdown
✅ Create the directory structure.
✅ Validate the YAML syntax.
✅ Configure the MCP server.

❌ You should create the directory.
❌ You need to validate the syntax.
❌ Configure the MCP server. (incomplete sentence)
```

**Be objective:**
```markdown
✅ To create a hook, define the event type in hooks.json.
✅ Validate frontmatter using sed to extract the YAML block.

❌ I recommend creating a hook by...
❌ You'll want to validate...
```

**Use markdown features:**
- Headers (##, ###) for hierarchy
- Bullet points for lists
- Code blocks for examples
- Tables for quick reference
- Bold for emphasis

### Content Organization

**Include in SKILL.md:**
- Purpose and overview
- Core concepts
- Essential procedures
- Most common use cases
- Links to references/

**Move to references/:**
- Detailed patterns (>500 words)
- Comprehensive examples
- API documentation
- Edge cases
- Troubleshooting

## Progressive Disclosure Implementation

### Level 1: Metadata (Always Loaded)

**Content:** Name + description
**Size:** ~100 words
**Purpose:** Skill discovery and triggering

**Example:**
```yaml
---
name: Skill Development
description: This skill should be used when the user asks to "create a skill",
"write SKILL.md", or mentions skill development, trigger phrases, or skill
best practices.
version: 0.1.0
---
```

### Level 2: SKILL.md Body (On Trigger)

**Content:** Core instructions
**Size:** 1,500-2,000 words
**Purpose:** Essential guidance

**Loads when:** Skill description matches user query

### Level 3: Bundled Resources (As Needed)

**Content:** Detailed documentation, examples, scripts
**Size:** Unlimited
**Purpose:** Comprehensive reference

**Loads when:** Claude determines need during task execution

**Examples:**
- `references/patterns.md` - When implementing complex patterns
- `examples/complete-agent.md` - When creating an agent
- `scripts/validate.sh` - When validation needed

## Auto-Discovery Mechanics

### How Skills Are Discovered

1. **Plugin loads:** Claude Code scans plugin directory
2. **Skills scan:** Finds all subdirectories in `skills/`
3. **SKILL.md check:** Identifies directories with SKILL.md
4. **Metadata load:** Reads name and description from frontmatter
5. **Trigger detection:** Monitors user queries for matching phrases

### Directory Location

**Plugin skills:** `plugin-name/skills/skill-name/`

**Example:**
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── skill-one/
    │   └── SKILL.md
    └── skill-two/
        ├── SKILL.md
        └── references/
```

### Trigger Matching

Claude matches user queries against skill descriptions:

**User query:** "How do I create a hook for validating writes?"

**Matching skills:**
1. Scans all skill descriptions
2. Finds: "create a hook" in hook-development description
3. Loads hook-development/SKILL.md
4. Executes with skill guidance

## Validation Checklist

Use this checklist to validate skill structure:

### Directory Structure
- [ ] Skill directory exists in `plugin-name/skills/`
- [ ] SKILL.md file exists
- [ ] Optional directories created as needed (references/, examples/, scripts/)

### SKILL.md Frontmatter
- [ ] YAML frontmatter present (--- markers)
- [ ] `name` field exists (Title Case)
- [ ] `description` field exists
- [ ] `description` uses third person ("This skill should be used when...")
- [ ] `description` includes specific trigger phrases
- [ ] `version` field present (optional but recommended)

### SKILL.md Body
- [ ] Markdown body present and substantial
- [ ] Uses imperative form (no "you should")
- [ ] Length 1,500-2,000 words (target)
- [ ] Length <3,000 words (maximum)
- [ ] Has clear section structure
- [ ] Includes links to supporting resources

### Supporting Files
- [ ] Referenced files in references/ exist
- [ ] Examples in examples/ are complete
- [ ] Scripts in scripts/ are executable
- [ ] All files follow naming conventions

### Progressive Disclosure
- [ ] Core content in SKILL.md
- [ ] Detailed docs in references/
- [ ] Working code in examples/
- [ ] Utilities in scripts/
- [ ] No duplication across files

## Common Structure Issues

### Issue 1: Missing SKILL.md

**Problem:** Directory exists but no SKILL.md

**Symptom:** Skill not discovered

**Fix:** Create SKILL.md with proper frontmatter

```bash
touch skills/my-skill/SKILL.md
```

### Issue 2: Invalid YAML Frontmatter

**Problem:** YAML syntax errors

**Symptom:** Skill fails to load

**Examples:**
```yaml
# Missing closing ---
---
name: My Skill
description: This skill...

# Wrong indentation
---
name: My Skill
  description: This skill...  # Too far indented

# Missing quotes
---
name: My Skill
description: This skill should be used when the user asks to "create a hook
# Unclosed string
```

**Fix:** Validate YAML syntax

```bash
# Extract YAML block
sed -n '/^---$/,/^---$/p' SKILL.md | yamllint
```

### Issue 3: Weak Trigger Description

**Problem:** Description doesn't trigger reliably

**Symptoms:**
- Skill doesn't activate when expected
- Claude doesn't recognize relevant queries

**Fix:** Add specific trigger phrases

**Before:**
```yaml
description: Provides skill guidance.
```

**After:**
```yaml
description: This skill should be used when the user asks to "create a skill",
"write SKILL.md", "improve skill quality", or mentions skill development,
trigger phrases, or skill structure.
```

### Issue 4: Bloated SKILL.md

**Problem:** Too much content in main file

**Symptoms:**
- Skill always loads excessive context
- Detailed docs always in memory
- Hard to maintain

**Fix:** Move content to references/

**Before:**
```
skill-name/
└── SKILL.md (8,000 words)
```

**After:**
```
skill-name/
├── SKILL.md (1,800 words - core essentials)
└── references/
    ├── patterns.md (2,500 words)
    └── advanced.md (3,700 words)
```

## Best Practice Examples

Study these skills as structure references:

### hook-development (plugin-dev)

```
hook-development/
├── SKILL.md (1,651 words)
├── references/
│   └── patterns.md
├── examples/
│   ├── pre-tool-use.md
│   ├── post-tool-use.md
│   └── stop.md
└── scripts/
    ├── validate-hook-schema.sh
    └── test-hook.sh
```

**Why excellent:**
- Lean SKILL.md
- 3 detailed examples
- 2 utility scripts
- Comprehensive references

### agent-development (plugin-dev)

```
agent-development/
├── SKILL.md (1,438 words)
├── references/
│   └── agent-prompt-guide.md
└── examples/
    └── complete-agent.md
```

**Why excellent:**
- Focused SKILL.md
- References include AI generation prompt
- Complete working example

## Quick Reference

### Minimal Skill

```
skill-name/
└── SKILL.md
```

Use for: Simple knowledge, straightforward guidance

### Standard Skill (Recommended)

```
skill-name/
├── SKILL.md
├── references/
│   └── detailed-guide.md
└── examples/
    └── working-example.md
```

Use for: Most skills with detailed content

### Complete Skill

```
skill-name/
├── SKILL.md
├── references/
│   ├── patterns.md
│   └── advanced.md
├── examples/
│   ├── example1.md
│   └── example2.md
└── scripts/
    └── validate.sh
```

Use for: Complex domains with utilities

Follow these structure standards to create skills that are discoverable, maintainable, and effective.
