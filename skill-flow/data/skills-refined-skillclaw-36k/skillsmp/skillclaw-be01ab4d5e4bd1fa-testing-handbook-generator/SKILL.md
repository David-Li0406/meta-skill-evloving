---
name: testing-handbook-generator
description: Use this skill when creating new skills based on the Trail of Bits Testing Handbook content for security testing tools and techniques.
---

# Testing Handbook Skill Generator

Generate and maintain Claude Code skills from the Trail of Bits Testing Handbook.

## When to Use

**Invoke this skill when:**
- Creating new security testing skills from handbook content.
- User mentions "testing handbook", "appsec.guide", or asks about generating skills.
- Bulk skill generation or refresh is needed.

**Do NOT use for:**
- General security testing questions (use the generated skills).
- Non-handbook skill creation.

## Handbook Location

The skill needs the Testing Handbook repository. See [discovery.md](discovery.md) for full details.

**Quick reference:** Check `./testing-handbook`, `../testing-handbook`, `~/testing-handbook` → ask user → clone as last resort.

**Repository:** `https://github.com/trailofbits/testing-handbook`

## Workflow Overview

```
Phase 0: Setup              Phase 1: Discovery
┌─────────────────┐        ┌─────────────────┐
│ Locate handbook │   →    │ Analyze handbook│
│ - Find or clone │        │ - Scan sections │
│ - Confirm path  │        │ - Classify types│
└─────────────────┘        └─────────────────┘
         ↓                          ↓
Phase 3: Generation        Phase 2: Planning
┌─────────────────┐        ┌─────────────────┐
│ TWO-PASS GEN    │   ←    │ Generate plan   │
│ Pass 1: Content │        │ - New skills    │
│ Pass 2: X-refs  │        │ - Updates       │
│ - Write to gen/ │        │ - Present user  │
└─────────────────┘        └─────────────────┘
         ↓
Phase 4: Testing           Phase 5: Finalize
┌─────────────────┐        ┌─────────────────┐
│ Validate skills │   →    │ Post-generation │
│ - Run validator │        │ - Update README │
│ - Test activation│       │ - Update X-refs │
│ - Fix issues    │        │ - Self-improve  │
└─────────────────┘        └─────────────────┘
```

## Scope Restrictions

**ONLY modify these locations:**
- `plugins/testing-handbook-skills/skills/[skill-name]/*` - Generated skills (as siblings to testing-handbook-generator).
- `plugins/testing-handbook-skills/skills/testing-handbook-generator/*` - Self-improvement.
- Repository root `README.md` - Add generated skills to table.

**NEVER modify or analyze:**
- Other plugins (`plugins/property-based-testing/`, `plugins/stati...`)