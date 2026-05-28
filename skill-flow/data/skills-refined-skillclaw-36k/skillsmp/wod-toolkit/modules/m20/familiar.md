# Familiar Module

Create familiar characters: spirits incarnated into physical bodies who are bonded to mages.

## Invoked By

This module is called when creating:
- **Familiar as PC** — Standalone familiar character (25 freebies)
- **Familiar for PC** — Via mage's Familiar background (10 × rating freebies)

### Freebie Points by Context

| Context | Freebies |
|---------|----------|
| Familiar as standalone PC | 25 |
| Familiar background ● | 10 |
| Familiar background ●● | 20 |
| Familiar background ●●● | 30 |
| Familiar background ●●●● | 40 |
| Familiar background ●●●●● | 50 |

When invoked from mage character creation:
- Use 10 × Background rating for freebies
- Must establish bond with the mage character
- Link familiar document from character sheet

## What is a Familiar?

Familiars are spirits inhabiting material bodies to aid mages. They:
- Are spirits in physical forms (animal, construct, object, etc.)
- Must be bonded to a mage
- Have Essence and Spirit Charms
- Share mystical connection with their mage

## Required Traits (All Familiars)

| Trait | Type | Cost/Value |
|-------|------|------------|
| **Bond-Sharing** | Advantage | 4/5/6 pts |
| **Paradox Nullification** | Advantage | 2-6 pts |
| **Thaumivore** | Flaw | 5 pts |

**Common additions**: Human Speech (1 pt), Spirit Travel (8/10/15 pts)

**Lookup**: `python scripts/lookup.py companion.special-advantages special-advantages "Bond-Sharing"`

## Creation Steps

### Step 1: Character Concept
- Spirit type and form
- Origin (summoned, volunteered, bound)
- Bond relationship
- Nature and Demeanor

### Step 2: Physical Form

| Form | Notes |
|------|-------|
| **Animal** | Cat, raven, snake — most traditional |
| **Construct** | Golem, homunculus |
| **Object** | Enchanted skull, talking sword |
| **Robot** | AI-imbued machine (Technocratic) |
| **Reanimate** | Animated corpse |
| **Bygone** | Mythical creature (dragon, griffin) — requires Unbelief |

### Step 3: Attributes (6/4/3)
Physical traits may be modified by form.

### Step 4: Abilities (11/7/4)
Cap: 4 dots starting.

### Step 5: Backgrounds
5 dots (cap 4 per background). Common: Arcane, Mentor, Library, Contacts.

### Step 6: Willpower and Essence
- **Willpower**: 3
- **Essence**: Willpower × 5

### Step 7: Required Advantages

**Bond-Sharing (4-6 pts)** — REQUIRED
- 4 pts: Emotional bond, sense general state
- 5 pts: Share senses, telepathy at close range
- 6 pts: Full telepathic bond any distance, share Quintessence/Essence

**Paradox Nullification (2-6 pts)** — REQUIRED
- 2 pts: 1 Paradox/scene
- 3 pts: 2/scene
- 4 pts: 3/scene
- 5 pts: 4/scene
- 6 pts: 5/scene

### Step 8: Required Flaw

**Thaumivore (5 pts)** — REQUIRED
Feeds on magical energy. Must be near active magic or Quintessence regularly.

### Step 9: Form-Based Traits

**Animal Forms**: Animal (2), No Dexterous Limbs (4), Human Speech (1), Nightsight (3), natural weapons

**Construct Forms**: Soak Lethal (3), Armor, Unaging (5)

**Bygone Forms**: MUST have Unbelief (3/5/8) unless in protected Realm

### Step 10: Spirit Charms

**Costs**: 1 freebie per Essence to activate; 5 freebies if always-on/variable/luck-based

**Lookup**: `python scripts/lookup.py companion.spirit-charms spirit-charms --keys`

Common Charms:
| Charm | Cost | Effect |
|-------|------|--------|
| Airt Sense | Free | Navigate spirit ways |
| Disorient | 1 | Confuse target's location sense |
| Bargain | 2 | +2 diff to mage's binding rolls |
| Smoke Screen | 2 | Create concealing fog |
| Bad Luck Curse | 5 | Turn successes into 1s |
| Good Luck Charm | 5 | Grant reroll to ally |
| Spirit Gossip | 5 | Gather info from spirits |
| Jack In | 5 | Interface with electronics |

### Step 11: Freebie Points

**Familiar as PC**: 25 freebies  
**Familiar for PC**: 10 × Familiar background rating

| Trait | Cost |
|-------|------|
| Attribute | 5 per dot |
| Ability | 2 per dot |
| Background | 1 per dot |
| Willpower | 2 per dot |
| Essence | 1 per dot |
| Special Advantage | As listed |
| Charm | 1/Essence or 5 pts |
| Merit | As listed |
| Flaw | Gives bonus |

---

## The Mage-Familiar Bond

1. How did the bond form?
2. What does each get from the relationship?
3. How equal is the relationship?
4. What happens if the mage mistreats the familiar?
5. What are the familiar's independent goals?

**Bond Mechanics**:
- Cannot exist in material world without a mage bond
- Breaking bond may destroy or exile familiar
- If mage dies, familiar must find new mage or fade

---

## Form-Specific Guidelines

### Animal Familiars
Use templates from Mage 20 pp. 618-620 or Gods & Monsters pp. 103-107.

### Construct Familiars
Purpose-built. Abilities match function.

### Object Familiars
Typically require mage to carry/use them. Flaws: Limbless.

### Bygone Familiars
**REQUIRED**: Unbelief (3/5/8). Cannot survive long in mundane reality.

---

## Validation Checklist

- [ ] Attributes: 13 dots (6/4/3)
- [ ] Abilities: 22 dots (11/7/4)
- [ ] Backgrounds: 5 dots
- [ ] Willpower: 3
- [ ] Essence: Willpower × 5
- [ ] Bond-Sharing: Purchased (REQUIRED)
- [ ] Paradox Nullification: Purchased (REQUIRED)
- [ ] Thaumivore: Taken (REQUIRED)
- [ ] Flaws ≤ 7 pts (not counting required Thaumivore)
- [ ] Freebie points spent exactly (25 if PC, 10 × rating if for mage's background)
- [ ] Charms suit spirit nature
- [ ] Bond to mage defined

---

## Output Template

```markdown
# [Familiar Name]

**Spirit Type**: [Element/Concept/Ancestor/etc.]  
**Physical Form**: [Animal/Construct/Object/etc.]  
**Nature**: [Archetype]  
**Demeanor**: [Archetype]  
**Bonded Mage**: [Name or description]  

## Attributes

### Physical
Strength ●○○○○ | Dexterity ●○○○○ | Stamina ●○○○○

### Social
Charisma ●○○○○ | Manipulation ●○○○○ | Appearance ●○○○○

### Mental
Perception ●○○○○ | Intelligence ●○○○○ | Wits ●○○○○

## Abilities

### Talents
[List]

### Skills
[List]

### Knowledges
[List]

## Backgrounds
[List]

## Advantages

### Special Advantages
- Bond-Sharing (● pts)
- Paradox Nullification (● pts)
- [Others]

### Spirit Charms
- Airt Sense (Free)
- [Others with costs]

### Merits
[If any]

### Flaws
- Thaumivore (5 pts) — REQUIRED
- [Others]

## Spirit Traits
**Willpower**: ●●●○○○○○○○  
**Essence**: ●●●●● ●●●●● ●●●●●  
**Health**: [ ] [ ] [ ] [ ] [ ] [ ] [ ]

## Physical Form
[Description of body]

## Spirit Nature
[True essence — what it embodies]

## The Bond
[Relationship with mage, how formed]

## History
[Origin, how became familiar]

## Personality
[How they think, quirks]
```
