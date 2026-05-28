# Chimera Module

Create chimerical creatures and items for C20—companions, mounts, guardians, voile, and chimerical weapons/tools.

## Chimera Types

| Type | Description | Module Section |
|------|-------------|----------------|
| **Companion** | Sentient creature, loyal to changeling | Companion Creation |
| **Mount** | Rideable creature | Companion Creation |
| **Guardian** | Protective creature (freehold) | Companion Creation |
| **Item** | Chimerical weapon, tool, or object | Item Creation |
| **Voile** | Chimerical clothing, jewelry | Item Creation |
| **Dreaming Native** | Wild chimera encountered in Dreaming | Antagonist/NPC |

## Context

| Context | Save Location | Notes |
|---------|---------------|-------|
| Character background | `[character]/chimera/` | Personal chimera |
| Freehold | `[freehold]/chimera/` | Freehold guardians/features |
| Standalone | `./chimera/` | General creation |

---

## Companion Chimera Creation

### What is a Companion Chimera?

A sentient (or semi-sentient) creature made of dreamstuff, bonded to a changeling or freehold. Can range from a talking cat to a dragon mount.

### Companion Workflow

1. **Concept** — Species/form, personality, origin
2. **Intelligence Level** — Non-sentient, semi-sentient, fully sentient
3. **Attributes** — Based on creature type and power level
4. **Abilities** — Relevant creature abilities
5. **Redes** — Special chimera powers (see Redes section)
6. **Glamour** — Chimera's own Glamour pool
7. **Health Levels** — Based on size/power
8. **Appearance** — Chimerical description
9. **Bond** — Relationship to owner
10. **Validate**

### Companion Power Levels

| Level | Glamour | Attributes | Redes | Examples |
|-------|---------|------------|-------|----------|
| Minor (1-2 dots) | 2-3 | 5/3/2 | 1-2 | Small pet, minor sprite |
| Standard (3 dots) | 4-5 | 7/5/3 | 2-3 | Loyal hound, riding horse |
| Powerful (4 dots) | 6-7 | 8/6/4 | 3-4 | War steed, guardian beast |
| Legendary (5 dots) | 8+ | 9/7/5 | 4-5 | Dragon, sphinx |

### Companion Attributes

Chimera use simplified Attributes:

**Physical**: Strength, Dexterity, Stamina
**Mental**: Perception, Intelligence, Wits
**Social**: (Optional for sentient) Charisma, Manipulation, Appearance

Allocate as X/Y/Z where X is primary category.

### Redes (Chimera Powers)

Redes are special abilities unique to chimera. Each companion gets 1-5 based on power level.

| Rede | Effect |
|------|--------|
| Armor | Natural armor, soak bonus |
| Claws/Fangs | Natural weapons |
| Flight | Can fly |
| Glamour Sense | Detect Glamour/magic |
| Hide | Become invisible or blend in |
| Increased Attribute | +2 to one Attribute |
| Poison | Venomous attack |
| Regeneration | Heal faster |
| Shapeshift | Change form |
| Size (Large) | Bigger than normal |
| Size (Small) | Smaller than normal |
| Speech | Can speak |
| Speed | Enhanced movement |
| Swim | Aquatic movement |
| Wyrd | Affect mortals physically |

Reference: `lookup.py chimera.redes redes`

### Chimera Health Levels

| Size | Health Levels |
|------|---------------|
| Tiny (mouse, sprite) | 3 |
| Small (cat, raven) | 5 |
| Medium (dog, human-sized) | 7 |
| Large (horse, lion) | 9 |
| Huge (elephant, dragon) | 11+ |

### Sentience Levels

| Level | Description | Communication |
|-------|-------------|---------------|
| Non-sentient | Animal intelligence | Instinct only |
| Semi-sentient | Clever animal, basic understanding | Simple concepts, emotions |
| Sentient | Human-level intelligence | Full speech, complex thought |

---

## Item Chimera Creation

### What is Item Chimera?

Chimerical objects—weapons, tools, clothing (voile), or other items made of dreamstuff. Exist only to fae sight unless they have the Wyrd quality.

### Item Workflow

1. **Type** — Weapon, armor, tool, voile, misc
2. **Appearance** — Chimerical description
3. **Function** — What it does
4. **Properties** — Special qualities
5. **Glamour Cost** — If any to use
6. **Origin** — How it was created/obtained
7. **Validate**

### Item Categories

| Category | Examples | Typical Properties |
|----------|----------|-------------------|
| Weapon | Sword, bow, gun | Damage bonus, special attack |
| Armor | Shield, chainmail | Soak bonus, protection |
| Tool | Lockpicks, compass | Skill bonus, special function |
| Voile | Cloak, crown, jewelry | Appearance, minor powers |
| Vehicle | Flying carpet, car | Transportation |
| Container | Bag of holding, chest | Storage, protection |

### Chimerical Weapons

| Weapon | Damage | Conceal | Notes |
|--------|--------|---------|-------|
| Knife/Dagger | Str+1 | P | |
| Sword | Str+2 | T | |
| Great Sword | Str+3 | N | Two-handed |
| Axe | Str+2 | T | |
| Spear | Str+2 | N | Reach |
| Bow | 4 | N | Ranged |
| Chimerical Gun | 5 | J-N | Ranged, modern |

**Conceal**: P = Pocket, J = Jacket, T = Trenchcoat, N = Not concealable

### Chimerical Armor

| Armor | Soak | Penalty | Notes |
|-------|------|---------|-------|
| Leather | +1 | 0 | Light |
| Chain | +2 | -1 | Medium |
| Plate | +3 | -2 | Heavy |
| Shield | +1 | 0 | Requires hand |

### Special Properties (Items)

| Property | Effect |
|----------|--------|
| Bane | Extra damage vs. specific target |
| Glamour Battery | Stores Glamour |
| Loyal | Returns to owner |
| Shrinking | Can change size |
| Unbreakable | Cannot be destroyed normally |
| Wyrd | Affects the mundane world |

---

## Voile (Chimerical Attire)

Voile is chimerical clothing and personal items. Most changelings create voile during Chrysalis—it doesn't require the Chimera background.

### Common Voile

| Item | Description |
|------|-------------|
| Faerie garb | Clothing matching kith/court |
| Jewelry | Rings, necklaces, crowns |
| Cloaks | Dramatic outerwear |
| Armor | Decorative or functional |
| Accessories | Bags, belts, pouches |

### Voile Properties

Basic voile has no mechanical effect—it's purely aesthetic. Significant voile may have minor properties:

| Property | Effect |
|----------|--------|
| Impressive | +1 die to social rolls when worn |
| Concealing | Hides items, harder to spot |
| Comfortable | Never uncomfortable, temperature-appropriate |
| Signature | Instantly recognizable, tied to identity |

---

## Chimera vs. Treasure

| Aspect | Chimera | Treasure |
|--------|---------|----------|
| Background | Chimera | Treasure |
| Nature | Dreamstuff | Enchanted real/chimerical item |
| Creation | Born/dreamed | Crafted/imbued |
| Visibility | Fae only (unless Wyrd) | May be visible to mortals |
| Power Source | Own Glamour | Stored/channeled Glamour |

If an item has active magical powers (cantrip effects), it's likely a Treasure.
If it's a creature or simple chimerical object, it's Chimera.

---

## Output Format (Companion)

```markdown
# [Chimera Name]

**Type**: Companion Chimera
**Form**: [Creature type]
**Intelligence**: [Non-sentient/Semi-sentient/Sentient]
**Size**: [Tiny/Small/Medium/Large/Huge]
**Owner/Bond**: [Character or Freehold name]

## Concept
[Description of the chimera's nature and personality]

## Appearance
[Chimerical appearance description]

## Attributes

### Physical
| Attribute | Rating |
|-----------|--------|
| Strength | [N] |
| Dexterity | [N] |
| Stamina | [N] |

### Mental
| Attribute | Rating |
|-----------|--------|
| Perception | [N] |
| Intelligence | [N] |
| Wits | [N] |

## Abilities
| Ability | Rating |
|---------|--------|
| [Ability] | [N] |

## Redes
| Rede | Effect |
|------|--------|
| [Rede] | [Description] |

## Statistics
| Stat | Value |
|------|-------|
| Glamour | [N] |
| Health Levels | [N] |
| Willpower | [N] (if sentient) |

## Origin
[How the chimera came to be and bonded with owner]

## Personality & Behavior
[How the chimera acts and what it wants]
```

## Output Format (Item)

```markdown
# [Item Name]

**Type**: Item Chimera / Voile
**Category**: [Weapon/Armor/Tool/Voile/etc.]
**Owner**: [Character or Freehold name]

## Appearance
[Chimerical description]

## Function
[What the item does]

## Properties
| Property | Effect |
|----------|--------|
| [Property] | [Description] |

## Statistics (if weapon/armor)
| Stat | Value |
|------|-------|
| Damage/Soak | [N] |
| Conceal | [Rating] |

## Origin
[How the item was created/obtained]
```

---

## Validation

### Companion
- [ ] Power level matches Chimera background dots
- [ ] Attributes allocated correctly for power level
- [ ] Redes within limit for power level
- [ ] Glamour pool set correctly
- [ ] Health levels match size
- [ ] Sentience level noted
- [ ] Bond to owner specified

### Item
- [ ] Type clearly categorized
- [ ] Properties appropriate for power level
- [ ] Statistics provided for weapons/armor
- [ ] Origin explained
