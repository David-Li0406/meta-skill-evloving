# Skill Quality Checklist

Use this checklist to validate your skill before committing.

---

## Required: SKILL.md Structure

- [ ] **File exists:** `SKILL.md` (case-sensitive) in skill directory
- [ ] **Frontmatter starts on line 1** (no blank lines before `---`)
- [ ] **Frontmatter ends with `---`** before markdown content
- [ ] **Uses spaces** for YAML indentation (not tabs)

## Required: Metadata Fields

- [ ] **`name` field present**
  - Lowercase letters, numbers, hyphens only
  - Max 64 characters
  - Matches directory name (recommended)

- [ ] **`description` field present**
  - Max 1024 characters
  - Includes specific action verbs
  - Contains trigger keywords users would say
  - Avoids vague phrases ("helps with", "assists in")

## Recommended: Content Quality

### Description Effectiveness

- [ ] **Answers "What does it do?"** - Lists specific capabilities
- [ ] **Answers "When to use?"** - Includes natural trigger phrases
- [ ] **Distinct from other skills** - Won't conflict with similar skills
- [ ] **Domain-specific terms** - Includes relevant keywords (e.g., "PDF", "SQL", "tests")

### Instructions Clarity

- [ ] **Has clear overview** - 1-2 sentences explaining the skill
- [ ] **Uses numbered steps** - Easy to follow sequentially
- [ ] **Includes examples** - At least one concrete usage example
- [ ] **Documents prerequisites** - Lists required packages/tools

### Structure

- [ ] **Under 500 lines** - Use progressive disclosure if longer
- [ ] **Clear section headings** - Easy to navigate
- [ ] **No orphan content** - Every section serves a purpose

## Optional: Advanced Features

### Tool Restrictions

- [ ] **`allowed-tools` appropriate** - Matches skill scope
- [ ] **Read-only skills restrict writes** - Use `Read, Grep, Glob`
- [ ] **Command-specific restrictions** - Use `Bash(cmd:*)` patterns

### Supporting Files

- [ ] **Large content split out** - Detailed docs in separate files
- [ ] **Files are linked** - SKILL.md references supporting files
- [ ] **Scripts are executable** - `chmod +x` applied if needed

### Progressive Disclosure

- [ ] **Essential info in SKILL.md** - Quick start, overview
- [ ] **Details in supporting files** - Reference, troubleshooting
- [ ] **Clear links** - Users know where to find more

---

## Validation Tests

### Test 1: Description Discovery

Ask Claude: *"What skills are available?"*
- [ ] Your skill appears in the list
- [ ] Description accurately represents the skill

### Test 2: Natural Trigger

Say something that should trigger the skill (using words from description):
- [ ] Skill activates automatically
- [ ] Claude follows the skill's instructions

### Test 3: Edge Cases

Try variations of trigger phrases:
- [ ] Works with different wordings
- [ ] Doesn't trigger for unrelated requests

---

## Common Issues & Fixes

| Issue | Check | Fix |
|-------|-------|-----|
| Skill not found | File path | Ensure `SKILL.md` in correct location |
| Skill not triggering | Description | Add more trigger keywords |
| Wrong skill triggers | Description overlap | Make descriptions more distinct |
| YAML parse error | Frontmatter syntax | Check for tabs, missing `---` |
| Tools not available | `allowed-tools` | Verify tool names are correct |

---

## Final Review

Before committing:

- [ ] **Tested locally** - Skill works as expected
- [ ] **No secrets** - No API keys, passwords, or sensitive data
- [ ] **Team reviewed** - (For project skills) Others have tested
- [ ] **Version noted** - Document version/date if applicable

---

## Quick Validation Commands

```bash
# Check skill exists in correct location
ls -la .claude/skills/your-skill/SKILL.md

# Verify YAML frontmatter (should show clean output)
head -20 .claude/skills/your-skill/SKILL.md

# Count lines (should be < 500 for SKILL.md)
wc -l .claude/skills/your-skill/SKILL.md
```
