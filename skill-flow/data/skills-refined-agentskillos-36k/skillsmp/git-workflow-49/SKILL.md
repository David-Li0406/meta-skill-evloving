---
name: git-workflow
description: Manage Git workflow for campaign content with proper commit messages and branching
license: MIT
compatibility: opencode
metadata:
  audience: campaign-managers
  workflow: jekyll
---

## What I do

- Create detailed creature/monster articles for The Scarlet Wood TTRPG campaign hub
- Follow Utopia TTRPG system rules for stats and abilities

## When to use me

Use this when generating new creature stats articles based on user input descriptions.
Ask clarifying questions if user input is missing key details or is ambiguous.

# Create Creature Skill

## Description

This skill assists in creating detailed creature/monster articles for The Scarlet Wood TTRPG
campaign hub, following the Utopia TTRPG system rules and the established Jekyll site structure.

## Purpose

Generate complete, campaign-ready creature articles with:

- Proper stat blocks using Utopia TTRPG mechanics
- Lore and ecological information
- Combat tactics and behavior
- Proper Jekyll front matter and markdown formatting
- Internal links following site conventions

## Input Parameters

The skill accepts natural language descriptions containing:

### Required Information

- **Name:** The creature's name
- **Basic concept:** What kind of creature it is
- **Size:** Small, Medium, or Large
- **Role:** Enemy, neutral, or potential ally

### Recommended Information

- **Habitat:** Where it lives
- **Behavior:** How it acts
- **Combat style:** Aggressive, defensive, ambush, etc.
- **Special abilities:** Unique powers or traits
- **Appearance:** Physical description

### Optional Information

- **Loot:** What can be harvested
- **Variants:** Different versions of the creature
- **Relationships:** Connections to factions/NPCs
- **Campaign integration:** Where it has appeared

## Process

1. **Gather Information:** Extract creature details from user input
2. **Generate Stats:** Create appropriate stat block using Utopia TTRPG rules:
   - Constitution, Endurance, Effervescence based on creature body, kit(s), class(es)
   - Block/Dodge ratings appropriate to size and nature
   - HP and Stamina calculations
   - Ability scores and modifiers (Agility, Strength, Intellect, Will, Display, Charm)
   - Defenses (Physical, Energy, Heat, Cold, Psychic)
3. **Design Abilities:** Create attacks and special abilities using item creation rules
4. **Write Lore:** Develop overview, appearance, ecology sections
5. **Add Tactical Info:** Define behavior, tactics, weaknesses
6. **Format Document:** Apply Jekyll front matter and markdown structure
7. **Add Links:** Include appropriate internal references

## Utopia TTRPG Rules Reference

### Size Categories

- **Small:** Fragile, evasive (higher dodge, lower block)
- **Medium:** Balanced, versatile
- **Large:** Tough, powerful (higher block, lower dodge)

### Core Statistics

- **Constitution:** 3-6 (base hit points)
- **Endurance:** 3-6 (stamina pool)
- **Effervescence:** 3-6 (elemental/magic resistance)

### Ability Scores

All creatures have six main abilities (scale 1-10+), each with two sub-abilities:

- **Agility** (Speed, Dexterity)
- **Strength** (Power, Fortitude)
- **Intellect** (Engineering, Memory)
- **Will** (Resolve, Awareness)
- **Display** (Portrayal, Stunt)
- **Charm** (Appeal, Language)

Modifiers = Score - 4
Sub-abilities can never exceed main ability score.

### Combat

- **Block Rating:** Dice notation (e.g., 2d4, 3d4; always multiples of d4)
- **Dodge Rating:** Dice notation (e.g., 2d12, 3d12; always multiples of d12)
- **Damage Types:** Physical, Energy, Heat, Cold, Psychic
- **Attack Format:** Type, Range, Damage dice, Special effects

## Output Format

Generate a complete markdown file following this structure:

```markdown
---
layout: page
title: [Creature Name]
summary: [One-line description]
topic: Creatures
tags:
    - creature
    - [combat/exploration/social]
    - [enemy/neutral/ally]
    - [habitat type]

published: false # REMOVE WHEN LIVE
---

![Creature Token]({{ "/assets/images/[slug]_token.png" | relative_url }})
{: .character-token}

[2-3 sentence introduction]

## Overview

[Detailed description of creature's role, behavior, and place in world]

## Appearance

- **Species/Type:** [Type]
- **Size:** [Small/Medium/Large]
- **Physical Description:** [Visual details]
- **Notable Features:** [Distinguishing characteristics]

## Stat Block

### Basic Statistics

- **Constitution:** [number]
- **Endurance:** [number]
- **Effervescence:** [number]
- **Gifted:** [List gifted subtraits]
- **Block Rating:** [dice]
- **Dodge Rating:** [dice]
- **Size:** [Size]
- **HP:** [value or formula]
- **Stamina:** [value or formula]

### Defenses

- **Physical Defense:** [number]
- **Elemental Defense:** [number]
- **Mental Defense:** [number]

### Abilities

[Full ability and sub-ability score breakdown with modifiers]

### Attacks

[Attack entries with type, range, damage, special effects]

### Abilities and Quirks

[Special abilities with costs and effects]

## Behavior and Tactics

[Combat behavior and strategy]

## Ecology and Habitat

[Where found, diet, social structure, activity patterns]

## Loot and Resources

[Harvestable materials]

## Links

- Back to [World]({{ "/world/" | relative_url }})
[Additional relevant links]
```

## Jekyll Site Conventions

### Front Matter

- `layout: page` (always)
- `title:` in Title Case
- `summary:` brief one-liner
- `topic: Creatures` (groups on world index)
- `tags:` kebab-case array
- `published: false` while drafting

### File Location

Save to: `_world/creatures/[creature-name].md`

### Markdown Style

- Headings: ATX style (`#`, `##`)
- Line length: ~100 characters
- Lists: 2-space indent
- Code: Backticks for inline, fenced for blocks

### Internal Links

Always use Jekyll's `relative_url` filter:

```markdown
[Link Text]({{ "/world/creatures/creature-name/" | relative_url }})
```

### Image References

```markdown
![Alt Text]({{ "/assets/images/filename.png" | relative_url }})
```

## Example Usage

**User Input:**
"Create a Shadow Stalker - a medium-sized feline predator that hunts at dusk in the deep forest. 
It can blend into shadows and pounce from darkness. Aggressive but intelligent, flees if badly 
wounded."

**Skill Output:**
Complete markdown file with:

- Title: Shadow Stalker
- Stats based on 'Beast' body, 'Evasive' and 'Aggressive' kits
- Shadow-themed attack items/actions
- Proper front matter and formatting
- Image placeholder
- Appropriate internal links

## Quality Checklist

Before finalizing, verify:

- [ ] Front matter complete and valid YAML
- [ ] Title, summary, and topic set
- [ ] Stats match selected body/kit(s)/class(es)
- [ ] All ability scores have modifiers
- [ ] Attacks include type, range, damage
- [ ] Defenses calculated correctly
- [ ] All internal links use `relative_url` filter
- [ ] Line length ~100 characters
- [ ] 2-space indentation for lists
- [ ] `published: false` set for drafting

## Notes for AI Assistant

- **Correctness:** Follow Utopia TTRPG custom creature and custom item rules precisely, ask for clarifications if needed
- **Balance:** Stats should be challenging but fair for party encounters
- **Flavor:** Include evocative descriptions that inspire roleplaying
- **Consistency:** Match lore established in other campaign documents
- **Clarity:** GMs should immediately understand how to run this creature
- **Completeness:** Provide enough detail without overwhelming
- **Flexibility:** Include variant options for different encounter types
- **Integration:** Reference related factions, NPCs, locations when appropriate

## Workflow

1. Analyze user input for key creature details
2. Determine appropriate creature body, kit(s), and class(es) from Utopia TTRPG Custom Creature Rules
3. Calculate stats based on selected body/kit(s)/class(es)
4. Determine appropriate attacks/actions using item creation rules from Utopia TTRPG Custom Item Rules
5. Calculate harvestable resources per Utopia TTRPG Custom Creature Rules
6. Format with proper front matter
7. Add image placeholder and links
8. Review against quality checklist

## Related Files

- Template: `content-templates/creature-article-template.md`
- Creature Rules Reference: `assets/Utopia_TTRPG_Custom_Creature_Rules_ocred.pdf`
- Item Rules Reference: `assets/Utopia_TTRPG_Custom_Item_Rules_ocred.pdf`
- Example Creatures: `_dm/npc-stats/*.md`
- Configuration: `_config.yml` (collections, permalinks)
