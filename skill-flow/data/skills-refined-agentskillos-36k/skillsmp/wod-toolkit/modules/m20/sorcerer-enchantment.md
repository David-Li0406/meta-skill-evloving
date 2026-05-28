# Sorcerer Enchantment Module

Create permanent and multi-use magic items for M20 Sorcerer.

## Invoked By

This module is called when creating:
- **Sorcerer PCs** with Artifact background (create the artifact)
- **Sorcerer PCs** with Enchantment Path (create 1-2 signature items)
- Standalone enchanted items for campaign use

When invoked from character creation:
- Artifact background items should match background rating in power level
- Enchantment Path PCs should have 1-2 items demonstrating their craft
- Link item documents from character sheet

## Overview

Enchantment creates **permanent or reusable magic items**. Unlike Alchemy, enchanted items can be used multiple times.

**Key Features**:
- **Ritual-only Path** — No quick spells
- **Creates lasting items** — Charms, talismans, artifacts
- **Requires crafting** — Both mundane and magical skills
- **No Aspects** — Level-based effects
- **Extended time** — Crafting + magical infusion

## Practice Variants

| Practice | Flavor | Typical Items |
|----------|--------|---------------|
| Enchantment (Traditional) | Mystical, symbolic | Amulets, rings, wands |
| Engineering (Hypertech) | Scientific gadgetry | Devices, implants |
| Craftwork | Artisanal, practical | Tools, weapons, clothing |

---

## System

### Time
**Crafting time + 1-3 days per level**

The mundane item must be crafted first (Crafts/Technology roll), then enchanted.

### Dice Pool
`Casting Attribute + Path Ability` at difficulty `Item Level + 4`

### Activation
Items may be:
- **Always active** — Continuous effect
- **Triggered** — Word, gesture, or condition activates
- **Limited use** — X uses per day/scene

### Maintenance
Higher-level items may require:
- Periodic Quintessence infusion
- Regular rituals
- Special storage conditions

---

## Effect Levels

| Level | Capability |
|-------|------------|
| • | Minor items (+1-2 dice or -1 difficulty, not obviously magical) |
| •• | Moderate items (+2 dice or -2 difficulty, subtle effects) |
| ••• | Obviously magical (+2 dice to multiple rolls, replicate 1 dot supernatural) |
| •••• | Superhuman (raise Attributes above 5, replicate 2 dots supernatural) |
| ••••• | Legendary (near-mythic, replicate 3 dots supernatural) |

---

## Price of Failure

**Simple Failure**: Wasted time and materials.

**Botch Options**:
| Result | Description |
|--------|-------------|
| Cursed Item | Works but with drawback |
| Unstable | Functions erratically |
| Explosion | Destroys item, damages enchanter |
| Wrong Effect | Does something unintended |
| Attracts Attention | Draws spirits, other supernaturals |

---

## Item Template

```markdown
### [Item Name] (•-•••••)

**Level**: [1-5]
**Base Item**: [What mundane object is enchanted]
**Crafting Time**: [Mundane crafting + enchantment days]

**Effect**: [Mechanical description]

**Activation**: [Always active / Trigger / Limited uses]

**Maintenance**: [Any upkeep requirements]

**Notes**: [Flavor, variations]
```

---

## Sample Enchanted Items

### Level • Items

#### Lucky Charm (•)
**Base Item**: Small token (coin, stone, pendant)  
**Effect**: +1 die to a specific type of roll (chosen at creation)  
**Activation**: Always active when carried  

#### Lockpicks of Finesse (•)
**Base Item**: Quality lockpick set  
**Effect**: -1 difficulty to lockpicking attempts  
**Activation**: Always active when used

### Level •• Items

#### Cloak of Shadows (••)
**Base Item**: Dark cloak or coat  
**Effect**: +2 dice to Stealth rolls in dim lighting  
**Activation**: Always active when worn

#### Truth-Seeker's Pendant (••)
**Base Item**: Pendant with clear gem  
**Effect**: Gem clouds when wearer hears a deliberate lie (1/scene)  
**Activation**: Triggered by spoken lies  

### Level ••• Items

#### Blade of Wounding (•••)
**Base Item**: Quality blade (knife, sword)  
**Effect**: +2 damage dice, wounds resist magical healing (+2 diff)  
**Activation**: Always active  
**Notes**: Visibly magical (faint glow, unusual cold)

#### Amulet of Mind Shield (•••)
**Base Item**: Amulet  
**Effect**: Replicates Mind Shields 1 (basic mental resistance)  
**Activation**: Always active when worn

### Level •••• Items

#### Gauntlets of Might (••••)
**Base Item**: Gloves or gauntlets  
**Effect**: Strength +2 (can exceed 5) while worn  
**Activation**: Always active when worn  
**Maintenance**: Must be oiled with Quintessence-infused solution monthly

#### Cloak of the Chameleon (••••)
**Base Item**: Cloak  
**Effect**: Replicates Psychic Invisibility 2 (3 uses per day)  
**Activation**: Command word  
**Maintenance**: Must be exposed to moonlight weekly

### Level ••••• Items

#### Ring of the Archmage (•••••)
**Base Item**: Ring with gem  
**Effect**: Replicates 3 dots of any one Path (chosen at creation)  
**Activation**: Varies by Path  
**Maintenance**: Requires weekly ritual and Quintessence

#### Boots of Seven Leagues (•••••)
**Base Item**: Quality boots  
**Effect**: Replicates Conveyance 5 (instantaneous travel, 1/day)  
**Activation**: Click heels together  
**Maintenance**: Must rest at least 8 hours between uses

---

## Creating New Items

### Step 1: Define the Effect
What does the item do? Reference effect levels.

### Step 2: Determine Level
Match effect to appropriate level.

### Step 3: Choose Base Item
The mundane item should thematically fit the enchantment:
- Weapons → combat effects
- Jewelry → mental/social effects
- Clothing → physical effects
- Tools → skill enhancements

### Step 4: Establish Requirements

**Materials by level**:
- Level 1-2: Quality mundane materials
- Level 3-4: Rare or exotic materials, Quintessence
- Level 5: Exceptional materials, significant Quintessence, possibly exotic components

### Step 5: Define Activation
- **Always active**: Simpler, but harder to conceal
- **Triggered**: More versatile, requires action to activate
- **Limited use**: Can be more powerful but runs out

### Step 6: Determine Maintenance
Higher-level items typically require:
- Regular Quintessence infusion
- Periodic rituals
- Special conditions (moonlight, blood, etc.)

---

## Advanced Enchantment

### Combining with Other Paths
An enchanter can store another hedge wizard's spell in an item:
- Enchanter provides the vessel
- Other caster provides the effect
- Both must succeed on their rolls

### Teaching Enchantment Patterns
- Can share specific item designs
- Student must have sufficient Path rating
- Teaching takes 1 week per item level

### Unique Items
Creating truly unique legendary items requires:
- Enchantment 5
- Extended story involvement
- Unique components
- Storyteller collaboration

---

## Comparison: Enchantment vs Alchemy

| Aspect | Enchantment | Alchemy |
|--------|-------------|---------|
| Duration | Permanent/reusable | One use |
| Creation time | Longer | Shorter |
| Materials | Physical objects | Ingredients/compounds |
| Maintenance | Often required | None |
| Flexibility | Fixed effect | Variable potency |

---

## Validation Checklist

- [ ] Level matches effect power
- [ ] Base item thematically appropriate
- [ ] Clear mechanical effect
- [ ] Activation method specified
- [ ] Maintenance requirements (if any)
- [ ] Fits "lasting item" theme
- [ ] Doesn't duplicate Alchemy (one-use)
- [ ] Doesn't exceed supernatural sources' capabilities
