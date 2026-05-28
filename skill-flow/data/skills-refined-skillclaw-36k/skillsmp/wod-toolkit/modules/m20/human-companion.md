# Human Companion Module

Create human (or mostly human) companion characters: acolytes, consors, retainers, cultists, Wards, contacts, backup agents, and other mortals who associate with mages.

## Invoked By

This module is called when creating:
- **Mage PCs** with Allies, Retainers, Cult, Spies, or Backup backgrounds
- **Sorcerer PCs** with Allies or Retainers backgrounds
- **Chantries** or **Constructs** with mortal staff

When invoked from character creation, create 1-2 representative companions based on background rating:

| Background Rating | Companions to Create |
|-------------------|---------------------|
| 1-2 | 1 representative NPC |
| 3-4 | 2 representative NPCs |
| 5 | 2-3 representative NPCs |

## Character Subtypes

| Type | Freebie Points | Notes |
|------|----------------|-------|
| **Acolyte** | 15 | Cult member, assistant, cultist, servant |
| **Backup Agent** | 15 | Technocratic employee, field operative |
| **Consor** | 21 | Skilled ally, professional, lover, trusted confidant |
| **Other Skilled Ally** | 21 | Hedge wizard, hunter, night-folk contact |

## Creation Steps

### Step 1: Character Concept
- **Concept**: Who were you before you encountered mages?
- **Motivation**: Why'd you get involved with them?
- **Affiliation**: Traditions, Technocracy, Disparates, Marauders, Nephandi, or none?
- **Type**: Acolyte, consor, hedge wizard, retainer, cultist?
- **Nature and Demeanor**: What's your personality?

### Step 2: Attributes (6/4/3)
| Category | Dots |
|----------|------|
| Primary | 6 |
| Secondary | 4 |
| Tertiary | 3 |

### Step 3: Abilities (11/7/4)
| Category | Dots |
|----------|------|
| Primary | 11 |
| Secondary | 7 |
| Tertiary | 4 |

**Cap**: Starting abilities capped at 4 dots.

### Step 4: Backgrounds
- **Base**: 5 dots (cap 4 per background)
- **Consors**: Must have at least 1 dot in Mentor

### Step 5: Willpower
- **Base**: 3

### Step 6: Merits, Flaws, and Advantages
Human companions may have:
- Standard Merits & Flaws (Mage 20 / Book of Secrets)
- Companion-specific Merits & Flaws (lookup: `lookup.py companion.companion-merits companion-merits`, `lookup.py companion.companion-flaws companion-flaws`)
- Special Advantages (rare — requires justification)

**Typically Do Not Have**: Spirit Charms, Essence, overtly supernatural Special Advantages

### Step 7: Freebie Points
| Trait | Cost |
|-------|------|
| Attribute | 5 per dot |
| Ability | 2 per dot |
| Background | 1 per dot |
| Willpower | 2 per dot |
| Merit | As listed |
| Flaw | Gives bonus |
| Special Advantage | As listed |

### Step 8: Finishing Touches
- Health Levels, Specialties (required for 4+ traits)
- Description, Equipment

---

## Companion Roles

| Role | Common Abilities |
|------|------------------|
| **Assistants** | Academics, Computer, Investigation, Science |
| **Backup** | Athletics, Brawl, Firearms, Melee |
| **Cleaners** | Streetwise, Subterfuge, Larceny, Politics |
| **Cultists** | Lore, Occult, Expression, Empathy |
| **Handlers** | Bureaucracy, Finance, Etiquette, Leadership |
| **Igors** | Medicine, Science, Crafts, Technology |
| **Lovers** | Empathy, Expression, Subterfuge |
| **Professionals** | Academics, Law, Medicine, Finance |
| **Servants** | Etiquette, Alertness, Stealth, Crafts |

---

## Companion-Specific Merits

### Alpha (2 pts)
+2 dice to Leadership and contested Social rolls for dominance.

### My Master is My Slave (5 pts)
+2 dice on Manipulation vs associated mage; they have +1 difficulty resisting.

## Companion-Specific Flaws

### Beta (1 pt)
+1 difficulty to resist commands; -1 die to Leadership in groups.

### Broken (5 pts)
Cannot spend Willpower to resist commands from authority figures.

### Omega (4 pts)
-2 dice on all Social rolls in group settings.

---

## Special Human Types

### Hedge Wizards
May have Numina or Paths (see `modules/sorcerer.md`). Subject to Paradox.

### Psychics
May have Psychic Phenomena (see `modules/psychic.md`).

### Hunters
May have True Faith or Numina, special equipment.

---

## Relationship Questions

1. How did you meet your mage?
2. What do you get out of this arrangement?
3. Does your mage treat you as an equal?
4. Do you have an exit strategy?
5. Do you pursue magic yourself?
6. What do your friends/family think?
7. Have you witnessed vulgar magic?
8. Would you betray your mage?

---

## Validation Checklist

- [ ] Attributes: 13 dots (6/4/3)
- [ ] Abilities: 22 dots (11/7/4)
- [ ] No starting Ability > 4
- [ ] Backgrounds: 5 dots (cap 4)
- [ ] Consors have Mentor 1+
- [ ] Willpower: 3
- [ ] Flaws ≤ 7 points
- [ ] Freebie points spent exactly (15 or 21)

---

## Output Template

```markdown
# [Character Name]

**Concept**: [One-line]  
**Nature**: [Archetype]  
**Demeanor**: [Archetype]  
**Affiliation**: [Traditions/Technocracy/etc.]  
**Type**: [Acolyte/Consor/etc.]  

## Attributes

### Physical
Strength ●○○○○ | Dexterity ●○○○○ | Stamina ●○○○○

### Social
Charisma ●○○○○ | Manipulation ●○○○○ | Appearance ●○○○○

### Mental
Perception ●○○○○ | Intelligence ●○○○○ | Wits ●○○○○

## Abilities

### Talents
[List with ratings]

### Skills
[List with ratings]

### Knowledges
[List with ratings]

## Backgrounds
[List with ratings]

## Advantages

### Merits
[List with costs]

### Flaws
[List with values]

## Other Traits
**Willpower**: ●●●○○○○○○○  
**Health**: [ ] [ ] [ ] [ ] [ ] [ ] [ ]

## Description
[Physical appearance, mannerisms, personality]

## Background
[History and relationship to magical world]

## Relationship to Mage(s)
[Who they serve, how they met, nature of bond]
```
