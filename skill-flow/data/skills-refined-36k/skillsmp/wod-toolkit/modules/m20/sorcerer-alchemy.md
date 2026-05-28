# Sorcerer Alchemy Module

Create alchemical recipes (potions, tinctures, powders, salves) for M20 Sorcerer.

## Invoked By

This module is called when creating:
- **Sorcerer PCs** with Alchemy Path (create 1-2 signature recipes)
- Standalone recipes for campaign use

When invoked from character creation:
- Create 1-2 recipes the character has mastered
- Recipe levels should be ≤ Alchemy Path rating
- Include Practice-appropriate flavor (Herbalism vs Advanced Chemistry)
- Link recipe documents from character sheet

## Overview

Alchemy creates **one-use magical items** through careful preparation. Unlike Enchantment, alchemical products are consumed upon use.

**Key Features**:
- **Ritual-only Path** — No quick spells
- **Creates consumables** — Potions, powders, salves
- **Requires laboratory** — Equipment and ingredients
- **No Aspects** — Level-based effects
- **Extended time** — Days, not minutes

## Practice Variants

| Practice | Flavor | Ingredients |
|----------|--------|-------------|
| Alchemy (Traditional) | Hermetic, philosophical | Metals, minerals, symbols |
| Herbalism (Witchcraft) | Natural, folk magic | Plants, fungi, animal parts |
| Advanced Chemistry | Scientific, technological | Synthetic compounds |
| Brewing | Practical, homey | Kitchen ingredients |

---

## System

### Time
**1 day per recipe level**

**Reduction**: Path Ability rating above recipe level reduces time by 1 day each (minimum several hours).

### Dice Pool
`Casting Attribute + Path Ability` at difficulty `Recipe Level + 4`

### Success Allocation
One success creates the recipe. Additional successes can split between:
- **Additional doses** — 1 success per extra dose
- **Shelf life** — 1 success per day potent

### Duration of Effects
Most effects last **one scene** unless specified otherwise.

---

## Effect Levels

| Level | Capability |
|-------|------------|
| • | Enhanced mundane chemicals (+1 Toxin Rating) |
| •• | Exceed physical limits (+1 Attribute, max 5), cryptic visions |
| ••• | Grant low-level psychic abilities (1 dot, +1 per 2 extra successes) |
| •••• | Potent improvements (+2 Attribute/Ability, can exceed 5) |
| ••••• | Reproduce supernatural powers (up to 3 dots, requires exotic components) |

---

## Price of Failure

**Simple Failure**: Ruined ingredients, wasted time.

**Botch Options**:
| Result | Description |
|--------|-------------|
| Explosion | Laboratory damage, injury |
| Toxic Byproduct | Produces poison instead |
| False Success | Appears correct but wrong effect |
| Contamination | Ruins other ongoing projects |
| Unstable Result | Works initially, fails at worst moment |

---

## Recipe Template

```markdown
### [Recipe Name] (•-•••••)

**Level**: [1-5]
**Preparation Time**: [X days]
**Shelf Life**: [Duration]
**Form**: [Potion/Powder/Salve/Pill/etc.]

**Ingredients**:
- [List key components]

**Effect**: [Mechanical description]

**Side Effects**: [Any drawbacks]

**Notes**: [Flavor, variations]
```

---

## Sample Recipes

### Level • Recipes

#### Soporific Powder (•)
**Form**: Powder added to drink  
**Ingredients**: Valerian, poppy extract, alcohol  
**Effect**: Target rolls Stamina (diff 8) or falls asleep. Sleep lasts (10 - Stamina) hours.

#### Wound Balm (•)
**Form**: Salve  
**Effect**: Negates wound penalties up to Injured level until wounded again.

### Level •• Recipes

#### Speed Draught (••)
**Form**: Potion  
**Ingredients**: Caffeine extract, ginseng  
**Effect**: Doubles running speed for one scene.  
**Side Effects**: Roll Stamina (diff 6) at end or +2 difficulty on physical rolls for 1 hour.

#### Vision Elixir (••)
**Form**: Liquid (hallucinogenic)  
**Effect**: Grants cryptic vision of future events or hidden connections.

### Level ••• Recipes

#### Adamantine Alloy (•••)
**Form**: Metal alloy (requires smithing)  
**Ingredients**: Iron, rare earth metals, Quintessence minerals  
**Effect**: Weapons +1 damage, -1 difficulty. Armor +1 soak.

#### Psychic Awakener (•••)
**Form**: Pill or injection  
**Effect**: Grants 1 dot of psychic phenomenon for 1 hour. +1 dot per 2 extra successes.

### Level •••• Recipes

#### Metabolic Booster (••••)
**Form**: Injection or pill  
**Ingredients**: Synthetic hormones, rare catalysts  
**Effect**: Raises Strength AND Stamina by 1 each for scene. May exceed 5.  
**Side Effects**: Extreme hunger during effect.

#### Longevity Treatment (••••)
**Form**: Daily potion regimen  
**Effect**: For each year on regimen, age only one month.  
**Side Effects**: If discontinued, age catches up at 1 month per day until resumed or death.

### Level ••••• Recipes

#### Celerity Elixir (•••••)
**Form**: Potion  
**Ingredients**: Requires 5+ points of vampire blood  
**Effect**: Grants Potence 3 equivalent (3 auto-successes on Strength) for 3 hours.  
**Side Effects**: Desperate hunger, bloodlust. Willpower (diff 8) to resist feeding.

#### Regeneration Powder (•••••)
**Form**: Ingested powder  
**Ingredients**: Werewolf fur, regenerative compounds  
**Effect**: Heal 1 level bashing/lethal every other turn for one story.  
**Side Effects**: Heavy sweating, animal smell. +1 difficulty to social rolls.

---

## Advanced Alchemy

### Combining Recipes
Two alchemists working together:
- Both must have required Path levels
- Time = longer of the two recipes
- Difficulty = higher of the two +1
- Both must succeed

### Teaching Recipes
- Student must have sufficient Path rating
- Teaching takes 1 week per recipe level
- No roll required if teacher succeeds on Intelligence + Instruction (diff 6)

### Legendary Recipes
The **Great Work** and similar require:
- Alchemy 5
- Extended campaigns
- Unique components (Philosopher's Stone ingredients, etc.)
- Storyteller collaboration

---

## Creating New Recipes

### Step 1: Define the Effect
What does the recipe do? Reference effect levels.

### Step 2: Determine Level
Match effect to appropriate level.

### Step 3: Establish Requirements

**Ingredients by level**:
- Level 1-2: Common (herbs, minerals, chemicals)
- Level 3-4: Rare (specific plants, exotic metals)
- Level 5: Exotic (supernatural components)

**Equipment**:
- Basic: Mortar and pestle, heat source
- Standard: Full laboratory
- Advanced: Specialized equipment

### Step 4: Add Conditions (Optional)
- **Time of creation**: Full moon, dawn, etc.
- **Consumption method**: Inhaled, injected, topical
- **Side effects**: Temporary drawbacks
- **Limitations**: Only works on certain targets

---

## Validation Checklist

- [ ] Level matches effect power
- [ ] Ingredients appropriate to level
- [ ] Clear mechanical effect
- [ ] Side effects balance powerful effects
- [ ] Form specified
- [ ] Fits "one-use item" theme
- [ ] Doesn't replicate Enchantment (permanent items)
- [ ] Doesn't exceed supernatural sources' capabilities
