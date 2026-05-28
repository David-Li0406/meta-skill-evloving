# Character Module — Demon

Create mechanically valid Demon characters for D20.

## PC vs NPC

| Type | Linked Documents | When |
|------|------------------|------|
| **PC** (default) | REQUIRED | Standard creation |
| **NPC** | Not required | "NPC", "quick", "simple", "stat block" |

## Dependencies (PC Only)

**Read `modules/d20/background-expansion.md` for the complete background → module mapping.**

| Background | Action |
|------------|--------|
| Allies, Mentor | Create NPC document(s) |
| Followers | Create follower document(s) |
| Pacts | Read `modules/d20/pact.md`, create pact document(s) |
| Eminence | Note position in demon hierarchy |

**DO NOT create a PC with backgrounds as one-line summaries.**

## Creation Steps

1. **PC/NPC** — Default PC
2. **Concept** — Name, House, Faction, Concept
3. **Mortal Host** — Who was the human before possession?
4. **Celestial Identity** — Pre-Fall name, role, and rebellion history
5. **Nature & Demeanor** — From `lookup.py shared.core archetypes`
6. **Attributes** — 7/5/3 across Physical/Social/Mental (+ 1 base each)
7. **Abilities** — 13/9/5 across Talents/Skills/Knowledges (cap 3)
8. **Lore** — 3 dots in House Lore and/or Common Lore
9. **Backgrounds** — 5 dots. Note which need sub-documents
10. **Virtues** — 7 dots (+ 1 base each in Conscience, Conviction, Courage)
11. **Faith** — Starts at 3
12. **Torment** — By House (Devils-Defilers: 3, Devourers-Slayers: 4)
13. **Willpower** — Sum of two highest Virtues
14. **Merits & Flaws** — From `lookup.py d20.character merits-flaws`. Flaws ≤ 7
15. **Apocalyptic Form** — One Visage determined by primary lore; record 4 low-Torment traits
16. **⛔ BACKGROUNDS (PC)** — Create documents for Allies/Followers/Pacts
17. **Freebies** — 15 + Flaws - Merits. Spend exactly.
18. **Specialties** — Required for 4+ traits
19. **Description** — Mortal appearance, mannerisms; apocalyptic form appearance
20. **Validate**

---

## House Selection

When choosing a House, consult the detailed references:

```bash
# Get House details
python scripts/lookup.py d20.character houses "Scourges"

# Search for Houses by Lore
python scripts/lookup.py d20.character houses --find "Awakening"
```

### House Overview

| House | Role | Primary Lore | Starting Torment |
|-------|------|--------------|------------------|
| Devils (1st) | Leadership, inspiration | Flame, Radiance | 3 |
| Scourges (2nd) | Protection, destruction | Awakening, Firmament, Winds | 3 |
| Malefactors (3rd) | Creation, crafting | Earth, Forge, Paths | 3 |
| Fiends (4th) | Knowledge, fate | Light, Patterns, Portals | 3 |
| Defilers (5th) | Desire, inspiration | Longing, Storms, Transfiguration | 3 |
| Devourers (6th) | Nature, predation | Beast, Flesh, Wild | 4 |
| Slayers (7th) | Death, souls | Death, Spirit, Realms | 4 |

---

## Faction Selection

Factions represent ideological allegiance, not organizational membership.

| Faction | Philosophy | Common Houses |
|---------|------------|---------------|
| Faustian | Humanity is the key to power | Devils, Defilers, Malefactors |
| Cryptic | The truth must be discovered | Fiends, any |
| Luciferan | Find Lucifer, resume the war | Devourers, Devils |
| Reconciler | Seek peace with God | Scourges, Slayers |
| Ravener | Creation must be destroyed | Devourers, any |

---

## Abilities (D20 Standard)

### Talents (11)
| Ability | Description |
|---------|-------------|
| Alertness | Noticing things |
| Athletics | Physical feats, **includes dodging** |
| Awareness | Supernatural perception |
| Brawl | Unarmed combat |
| Empathy | Reading emotions |
| Expression | Communication |
| Intimidation | Coercion through fear |
| Intuition | Gut feelings, hunches |
| Leadership | Commanding others |
| Streetwise | Urban survival |
| Subterfuge | Deception |

### Skills (11)
| Ability | Description |
|---------|-------------|
| Animal Ken | Animal handling |
| Crafts | Creating objects |
| Drive | Vehicle operation |
| Etiquette | Social graces |
| Firearms | Ranged weapons |
| Larceny | Security systems, theft |
| Melee | Armed combat |
| Performance | Entertainment |
| Stealth | Hiding, sneaking |
| Survival | Wilderness/urban survival |
| Technology | Modern devices |

### Knowledges (11)
| Ability | Description |
|---------|-------------|
| Academics | Liberal arts |
| Computer | Digital systems |
| Finance | Money, economics |
| Investigation | Finding clues |
| Law | Legal systems |
| Medicine | Healing |
| Occult | Supernatural lore |
| Politics | Political systems |
| Religion | Theology, faiths |
| Research | Archives, databases |
| Science | Physical sciences |

---

## Lore

Characters begin with 3 dots distributed among House Lore and/or Common Lore.

### Common Lore (All Houses)
- Lore of the Celestials
- Lore of the Fundament  
- Lore of Humanity

### House Lore
| House | Available Lore |
|-------|----------------|
| Devils | Flame, Radiance, (Celestials) |
| Scourges | Awakening, Firmament, Winds |
| Malefactors | Earth, Forge, Paths |
| Fiends | Light, Patterns, Portals |
| Defilers | Longing, Storms, Transfiguration |
| Devourers | Beast, Flesh, Wild |
| Slayers | Death, Spirit, Realms |

**Learning other Houses' Lore** requires finding a teacher and spending experience. This is difficult and often requires significant story justification.

---

## Virtues

Demons use these three Virtues:

| Virtue | Governs |
|--------|---------|
| Conscience | Moral compass, resisting cruelty |
| Conviction | Strength of belief, resisting doubt |
| Courage | Facing fear, taking action |

**Willpower** = Sum of two highest Virtues

---

## Faith & Torment

### Faith
- Starting Faith: **3**
- Maximum Faith: **10**
- Faith powers evocations and innate abilities
- Faith can be spent for automatic successes
- Faith is regained through worship, pacts, and reaping

### Torment
- Starting Torment: **By House** (3 or 4)
- Maximum Torment: **10**
- High Torment corrupts evocations
- Torment 7+ triggers high-Torment apocalyptic form
- Torment 10 = near-Earthbound state

---

## Allocation Summary

| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Lore | 3 (House + Common) |
| Backgrounds | 5 |
| Virtues | 7 (+ 3 base) |
| Faith | 3 (starting) |
| Torment | By House |
| Willpower | Two highest Virtues |
| Freebies | 15 |

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 |
| Lore | 7 |
| Virtue | 2 |
| Faith | 6 |
| Willpower | 1 |

---

## Reference Data

```bash
# House details
python scripts/lookup.py d20.character houses "Devils"

# Faction details
python scripts/lookup.py d20.character factions "Faustian"

# Archetypes for Nature/Demeanor
python scripts/lookup.py shared.core archetypes "Visionary"

# Abilities
python scripts/lookup.py shared.core abilities "Awareness"

# Backgrounds
python scripts/lookup.py d20.character backgrounds "Eminence"

# Merits & Flaws
python scripts/lookup.py d20.character merits-flaws --find "faith"

# Lore
python scripts/lookup.py d20.lore house-lore "Devils"
python scripts/lookup.py d20.lore evocations "Lore of Flame"

# Apocalyptic Forms
python scripts/lookup.py d20.apocalyptic visages "Visage of Flame"
```

---

## Validation

- [ ] Attributes: 15 dots (+ 9 base = 24 total)
- [ ] Abilities: 27 dots, none > 3
- [ ] Lore: 3 dots in House/Common Lore only
- [ ] Backgrounds: 5 dots
- [ ] Virtues: 10 total (7 + 3 base)
- [ ] Faith: 3
- [ ] Torment: Correct for House
- [ ] Willpower: Sum of two highest Virtues
- [ ] Flaws ≤ 7 points
- [ ] Freebies spent exactly
- [ ] Apocalyptic form documented with all traits
- [ ] (PC) All relevant backgrounds have documents:
  - [ ] Allies → NPC documents
  - [ ] Followers → Follower documents
  - [ ] Pacts → Pact documents
  - [ ] Mentor → NPC mentor document
- [ ] All links valid

---

## PC File Structure

```
[character]/
├── [character].md          ← Links to all below
├── npcs/                   ← Allies, Mentors
├── followers/              ← Followers
├── pacts/                  ← Pact agreements
└── apocalyptic-form.md     ← Form details
```

---

## Output Template

```markdown
# [Character Name]

**Celestial Name**: [Pre-Fall name]
**House**: [House] (The [Ordinal] House)
**Faction**: [Faction]
**Concept**: [Brief concept]

## The Mortal Host

**Name**: [Human name]
**Background**: [Who was this person before possession?]
**Why vulnerable**: [What made them susceptible to possession?]

## The Fallen

**Role Before Fall**: [What was the demon's duty in Heaven?]
**Role in Rebellion**: [What did they do during the war?]
**Time in Abyss**: [How did imprisonment affect them?]

## Personality

**Nature**: [Archetype]
**Demeanor**: [Archetype]

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
| Manipulation | ●●●○○ |
| Appearance | ●●○○○ |

### Mental
| Attribute | Rating |
|-----------|--------|
| Perception | ●●●○○ |
| Intelligence | ●●○○○ |
| Wits | ●●●○○ |

## Abilities

### Talents
| Ability | Rating | Specialty |
|---------|--------|-----------|
| [Ability] | ●●○○○ | |

### Skills
| Ability | Rating | Specialty |
|---------|--------|-----------|
| [Ability] | ●●○○○ | |

### Knowledges
| Ability | Rating | Specialty |
|---------|--------|-----------|
| [Ability] | ●●○○○ | |

## Lore

| Lore | Rating | Evocations Known |
|------|--------|------------------|
| [Lore] | ●●○○○ | [List evocations at this level] |

## Backgrounds

| Background | Rating | Details |
|------------|--------|---------|
| [Background] | ●●○○○ | [Link to document or brief] |

## Virtues & Morality

| Trait | Rating |
|-------|--------|
| Conscience | ●●●○○ |
| Conviction | ●●●○○ |
| Courage | ●●●○○ |

## Secondary Traits

| Trait | Value |
|-------|-------|
| Faith | ●●●○○○○○○○ |
| Torment | ●●●○○○○○○○ |
| Willpower | ●●●●●●○○○○ |

## Apocalyptic Form

**Visage**: [Sumerian Name], Visage of [Primary Lore]
**Primary Lore**: [Lore name]

### Low-Torment Traits (Always Available)
1. [Trait]: [Effect]
2. [Trait]: [Effect]
3. [Trait]: [Effect]
4. [Trait]: [Effect]

### High-Torment Traits (Unlocked at Torment 7+)
- [Trait 1] (Torment 7)
- [Trait 2] (Torment 8)
- [Trait 3] (Torment 9)
- [Trait 4] (Torment 10)

### Low-Torment Form
[Description of angelic/beautiful appearance]

| Trait | Effect |
|-------|--------|
| [Trait 1] | [Mechanical effect] |
| [Trait 2] | [Mechanical effect] |
| ... | ... |

### High-Torment Form
[Description of monstrous appearance]

| Trait | Effect |
|-------|--------|
| [Corrupted Trait 1] | [Mechanical effect] |
| [Corrupted Trait 2] | [Mechanical effect] |
| ... | ... |

## Merits & Flaws

| Merit/Flaw | Points | Description |
|------------|--------|-------------|
| [Name] | [+/-N] | [Brief description] |

## Description

**Mortal Appearance**: [Physical appearance in human form]

**Mannerisms**: [How the demon's nature shows through]

## Background

[Character history: the mortal's life, the moment of possession, adjustment to merged existence]

## Goals & Motivations

[What drives the character—both demon and remnants of mortal]
```
