---
name: terminology-management
description: 術語表管理與一致性檢查。Use when managing glossary, checking term consistency, or making terminology decisions.
---

# Terminology Management

## Glossary Structure

Location: `glossary.json` (project root)

```json
{
  "Move": {
    "zh": "動作",
    "notes": "PbtA 系統核心機制"
  },
  "Playbook": {
    "zh": "劇本",
    "notes": "角色模板，也可譯為「職業書」"
  }
}
```

## Operations

### Add Term

1. Check if term exists in glossary
2. If new, add with translation and context notes
3. Update all existing documents with new term

### Check Consistency

Scan all `.md` files in `docs/src/content/docs/`:

1. Extract English terms (capitalized words, quoted terms)
2. Cross-reference with `glossary.json`
3. Report:
   - Missing terms (not in glossary)
   - Inconsistent usage (same term, different translations)
   - Untranslated terms (English in final output)

### Batch Replace

When terminology decision is made:

1. Record in `style-decisions.json`
2. Find all occurrences across docs
3. Replace with consistent translation
4. Verify no orphaned terms remain

## Style Decisions

Location: `style-decisions.json` (project root)

```json
{
  "dice_notation": {
    "decision": "保留原文",
    "alternatives": ["翻譯為中文"],
    "reason": "2d6 等骰子標記為國際通用，保留更清晰"
  },
  "game_title": {
    "decision": "使用官方中文名",
    "alternatives": ["音譯", "意譯"],
    "reason": "遵循官方授權翻譯"
  }
}
```

## Consistency Report Format

```markdown
## Terminology Report

### Missing from Glossary
- `Harm` (found in: combat.md:15, conditions.md:23)
- `Hold` (found in: basic-moves.md:42)

### Inconsistent Usage
- `Move`: "動作" (5x), "行動" (2x)
  - Files: rules/index.md, combat.md

### Untranslated
- "Experience" in characters/advancement.md:18
```

## Priority Categories

| Category | Handling |
|----------|----------|
| Core mechanics | Must be consistent, add to glossary first |
| Proper nouns | Check official translations, record decision |
| Flavor text | More flexible, prioritize readability |
| UI/System terms | Match Starlight conventions |
