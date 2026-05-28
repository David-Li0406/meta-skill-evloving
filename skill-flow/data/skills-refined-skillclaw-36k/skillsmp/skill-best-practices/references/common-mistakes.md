# Common Skill Mistakes and How to Fix Them

## Overview

This guide covers the most common mistakes made when creating Claude Code skills and provides clear solutions for each issue.

## Critical Mistakes (Must Fix)

### Mistake 1: Missing or Invalid Frontmatter

**Problem:**
- No YAML frontmatter
- Missing `---` delimiters
- Missing required fields
- Invalid YAML syntax

**Examples:**

❌ **Missing frontmatter:**
```markdown
# My Skill

Content here...
```

❌ **Missing closing delimiter:**
```markdown
---
name: My Skill
description: This skill...

[content continues]
```

❌ **Missing required field:**
```yaml
---
name: My Skill
version: 0.1.0
---
```

**Fix:**

✅ **Valid frontmatter:**
```yaml
---
name: My Skill
description: This skill should be used when the user asks to "task 1",
"task 2", or mentions concept1 or concept2.
version: 0.1.0
---
```

**Validation:**
```bash
# Extract and validate YAML
sed -n '/^---$/,/^---$/p' SKILL.md | yamllint
```

---

### Mistake 2: Weak or Missing Trigger Phrases

**Problem:**
- Vague descriptions
- No specific user phrases
- Missing third person
- Incomplete trigger coverage

**Examples:**

❌ **Too vague:**
```yaml
description: Provides skill guidance.
```

❌ **Second person:**
```yaml
description: Use this skill when creating skills.
```

❌ **No specific phrases:**
```yaml
description: This skill helps with skill development.
```

**Fix:**

✅ **Strong triggers:**
```yaml
description: This skill should be used when the user asks to "create a skill",
"write a new skill", "add a skill to my plugin", "how do I create SKILL.md",
"what are skill best practices", or mentions skill development, trigger phrases,
progressive disclosure, or skill structure.
```

**Improvement Pattern:**
1. Start with "This skill should be used when..."
2. Add 3-7 specific action phrases in quotes
3. Include question formats ("how do I", "what are")
4. Mention domain concepts
5. List component names if applicable

---

### Mistake 3: Wrong File or Directory Name

**Problem:**
- SKILL.md named incorrectly
- Skill directory not using kebab-case
- Missing SKILL.md capitalization

**Examples:**

❌ **Wrong filename:**
```
skill-name/
└── skill.md          # Wrong case
└── README.md         # Wrong name
```

❌ **Wrong directory name:**
```
skillName/            # CamelCase
skill_name/           # Snake_case
SkillName/            # PascalCase
```

**Fix:**

✅ **Correct structure:**
```
skill-name/           # Kebab-case
└── SKILL.md          # Exactly SKILL.md
```

**Validation:**
```bash
# Check filename
ls -la skills/your-skill/SKILL.md

# Should show: SKILL.md (uppercase)
```

---

## Major Mistakes (Should Fix)

### Mistake 4: Second Person Writing Style

**Problem:**
Using "you should", "you need to", "you can" throughout SKILL.md

**Examples:**

❌ **Second person:**
```markdown
## Creating a Skill

You should start by creating the directory structure. You need to add
SKILL.md with proper frontmatter. You can include references for detailed
content.
```

**Fix:**

✅ **Imperative form:**
```markdown
## Creating a Skill

Start by creating the directory structure. Add SKILL.md with proper
frontmatter. Include references/ for detailed content.
```

**Automated Fix:**
```bash
# Replace common second-person patterns
sed -i 's/You should //g' SKILL.md
sed -i 's/You need to //g' SKILL.md
sed -i 's/You can //g' SKILL.md
sed -i 's/You might //g' SKILL.md
```

---

### Mistake 5: Bloated SKILL.md

**Problem:**
SKILL.md exceeds 2,000-3,000 words
All content in one file
Detailed sections that should be in references/

**Examples:**

❌ **Too large:**
```
skill-name/
└── SKILL.md (8,000 words - everything)
```

**Symptoms:**
- File >100KB
- Multiple sections >500 words each
- Comprehensive reference material included
- Always loads excessive context

**Fix:**

✅ **Progressive disclosure:**
```
skill-name/
├── SKILL.md (1,800 words - core essentials)
└── references/
    ├── detailed-patterns.md (2,500 words)
    └── advanced-techniques.md (3,000 words)
```

**Migration strategy:**
1. Identify sections >500 words
2. Move detailed content to references/
3. Keep core overview in SKILL.md
4. Add cross-references

**Example migration:**

Before (SKILL.md):
```markdown
## Hook Patterns

[2,000 words of detailed hook patterns...]
```

After:
- SKILL.md:
  ```markdown
  ## Hook Patterns

  For comprehensive hook patterns and examples, see
  **`references/hook-patterns.md`**.

  Key pattern types:
  - PreToolUse validation
  - PostToolUse notifications
  - Stop event handlers
  ```

- references/hook-patterns.md:
  ```markdown
  # Hook Patterns

  [Complete 2,000-word guide...]
  ```

---

### Mistake 6: Missing Resource References

**Problem:**
SKILL.md doesn't mention supporting files
References/ exist but aren't linked
Examples not referenced in main content

**Examples:**

❌ **Unreferenced resources:**
```
skill-name/
├── SKILL.md (no mentions of references/)
└── references/
    └── detailed-guide.md (never referenced)
```

**Fix:**

✅ **Clear references:**
```markdown
## Additional Resources

### Reference Files

For detailed patterns and techniques:
- **`references/detailed-guide.md`** - Comprehensive patterns
- **`references/advanced.md`** - Advanced use cases

### Examples

Working examples in `examples/`:
- **`example1.md`** - Basic example
- **`example2.md`** - Advanced example
```

**Best practice:** Always reference supporting resources in a dedicated "Additional Resources" section at the end of SKILL.md.

---

## Minor Mistakes (Nice to Fix)

### Mistake 7: Inconsistent Section Structure

**Problem:**
Inconsistent heading levels
Unclear organization
Missing sections

**Examples:**

❌ **Inconsistent:**
```markdown
# Overview

## Creating Skills

### Step 1

#### Details

# Another Top Level Section  # Inconsistent
```

**Fix:**

✅ **Consistent structure:**
```markdown
# Skill Name

## Overview

## Core Concepts

## Essential Procedures

## Quick Reference

## Additional Resources
```

---

### Mistake 8: Missing Examples

**Problem:**
Abstract concepts without concrete examples
Procedures without sample code
Patterns without demonstrations

**Examples:**

❌ **No examples:**
```markdown
## Creating Hooks

Define hooks in hooks.json with the appropriate event type and matcher.
```

**Fix:**

✅ **With examples:**
```markdown
## Creating Hooks

Define hooks in `hooks/hooks.json` with the event type and matcher:

```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "bash /Users/wxj/.claude/plugins/cache/claude-plugins-official/plugin-dev/e30768372b41/hooks/scripts/validate.sh"
    }]
  }]
}
```

This validates all Write and Edit tool uses.
```

---

### Mistake 9: Poor Formatting

**Problem:**
Missing code block markers
Inconsistent list formatting
Unclear emphasis

**Examples:**

❌ **Poor formatting:**
```markdown
Use the create command to make a new skill. The syntax is:
name: My Skill
description: This skill...
```

**Fix:**

✅ **Proper formatting:**
```markdown
Use the `create` command to make a new skill. The syntax is:

```yaml
---
name: My Skill
description: This skill should be used when...
---
```
```

---

### Mistake 10: Duplicate Content

**Problem:**
Same information in SKILL.md and references/
Content repeated across sections
Redundant explanations

**Examples:**

❌ **Duplication:**
```
SKILL.md:
## Hook Patterns
[Detailed explanation of patterns]

references/patterns.md:
## Hook Patterns
[Same detailed explanation]
```

**Fix:**

✅ **Progressive disclosure:**
```
SKILL.md:
## Hook Patterns

For detailed patterns, see **`references/patterns.md`**.

Key pattern types:
- PreToolUse validation
- PostToolUse notifications
- Stop handlers

references/patterns.md:
## Hook Patterns

[Comprehensive 2,000-word guide...]
```

**Rule:** Information should live in exactly one place. Reference it from elsewhere.

---

## Detection and Prevention

### Automated Detection

Create validation scripts to catch common mistakes:

```bash
#!/bin/bash
# validate-skill.sh

skill_file="SKILL.md"

# Check for SKILL.md existence
if [ ! -f "$skill_file" ]; then
  echo "❌ ERROR: SKILL.md not found"
  exit 1
fi

# Check for YAML frontmatter
if ! grep -q "^---$" "$skill_file"; then
  echo "❌ ERROR: Missing YAML frontmatter delimiters"
  exit 1
fi

# Check for required fields
if ! grep -q "^name:" "$skill_file"; then
  echo "❌ ERROR: Missing 'name' field"
  exit 1
fi

if ! grep -q "^description:" "$skill_file"; then
  echo "❌ ERROR: Missing 'description' field"
  exit 1
fi

# Check for second person
if grep -qi "you should\|you need to\|you can" "$skill_file"; then
  echo "⚠️  WARNING: Found second person (use imperative form)"
fi

# Check word count
word_count=$(wc -w < "$skill_file")
if [ $word_count -gt 3000 ]; then
  echo "⚠️  WARNING: SKILL.md too long ($word_count words, target <2000)"
fi

echo "✅ Validation complete"
```

### Manual Review Checklist

Before finalizing a skill, review:

**Critical:**
- [ ] Valid YAML frontmatter with name and description
- [ ] Description uses third person
- [ ] Description includes specific trigger phrases
- [ ] SKILL.md file exists with correct capitalization

**Major:**
- [ ] Body uses imperative form (no "you should")
- [ ] SKILL.md <2,000 words (ideally)
- [ ] References/ are linked from SKILL.md

**Minor:**
- [ ] Consistent section structure
- [ ] Examples included for abstract concepts
- [ ] Proper markdown formatting
- [ ] No duplicate content

---

## Quick Reference

### Critical Fixes

| Mistake | Fix | Priority |
|---------|-----|----------|
| Missing frontmatter | Add YAML with --- delimiters | Critical |
| Weak triggers | Add specific phrases in third person | Critical |
| Wrong filename | Use exactly SKILL.md | Critical |
| Second person | Convert to imperative form | Major |
| Bloated SKILL.md | Move content to references/ | Major |

### Validation Commands

```bash
# Validate YAML syntax
sed -n '/^---$/,/^---$/p' SKILL.md | yamllint

# Check word count
wc -w SKILL.md

# Find second person
grep -ni "you should\|you need to" SKILL.md

# Check for references
grep -n "references/" SKILL.md

# Validate structure
./scripts/validate-skill.sh SKILL.md
```

Avoid these common mistakes to create high-quality, effective skills that trigger reliably and provide excellent guidance.
