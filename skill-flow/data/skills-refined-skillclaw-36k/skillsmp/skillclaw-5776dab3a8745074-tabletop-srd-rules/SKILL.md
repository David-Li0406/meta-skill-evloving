---
name: tabletop-srd-rules
description: Use this skill when the GM needs to look up rules, reference what the SRD says, find official rules, get exact wording, check RAW (rules as written), verify rules references, or understand how mechanics work in tabletop RPGs like D20 5E or Daggerheart.
---

# Tabletop SRD Rule Lookup Skill

Provide authoritative rule lookups from the System Reference Documents (SRD) for various tabletop RPGs. Use the complete SRD markdown files in this skill's references directory to answer questions about official rules.

## When to Use This Skill

This skill applies when the user:
- Asks "what does the SRD say about..."
- Requests "official rules for..."
- Wants "exact wording of..."
- Asks for "RAW" (rules as written)
- Needs to verify a rule during gameplay
- Questions how a mechanic works
- Needs to look up class features, abilities, or adversary stat blocks

## SRD File Organization

The SRD files are located at `${CLAUDE_PLUGIN_ROOT}/skills/tabletop-srd-rules/references/srd/`:

| File/Directory | Contents |
|----------------|----------|
| `00_Legal.md` | CC-BY-4.0 attribution (required for any derivative work) |
| `01_PlayingTheGame.md` | Core mechanics: abilities, D20 tests, actions, combat, damage |
| `02_CharacterCreation.md` | Character creation rules and process |
| `03_Classes/` | Class descriptions (multiple files for different systems) |
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
| `abilities/` | Domain cards and abilities (specific to Daggerheart) |
| `adversaries/` | Adversary stat blocks by name (specific to Daggerheart) |
| `ancestries/` | Ancestry features and options (specific to Daggerheart) |
| `armor/` | Armor definitions and stats (specific to Daggerheart) |
| `classes/` | Class definitions (specific to Daggerheart) |
| `consumables/` | Consumable item definitions (specific to Daggerheart) |
| `contents/` | Core rules (Combat, Character Creation, etc.) (specific to Daggerheart) |
| `domains/` | Domain descriptions (specific to Daggerheart) |
| `environments/` | Environmental rules and hazards (specific to Daggerheart) |
| `frames/` | Campaign frame content (specific to Daggerheart) |
| `items/` | General item definitions (specific to Daggerheart) |
| `subclasses/` | Subclass definitions (specific to Daggerheart) |
| `weapons/` | Weapon definitions and stats (specific to Daggerheart) |

## Search Patterns for Large Files

For efficient searching of large SRD files, use grep with the following patterns.

### Searching Spells

Spells are organized under `#### Spell Name` headings. Use case-insensitive search:

```bash
# Find a specific spell (show 40 lines for full description)
grep -i -A 40 "^#### Fireball" "${CLAUDE_PLUGIN_ROOT}/skills/tabletop-srd-rules/references/srd/07_Spells.md"
```

### Searching Adversaries

Each adversary has its own file in `adversaries/`. Use case-insensitive search:

```bash
# Find a specific adversary by name (exact match)
cat "${CLAUDE_PLUGIN_ROOT}/skills/tabletop-srd-rules/references/srd/adversaries/Bear.md"
```