# registry.json - Complete Reference

Complete schema and configuration reference for `.agent/skills/registry.json`.

## Table of Contents

- [File Location](#file-location)
- [Complete Schema](#complete-schema)
- [Field Guide](#field-guide)
- [Examples](#examples)
- [Validation](#validation)

---

## File Location

**Path:** `.agent/skills/registry.json`

This JSON file defines all skills and their trigger conditions for the auto-activation system.

---

## Complete Schema

```typescript
interface SkillRegistry {
    version: string;
    skills: SkillEntry[];
}

interface SkillEntry {
    id: string;                    // Unique identifier
    intent_keywords: string[];     // Trigger keywords
    skill_path: string;            // Path to SKILL.md
    description: string;           // Brief description (max 1024 chars)
}
```

---

## Field Guide

### id (required)
- **Type**: string
- **Purpose**: Unique identifier for the skill
- **Convention**: lowercase-with-dashes
- **Example**: `"frontend-design"`, `"pdf-processor"`

### intent_keywords (required)
- **Type**: string[]
- **Purpose**: Words/phrases that trigger this skill
- **Matching**: Case-insensitive substring match
- **Example**: `["pdf", "extract pdf", "merge pdf"]`

### skill_path (required)
- **Type**: string
- **Purpose**: Relative path to SKILL.md
- **Convention**: Always starts with `.agent/skills/`
- **Example**: `".agent/skills/pdf/SKILL.md"`

### description (required)
- **Type**: string
- **Purpose**: Brief description for routing decisions
- **Limit**: Max 1024 characters
- **Content**: Should match SKILL.md frontmatter description

---

## Examples

### Basic Skill Entry

```json
{
    "id": "pdf",
    "intent_keywords": ["pdf"],
    "skill_path": ".agent/skills/pdf/SKILL.md",
    "description": "Comprehensive PDF manipulation toolkit..."
}
```

### Multi-Keyword Skill

```json
{
    "id": "frontend-design",
    "intent_keywords": [
        "frontend design",
        "frontend",
        "ui",
        "ux",
        "dashboard",
        "react component"
    ],
    "skill_path": ".agent/skills/frontend-design/SKILL.md",
    "description": "Create distinctive, production-grade frontend interfaces..."
}
```

---

## Validation

### Check JSON Syntax

```bash
cat .agent/skills/registry.json | jq .
```

If valid, jq will pretty-print the JSON. If invalid, it will show the error.

### Common JSON Errors

**Trailing comma:**
```json
{
  "keywords": ["one", "two",]  // ❌ Trailing comma
}
```

**Missing quotes:**
```json
{
  id: "guardrail"  // ❌ Missing quotes on key
}
```

### Validation Checklist

- [ ] JSON syntax valid (use `jq`)
- [ ] All skill IDs are unique
- [ ] All skill_path files exist
- [ ] Descriptions under 1024 chars
- [ ] Keywords are relevant and specific
- [ ] No duplicate keywords across unrelated skills

---

**Related Files:**
- [SKILL.md](../SKILL.md) - Main skill guide
- [TRIGGER_TYPES.md](TRIGGER_TYPES.md) - Complete trigger documentation
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Debugging configuration issues
