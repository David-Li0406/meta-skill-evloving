---
name: srd-rule-lookup
description: Use this skill when the GM needs to look up rules, reference what the SRD says, find official rules, get exact wording, check RAW (rules as written), verify rules references, or understand how mechanics work in either Daggerheart or d20 5E.
---

# SRD Rule Lookup Skill

Provide authoritative rule lookups from the System Reference Documents (SRD) for both Daggerheart and d20 5E. Use the complete SRD markdown files in this skill's references directory to answer questions about official rules.

## When to Use This Skill

This skill applies when the user:
- Asks "what does the SRD say about..."
- Requests "official rules for..."
- Wants "exact wording of..."
- Asks for "RAW" (rules as written)
- Needs to verify a rule during gameplay
- Questions how a mechanic works
- Needs to look up adversary stat blocks
- Needs class feature or ability details
- Needs domain card descriptions (for Daggerheart)

## SRD File Organization

### Daggerheart SRD Directory

The Daggerheart SRD files are located at `${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/`:

| Directory | Contents |
|-----------|----------|
| `abilities/` | Domain cards and abilities (Arcana, Blade, Bone, etc.) |
| `adversaries/` | Adversary stat blocks by name |
| `ancestries/` | Ancestry features and options |
| `armor/` | Armor definitions and stats |
| `classes/` | Class definitions (9 classes: Bard, Druid, Guardian, Ranger, Rogue, Seraph, Sorcerer, Warrior, Wizard) |
| `communities/` | Community features and options |
| `contents/` | Core rules (Combat, Character Creation, etc.) |
| `domains/` | Domain descriptions (9 domains: Arcana, Blade, Bone, Codex, Grace, Midnight, Sage, Splendor, Valor) |
| `environments/` | Environmental rules and hazards |
| `frames/` | Campaign frame content |
| `items/` | General item definitions |
| `subclasses/` | Subclass definitions |
| `weapons/` | Weapon definitions and stats |

### d20 5E SRD Directory

The d20 SRD files are located at `${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/`:

| File | Contents |
|------|----------|
| `00_Legal.md` | CC-BY-4.0 attribution (required for any derivative work) |
| `01_PlayingTheGame.md` | Core mechanics: abilities, D20 tests, actions, combat, damage |
| `02_CharacterCreation.md` | Character creation rules and process |
| `03_Classes/` | Class descriptions (12 files, one per class) |
| `04_CharacterOrigins.md` | Backgrounds, species, and origin features |
| `05_Feats.md` | Feat descriptions and requirements |
| `06_Equipment.md` | Weapons, armor, adventuring gear, trade goods |
| `07_Spells.md` | All spell descriptions (A-Z) |
| `08_RulesGlossary.md` | Alphabetical rules definitions |
| `09_GameplayToolbox.md` | Optional rules and DM tools |
| `10_MagicItems.md` | Magic item descriptions |
| `11_Monsters.md` | Monster creation and CR rules |
| `12_MonstersA-Z.md` | All monster stat blocks (A-Z) |
| `13_Animals.md` | Animal stat blocks and mounts |

## Search Patterns for SRD Files

### Searching Daggerheart Adversaries

```bash
# Find a specific adversary by name (exact match)
cat "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/adversaries/Bear.md"
```

### Searching d20 Spells

```bash
# Find a specific spell (show 40 lines for full description)
grep -i -A 40 "^#### Fireball" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/07_Spells.md"
```

## Response Format

When answering rule questions:

1. Quote the exact SRD text first (use blockquotes)
2. Cite the source file
3. Explain or clarify if needed
4. Note any related rules

### Example Response

> From `08_RulesGlossary.md`:
>
> **Advantage**
> If you have Advantage on a D20 Test, roll two d20s, and use the higher roll. A roll can't be affected by more than one Advantage, and Advantage and Disadvantage on the same roll cancel each other.

This means having multiple sources of Advantage doesn't stack - you still only roll two dice.

## Attribution Requirement

When quoting substantial portions of the SRD in any output, include the appropriate attribution:

For Daggerheart:
> This work includes material from the Daggerheart System Reference Document 1.0, published by Darrington Press. Daggerheart and all related marks are trademarks of Critical Role, LLC and used under the Darrington Press Community Gaming License (DPCGL). See https://www.daggerheart.com/ for full license terms.

For d20 5E:
> This work includes material from the System Reference Document 5.2 ("SRD 5.2") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

## Common Rule Categories

| Question About | Search Location |
|----------------|-----------------|
| How combat works | `contents/` (Combat.md for Daggerheart, `01_PlayingTheGame.md` for d20) |
| Class features | `classes/[class].md` |
| Spell effects | `abilities/` (for Daggerheart), `07_Spells.md` (for d20) |
| Adversary stat block | `adversaries/[name].md` (for Daggerheart), `12_MonstersA-Z.md` (for d20) |
| Weapon stats | `weapons/` (for Daggerheart), `06_Equipment.md` (for d20) |
| Armor stats | `armor/` (for Daggerheart), `06_Equipment.md` (for d20) |

## Notes

- The SRD contains only rules released under the respective licenses; some content may be excluded.
- For quick lookups, `cat` the specific file; for broad searches, use `grep -ri`.