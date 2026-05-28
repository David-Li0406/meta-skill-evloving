# Character Sheet Output Template

Standard format for M20 character documents.

## Full Character Sheet Format

```markdown
# [Character Name]

**Concept**: [Brief concept phrase]
**Faction**: [Tradition/Convention/Craft]
**Subfaction**: [House/Methodology/Path, if any]
**Nature**: [Archetype]
**Demeanor**: [Archetype]

## Description

[2-4 sentences describing physical appearance, typical dress, and notable mannerisms]

---

## Attributes

### Physical
- **Strength**: ●●○○○ [Specialty if 4+]
- **Dexterity**: ●●●○○
- **Stamina**: ●●○○○

### Social
- **Charisma**: ●●●○○
- **Manipulation**: ●●○○○
- **Appearance**: ●●○○○

### Mental
- **Perception**: ●●●○○
- **Intelligence**: ●●●●○ (Specialty: [Name])
- **Wits**: ●●●○○

---

## Abilities

### Talents
- Alertness ●●○○○
- Awareness ●●●○○
- [etc.]

### Skills
- Crafts ●●○○○
- [etc.]

### Knowledges
- Academics ●●●○○
- Occult ●●●●○ (Specialty: [Name])
- [etc.]

---

## Backgrounds

| Background | Rating | Description |
|------------|--------|-------------|
| Avatar | ●●●○○ | [Brief description or link] |
| Library | ●●○○○ | [Link to Library document if created] |
| Node | ●○○○○ | [Link to Node document if created] |
| [etc.] | | |

---

## Spheres

**Affinity**: [Sphere Name] ([Faction/Subfaction])

| Sphere | Rating | Notes |
|--------|--------|-------|
| [Affinity] | ●●○○○ | Affinity Sphere |
| Correspondence | ●○○○○ | |
| [etc.] | | |

---

## Focus

### Paradigm
[Paradigm name and brief explanation of worldview]

### Practices
- [Practice 1]: [Brief description of how used]
- [Practice 2]: [Brief description]

### Instruments (7 minimum)
1. [Instrument] - [How used]
2. [Instrument] - [How used]
3. [Instrument] - [How used]
4. [Instrument] - [How used]
5. [Instrument] - [How used]
6. [Instrument] - [How used]
7. [Instrument] - [How used]

---

## Resonance

**[Adjective] [Rating]**: [Brief description of how the character's magic feels/manifests]

---

## Starting Rotes

| Rote | Spheres | Practice | Effect |
|------|---------|----------|--------|
| [Name] | [Sphere N, Sphere N] | [Practice] | [Brief description] |
| [Name] | [Sphere N] | [Practice] | [Brief description] |

**Total Sphere Dots**: [N] (6 base + [N] from freebies + [N] from XP)

---

## Merits & Flaws

### Merits
| Merit | Cost | Description |
|-------|------|-------------|
| [Name] | [N] | [Brief description] |

### Flaws
| Flaw | Points | Description |
|------|--------|-------------|
| [Name] | [N] | [Brief description] |

---

## Derived Statistics

- **Willpower**: ●●●●●●○○○○ (6)
- **Quintessence**: [N] (max [Avatar] without Prime 1)
- **Paradox**: 0
- **Health**: ○○○○○○○ (7 levels)
- **Arete**: ●●○○○ (2)

---

## Point Audit

### Base Allocation
| Category | Allocated | Required |
|----------|-----------|----------|
| Attributes (Primary) | [N] | 7 |
| Attributes (Secondary) | [N] | 5 |
| Attributes (Tertiary) | [N] | 3 |
| Abilities (Primary) | [N] | 13 |
| Abilities (Secondary) | [N] | 9 |
| Abilities (Tertiary) | [N] | 5 |
| Backgrounds | [N] | 7 |
| Spheres | [N] | 5 |
| Arete | 1 | 1 |
| Willpower | 5 | 5 |
| Affinity (free) | 1 | 1 |

### Freebies
| Source | Points |
|--------|--------|
| Base | 15 |
| Flaws | +[N] |
| **Total Available** | [N] |

| Expenditure | Cost Each | Qty | Total |
|-------------|-----------|-----|-------|
| Attribute dots | 5 | [N] | [N] |
| Ability dots | 2 | [N] | [N] |
| Background dots | 1 | [N] | [N] |
| Willpower dots | 1 | [N] | [N] |
| Sphere dots | 7 | [N] | [N] |
| Arete dots | 4 | [N] | [N] |
| Merits | varies | - | [N] |
| **Total Spent** | | | [N] |

**Remaining**: [N] (must be 0)

### Validation Checklist
- [ ] Attribute totals correct (7/5/3 + freebies)
- [ ] Ability totals correct (13/9/5 + freebies)
- [ ] No Ability > 3 without freebies
- [ ] Background total correct (7 + freebies, accounting for multipliers)
- [ ] Sphere total correct (5 base + 1 affinity free + freebies)
- [ ] No Sphere > Arete
- [ ] All 4+ traits have specialties
- [ ] 7+ instruments defined
- [ ] Paradigm defined
- [ ] At least 1 Practice defined
- [ ] Exactly 1 Resonance trait with rating 1-5
- [ ] Starting rotes total 6 Sphere dots (+ freebie/XP purchases)
- [ ] All rotes use only Spheres character possesses
- [ ] Affinity matches faction/subfaction
- [ ] Freebie math balances (spent = available)
- [ ] Flaw points ≤ 7

---

## Character Notes

[Background, history, goals, relationships, or other narrative information]
```

## Compact NPC Format

For NPCs, use abbreviated format:

```markdown
# [Name] ([Faction])

**Concept**: [Phrase] | **Nature/Demeanor**: [N]/[D] | **Arete**: [N]

**Attributes**: Str [N], Dex [N], Sta [N] | Cha [N], Man [N], App [N] | Per [N], Int [N], Wit [N]

**Key Abilities**: [Ability] [N], [Ability] [N], [Ability] [N]

**Spheres**: [Sphere] [N], [Sphere] [N] (Affinity: [Sphere])

**Backgrounds**: [Background] [N], [Background] [N]

**Willpower**: [N] | **Quintessence**: [N] | **Health**: [N]

**Resonance**: [Adjective] [N]

**Focus**: [Paradigm] via [Practice] using [key instruments]

**Signature Rotes**: [Rote Name] ([Spheres]), [Rote Name] ([Spheres])

**Notes**: [Brief description and role]
```

## Linked Documents

When backgrounds reference other creators, use:

```markdown
| Background | Rating | Document |
|------------|--------|----------|
| Library | ●●○○○ | [The Cerulean Archive](./libraries/cerulean_archive.md) |
| Node | ●●●○○ | [Whisperwind Glade](./nodes/whisperwind_glade.md) |
| Sanctum | ●●○○○ | [The Painted Room](./sanctums/painted_room.md) |
| Wonder | ●○○○○ | [Compass of the Lost](./wonders/compass_lost.md) |
```
