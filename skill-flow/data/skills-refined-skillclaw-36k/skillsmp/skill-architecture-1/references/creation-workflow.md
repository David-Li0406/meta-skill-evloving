# Creation Workflow

Step-by-step process for creating effective skills, merging marketplace best practices with security-focused approach.

## Overview

Two complementary workflows:
1. **Marketplace 6-Step Process** (comprehensive, uses scripts)
2. **Manual Creation** (lightweight, no scripts)

Choose based on complexity and tooling preferences.

______________________________________________________________________

## Marketplace 6-Step Process (Recommended)

### Step 1: Understanding with Concrete Examples

Gather real examples of how the skill will be used.

**Questions to ask**:
- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"
- "What would trigger this skill?"
- "What file types or domains are involved?"

**Example conversation**:
```
User: "I need help rotating PDFs"
You: "What else besides rotation? Merging? Splitting?"
User: "Yes, and extracting text"
You: "What would you say to trigger this? 'Rotate this PDF'?"
```

**Output**: Clear list of use cases and trigger phrases

### Step 2: Planning Reusable Contents

Analyze each use case to identify resources needed.

**Decision matrix**:

| Task Type | Resource Type | Example |
|-----------|---------------|---------|
| Repeated code | scripts/ | PDF rotation algorithm |
| Domain knowledge | references/ | Database schemas, API docs |
| Templates/assets | assets/ | HTML boilerplate, config files |
| Simple workflows | SKILL.md only | Basic instructions |

**Example analysis**:
- "Rotating PDFs" → Code repeated each time → `scripts/rotate_pdf.py`
- "Database queries" → Schema not memorized → `references/schema.md`
- "Frontend apps" → Same boilerplate → `assets/template/`

### Step 3: Initialize with Script

Use marketplace script for proper structure:

```bash
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/init_skill.py pdf-editor --path ~/.claude/skills/
```

**Creates**:
```
~/.claude/skills/pdf-editor/
├── SKILL.md (template with TODOs)
├── scripts/
│   └── example_script.py (delete if not needed)
├── references/
│   └── example_reference.md (delete if not needed)
└── assets/
    └── example_asset.txt (delete if not needed)
```

**Delete unused directories** - Most skills don't need all three.

### Step 4: Edit the Skill

**A. Start with Resources**

Implement planned resources from Step 2:
- Write scripts in `scripts/`
- Document schemas/APIs in `references/`
- Add templates to `assets/`

May require user input (brand assets, credentials, etc.)

**B. Update SKILL.md**

Answer three questions:
1. **What is the purpose?** (2-3 sentences)
2. **When should it be used?** (Trigger keywords!)
3. **How to use bundled resources?** (Commands, examples)

**Writing style**: Imperative form (verb-first)
- ✅ "To rotate a PDF, run `scripts/rotate_pdf.py <file> <degrees>`"
- ❌ "You can rotate PDFs by running..."

**C. Update Description**

Critical for skill discovery:

```yaml
---
description: Extract text and tables from PDFs, rotate pages, merge documents. Use when working with PDF files or when user mentions forms, contracts, document processing.
---
```

**Include**:
- WHAT it does (specific capabilities)
- WHEN to use (triggers: file types, keywords, domains)

### Step 5: Package and Validate

Run packaging script (validates automatically):

```bash
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/package_skill.py ~/.claude/skills/pdf-editor/
```

**Validates**:
- [ ] YAML frontmatter format
- [ ] Required fields present
- [ ] Naming conventions
- [ ] Description quality
- [ ] File organization

**Output**: `pdf-editor.zip` (if valid)

### Step 6: Iterate

1. **Test**: Use skill on real tasks
2. **Observe**: Notice struggles or inefficiencies
3. **Identify**: What needs updating?
4. **Implement**: Fix SKILL.md or resources
5. **Repeat**: Test again

**Common iterations**:
- Add missing trigger keywords to description
- Extract large SKILL.md sections to references/
- Add scripts for repeatedly rewritten code
- Improve examples with real use cases

______________________________________________________________________

## Manual Creation (Lightweight)

For simple skills without scripts/assets:

### Step 1: Define Purpose and Triggers

Answer:
- What specific problem does this solve?
- What keywords would users naturally mention?
- What file types or domains?

### Step 2: Create Structure

```bash
mkdir -p ~/.claude/skills/your-skill-name
touch ~/.claude/skills/your-skill-name/SKILL.md
```

### Step 3: Write YAML Frontmatter

```yaml
---
name: your-skill-name
description: What this does and when to use it. Include trigger keywords!
allowed-tools: Read, Grep, Bash # Optional, for security
---
```

### Step 4: Write Instructions

- Use imperative form
- Be specific and actionable
- Include examples

Example:
```markdown
## Instructions

1. Check file exists: `ls <file>`
2. Process with: `grep -i "pattern" <file>`
3. Output results
```

### Step 5: Test Activation

1. Start new conversation (or `/clear`)
2. Ask question using trigger keywords
3. Verify Claude loads skill (output mentions skill name)
4. Refine description if not activating

### Step 6: Security Audit

- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] `allowed-tools` restricts dangerous operations
- [ ] Tested for prompt injection
- [ ] No unsafe file operations

See [Security Practices](/Users/terryli/.claude/skills/skill-architecture/references/security-practices.md)

______________________________________________________________________

## Common Creation Patterns

See [Workflow Patterns](/Users/terryli/.claude/skills/skill-architecture/references/workflow-patterns.md) for practical examples and workflow comparison.

______________________________________________________________________

## User Conventions (Terry's Standards)

When creating skills, follow conventions from [`~/.claude/CLAUDE.md`](/Users/terryli/.claude/CLAUDE.md):

### Absolute Paths

Always use absolute paths (iTerm2 Cmd+click compatible):

```markdown
See [Schema](/Users/terryli/.claude/skills/api-client/references/schema.md)  # Not: See references/schema.md
```

### Python Scripts

Use PEP 723 inline dependencies:

```python
# /// script
# dependencies = ["pyyaml>=6.0"]
# ///
import yaml
```
Run with: `uv run scripts/process.py`

### Unix-Only

Specify platform scope:

```markdown
> ⚠️ **Platform**: macOS, Linux only (no Windows support)
```

### Machine-Readable Planning

For complex workflows, reference OpenAPI specs:

```markdown
See specification: [`/Users/terryli/.claude/specifications/workflow.yaml`](/Users/terryli/.claude/specifications/workflow.yaml)
```

______________________________________________________________________

## Troubleshooting Creation

### "Skill not activating"

**Cause**: Description doesn't match user query

**Fix**: Add more trigger keywords
```yaml
# Before
description: PDF manipulation tool

# After
description: Extract text and tables from PDFs, rotate pages, merge documents. Use when working with PDF files or when user mentions forms, contracts, document processing.
```

### "SKILL.md too long"

**Cause**: Too much detail in main file

**Fix**: Use progressive disclosure
- Move details to `references/`
- Keep only essential info in SKILL.md
- Add navigation links

### "Skill loaded but fails"

**Cause**: Instructions unclear or incomplete

**Fix**:
- Add specific examples
- Include error handling
- Test instructions manually first

### "Validation fails"

**Cause**: Structural or format issues

**Fix**: Run validation script for details
```bash
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/package_skill.py <skill-path>
```

See error messages for specific issues.
