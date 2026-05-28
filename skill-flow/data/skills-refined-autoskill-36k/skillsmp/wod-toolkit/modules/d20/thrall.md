# Thrall Module

Create pact-bound mortal servants.

## Overview

Thralls are mortals bound to a demon through a pact. They provide Faith in exchange for supernatural benefits.

**Key Distinctions**:
- **Thrall**: Mortal bound by formal pact; provides regular Faith
- **Follower**: Worshipper without formal pact; provides less reliable Faith
- **Believer**: Mortal with faith in the demon but no formal relationship

---

## Creation Steps

1. **Concept** — Who was this mortal before the pact?
2. **What they wanted** — What desire made them vulnerable?
3. **The pact terms** — What did demon offer? What does mortal owe?
4. **Nature & Demeanor** — From `lookup.py shared.core archetypes`
5. **Attributes** — 6/4/3 (+ 9 base)
6. **Abilities** — 11/7/4 (cap 3)
7. **Backgrounds** — 5 dots
8. **Virtues** — 7 dots (+ 3 base)
9. **Willpower** — Sum of two highest Virtues
10. **Merits & Flaws** — Flaws ≤ 7
11. **Empowerment** — If demon has granted supernatural abilities
12. **Freebies** — 21 + Flaws - Merits
13. **Pact Document** — Create linked pact document
14. **Validate**

---

## Attributes

| Category | Allocation |
|----------|------------|
| Primary | 6 dots |
| Secondary | 4 dots |
| Tertiary | 3 dots |
| Base | +1 each (9 total) |

---

## Abilities

Standard D20 Ability list (11/11/11).

| Category | Allocation |
|----------|------------|
| Primary | 11 dots |
| Secondary | 7 dots |
| Tertiary | 4 dots |
| Cap | 3 at creation |

---

## Backgrounds

Thralls receive 5 Background dots. Common choices:

| Background | Use |
|------------|-----|
| Allies | Friends and associates |
| Contacts | Information sources |
| Influence | Pull in mortal society |
| Resources | Wealth |
| Status | Position in organization |

**Note**: Thralls do not have demon-specific Backgrounds (Eminence, Pacts, Legacy).

---

## Virtues

Thralls use the same Virtues as demons:

| Virtue | Governs |
|--------|---------|
| Conscience | Moral compass |
| Conviction | Strength of belief |
| Courage | Facing fear |

**Willpower** = Sum of two highest Virtues

---

## The Pact

Every thrall is bound by a pact. See `modules/d20/pact.md` for full pact creation rules.

### Common Pact Terms

**What Demons Offer**:
- Healing or health
- Wealth or success
- Knowledge or skills
- Protection
- Revenge
- Love or beauty
- Power or influence

**What Mortals Owe**:
- Regular worship (provides Faith)
- Service (tasks, missions)
- Recruitment (bring others)
- Sacrifice (resources, relationships)
- Soul claim (upon death)

---

## Empowered Thralls

Demons can invest Faith into thralls, granting supernatural abilities.

### Empowerment Costs

| Ability | Faith Cost | Effect |
|---------|------------|--------|
| Enhanced Attribute | 1 per +1 | Permanent Attribute increase |
| Enhanced Ability | 1 per +2 | Permanent Ability increase |
| Immunity | 2 | Immunity to one harm type |
| Special Sense | 1 | Supernatural perception |
| Minor Power | 2 | Limited supernatural ability |
| Major Power | 4 | Significant supernatural ability |

**Invested Faith**:
- Remains committed to the thrall
- Cannot be used by demon for other purposes
- Returns if thrall dies or pact is broken
- Thrall may lose powers if Faith is withdrawn

---

## Faith Harvesting

Thralls provide Faith to their demon masters:

| Method | Faith Gained | Notes |
|--------|--------------|-------|
| Daily worship | 1 per week | Reliable, passive |
| Active service | 1 per significant task | Requires direction |
| Sacrifice | 1-3 per sacrifice | Depends on sacrifice value |
| Reaping | 1-3 | Drains thrall; risky |

**Reaping**: Forcibly taking Faith. Causes harm and may damage the pact relationship.

---

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 |
| Virtue | 2 |
| Willpower | 1 |

---

## Validation

- [ ] Attributes: 13 dots (+ 9 base = 22 total)
- [ ] Abilities: 22 dots, none > 3
- [ ] Backgrounds: 5 dots
- [ ] Virtues: 10 total (7 + 3 base)
- [ ] Willpower: Sum of two highest Virtues
- [ ] Flaws ≤ 7 points
- [ ] Freebies spent exactly
- [ ] Pact document created and linked
- [ ] Empowerments documented (if any)

---

## Output Template

```markdown
# [Thrall Name]

**Concept**: [Brief concept]
**Bound To**: [Demon name]
**Pact Date**: [When pact was made]

## Before the Pact

[Who was this person? What did they want?]

## The Bargain

**What They Wanted**: [The desire that drove them]
**What Was Offered**: [What the demon promised]
**What They Owe**: [Their obligations]

## Personality

**Nature**: [Archetype]
**Demeanor**: [Archetype]

## Attributes

### Physical
| Attribute | Rating |
|-----------|--------|
| Strength | ●●○○○ |
| Dexterity | ●●○○○ |
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
| Perception | ●●○○○ |
| Intelligence | ●●○○○ |
| Wits | ●●○○○ |

## Abilities

### Talents
| Ability | Rating |
|---------|--------|
| [Ability] | ●●○○○ |

### Skills
| Ability | Rating |
|---------|--------|
| [Ability] | ●●○○○ |

### Knowledges
| Ability | Rating |
|---------|--------|
| [Ability] | ●●○○○ |

## Backgrounds

| Background | Rating | Details |
|------------|--------|---------|
| [Background] | ●●○○○ | [Description] |

## Virtues

| Trait | Rating |
|-------|--------|
| Conscience | ●●○○○ |
| Conviction | ●●○○○ |
| Courage | ●●○○○ |

## Secondary Traits

| Trait | Value |
|-------|-------|
| Willpower | ●●●●●○○○○○ |
| Health | ○○○○○○○ |

## Empowerments

| Power | Faith Invested | Effect |
|-------|----------------|--------|
| [Power] | [N] | [Description] |

## Merits & Flaws

| Merit/Flaw | Points | Description |
|------------|--------|-------------|
| [Name] | [+/-N] | [Brief description] |

## Description

[Physical appearance, mannerisms]

## Relationship with Master

[How do they view the demon? Loyal? Fearful? Resentful?]

## Pact Document

[Link to full pact document]
```
