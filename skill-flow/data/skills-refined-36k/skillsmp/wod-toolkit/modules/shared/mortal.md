# Shared Mortal Module

Create base mortal characters for any World of Darkness game.

## Scope

This module covers **base mortal creation only**:
- Attributes, Abilities, Backgrounds
- Merits & Flaws
- Willpower

For game-specific mortal-adjacent types, use the appropriate game module:
- **V20**: `modules/v20/ghoul.md`, `modules/v20/revenant.md`
- **W20**: `modules/w20/kinfolk.md`, `modules/w20/fomor.md`
- **M20**: `modules/m20/sorcerer.md`, `modules/m20/human-companion.md`
- **Wr20**: `modules/wr20/medium.md`, `modules/wr20/ghost-hunter.md`
- **C20**: `modules/c20/kinain.md`

---

## Mortal Character Creation

### Standard Allocation
| Category | Dots |
|----------|------|
| Attributes | 6/4/3 (+ 9 base) |
| Abilities | 11/7/4 (cap 3 at creation) |
| Backgrounds | 5 |
| Willpower | 3-5 (varies by concept) |
| Freebies | 21 |

### Freebie Costs
| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 |
| Willpower | 1 |
| Merit | As listed |

---

## Step-by-Step Creation

### 1. Concept
- **Who were they before?** Occupation, social status, family
- **What drives them?** Goals, fears, desires
- **How do they relate to the supernatural?** Aware? Ignorant? Seeking?

### 2. Attributes
Prioritize Physical, Social, Mental as Primary (6), Secondary (4), Tertiary (3).
Add 1 free dot to each Attribute (9 total base).

**Reference**: `lookup.py shared.core attributes`

### 3. Abilities
Prioritize Talents, Skills, Knowledges as Primary (11), Secondary (7), Tertiary (4).
No Ability above 3 at creation without freebies.

**Reference**: `lookup.py shared.core abilities-primary`

### 4. Backgrounds
5 dots among:
- Allies, Contacts, Fame, Influence, Mentor, Resources, Retainers, Status

**Reference**: `lookup.py shared.core backgrounds-universal`

Game-specific backgrounds may be available (check game overview).

### 5. Nature & Demeanor
Select from shared archetypes.

**Reference**: `lookup.py shared.core archetypes`

### 6. Willpower
Base Willpower 3-5 depending on concept:
- 3: Average person
- 4: Strong-willed
- 5: Exceptional determination

### 7. Freebies (21 points)
Spend on any traits. Consider:
- Raising key Abilities above 3
- Adding Willpower
- Purchasing Merits
- Additional Backgrounds

### 8. Merits & Flaws (Optional)
Up to 7 points of Flaws, balanced by Merits.
Check game-specific merits-flaws files for options.

---

## Common Mortal Archetypes

### The Investigator
Attributes: Mental primary
Key Abilities: Investigation, Alertness, Academics, Computer
Backgrounds: Contacts, Resources
Concept: Detective, journalist, researcher

### The Professional
Attributes: Social or Mental primary
Key Abilities: Finance, Law, Politics, Etiquette
Backgrounds: Resources, Influence, Contacts
Concept: Lawyer, doctor, executive

### The Street-Smart
Attributes: Physical or Social primary
Key Abilities: Streetwise, Brawl, Subterfuge, Larceny
Backgrounds: Contacts, Allies
Concept: Criminal, hustler, survivor

### The Academic
Attributes: Mental primary
Key Abilities: Academics, Occult, Science, Investigation
Backgrounds: Resources, Mentor, Library (if available)
Concept: Professor, occultist, student

### The Protector
Attributes: Physical primary
Key Abilities: Brawl, Firearms, Athletics, Alertness
Backgrounds: Allies, Resources
Concept: Bodyguard, police officer, soldier

---

## Supernatural Awareness

Mortals may have varying levels of awareness:

| Level | Description |
|-------|-------------|
| **Ignorant** | Knows nothing of the supernatural |
| **Skeptic** | Has encountered but rationalizes away |
| **Aware** | Knows supernatural exists, limited knowledge |
| **Knowledgeable** | Understands specific supernatural types |
| **Hunter** | Actively opposes or investigates supernatural |

The **Awareness** Talent represents instinctive reaction to supernatural presence.

---

## Mortal Vulnerabilities

Mortals lack supernatural resilience:
- **Health**: 7 health levels (no regeneration)
- **Damage**: No special damage resistance
- **Mental**: Vulnerable to supernatural mental powers
- **Aging**: Subject to normal mortality

---

## Advancement to Supernatural

Mortals may become supernatural through:
- **V20**: Embrace (vampire), Ghouling
- **W20**: First Change (if Kinfolk with dormant gene)
- **M20**: Awakening (rare), Sorcerous training
- **Wr20**: Death (becoming wraith)
- **C20**: Chrysalis (if Kinain with strong fae blood)

---

## Output Template

```markdown
# [Character Name]

**Concept**: [Brief description]  
**Nature**: [Archetype]  
**Demeanor**: [Archetype]  
**Supernatural Awareness**: [Level]

## Attributes

### Physical
| Attribute | Rating |
|-----------|--------|
| Strength | ●●○○○ |
| Dexterity | ●●●○○ |
| Stamina | ●●○○○ |

### Social
| Attribute | Rating |
|-----------|--------|
| Charisma | ●●○○○ |
| Manipulation | ●●○○○ |
| Appearance | ●●○○○ |

### Mental
| Attribute | Rating |
|-----------|--------|
| Perception | ●●●○○ |
| Intelligence | ●●●○○ |
| Wits | ●●○○○ |

## Abilities

### Talents
[List with ratings]

### Skills
[List with ratings]

### Knowledges
[List with ratings]

## Backgrounds
[List with ratings]

## Other Traits
**Willpower**: ●●●●○○○○○○  
**Health**: ○○○○○○○

## Merits & Flaws
[If any]

## Description
[Physical appearance, personality, history]

## Notes
[Relationships, goals, hooks for supernatural involvement]
```

---

## Validation Checklist

- [ ] Attributes: 6/4/3 distributed correctly (+ 9 base)
- [ ] Abilities: 11/7/4 distributed correctly
- [ ] No Ability above 3 without freebies
- [ ] Backgrounds: 5 dots
- [ ] Willpower: 3-5
- [ ] Freebies: 21 points spent correctly
- [ ] Flaws balanced by Merits (max 7 Flaw points)
- [ ] Nature and Demeanor selected
- [ ] Concept clear and playable
