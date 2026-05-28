# Troubleshooting - Skill Activation Issues

Complete debugging guide for skill activation problems.

## Table of Contents

- [Skill Not Triggering](#skill-not-triggering)
- [False Positives](#false-positives)
- [Performance Issues](#performance-issues)

---

## Skill Not Triggering

### Symptoms
Ask a question or start a task, but relevant skill doesn't activate.

### Common Causes

#### 1. Keywords Don't Match

**Check:**
- Look at `intent_keywords` in registry.json
- Are the keywords actually in your input?
- Remember: case-insensitive substring matching

**Example:**
```json
"intent_keywords": ["layout", "grid"]
```
- "how does the layout work?" → ✅ Matches "layout"
- "how does the grid system work?" → ✅ Matches "grid"
- "how does it work?" → ❌ No match

**Fix:** Add more keyword variations to registry.json

#### 2. Skill Not Registered

**Check:**
```bash
cat .agent/skills/registry.json | jq '.skills[] | select(.id == "your-skill")'
```

**Fix:** Add skill entry to registry.json

#### 3. Invalid SKILL.md

**Check:**
- YAML frontmatter is valid
- File exists at specified path
- No syntax errors

**Example Valid Frontmatter:**
```yaml
---
name: your-skill
description: Your description here
---
```

---

## False Positives

### Symptoms
Skill activates when it shouldn't.

### Common Causes

#### 1. Keywords Too Generic

**Problem:**
```json
"intent_keywords": ["work", "system", "create"]
```
These match almost everything!

**Fix:** Use more specific keywords:
```json
"intent_keywords": ["pdf work", "pdf system", "create pdf"]
```

#### 2. Overlapping Keywords

**Problem:** Two skills share the same keywords.

**Fix:** 
- Make keywords more specific to each skill
- Add context words to disambiguate

---

## Performance Issues

### Symptoms
Noticeable delay before responses.

### Common Causes

#### 1. Too Many Patterns

**Problem:**
Every pattern = regex compilation + matching

**Solution:** Reduce patterns
- Combine similar patterns
- Remove redundant patterns

#### 2. Complex Regex

**Problem:**
```regex
(create|add|modify|update|implement|build).*?(feature|endpoint|route|service|controller|component)
```
Long alternations = slow

**Solution:** Simplify
```regex
(create|add).*?(feature|endpoint)
```

### Measure Performance

Performance should be imperceptible to users. If you notice delays:
1. Check number of registered skills
2. Review complexity of keywords
3. Consider caching strategies

---

## Quick Debug Checklist

1. [ ] Is skill listed in `registry.json`?
2. [ ] Do `intent_keywords` match your input?
3. [ ] Is `skill_path` correct?
4. [ ] Is SKILL.md valid frontmatter + markdown?
5. [ ] Are keywords specific enough?
6. [ ] Any JSON syntax errors?

---

**Related Files:**
- [SKILL.md](../SKILL.md) - Main skill guide
- [HOOK_MECHANISMS.md](HOOK_MECHANISMS.md) - How hooks work
- [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md) - Configuration reference
