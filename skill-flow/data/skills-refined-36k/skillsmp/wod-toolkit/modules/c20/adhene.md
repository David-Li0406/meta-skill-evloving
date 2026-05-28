# Adhene Module

Create Adhene characters for C20—the Denizens of the Dreaming, ancient fae who never took the Changeling Way.

## What are Adhene?

Adhene (ah-HEEN-ee), also called Denizens, are fae who remained in the Dreaming during the Shattering rather than taking mortal form. They are alien, powerful, and operate by different rules than Kithain.

## Adhene vs. Kithain

| Aspect | Adhene | Kithain |
|--------|--------|---------|
| Origin | Pure Dreaming | Mortal-bonded |
| Mortality | Immortal (in Dreaming) | Reincarnating |
| Banality | Extremely vulnerable | Resistant |
| Ariá | Yes (mood states) | No |
| Glamour | Different rules | Standard |
| Autumn World | Difficult to exist | Natural |

---

## Adhene Types (Kiths)

### Acheri
**Concept**: Plague spirits, disease bringers
- **Glamour**: 4 | **Willpower**: 5
- **Ariá**: Dioniae (joy in suffering), Araminae (sorrow), Apolliae (healing)
- **Birthright**: Disease Touch—spread illness
- **Frailty**: Compulsion—must spread sickness
- **Origin**: Pestilence dreams, fears of plague

### Aonides
**Concept**: Muses, inspiration spirits
- **Glamour**: 6 | **Willpower**: 3
- **Ariá**: Apolliae (inspiration), Dioniae (passion), Araminae (melancholy)
- **Birthright**: Inspire—grant artistic ability
- **Frailty**: Fading—lose self without inspiring others
- **Origin**: Pure creative inspiration

### Fir-bholg
**Concept**: Giant warriors, primal fighters
- **Glamour**: 3 | **Willpower**: 6
- **Ariá**: Dioniae (battle fury), Apolliae (honor), Araminae (regret)
- **Birthright**: Titanic Strength—giant's power
- **Frailty**: Giant Form—cannot hide nature
- **Origin**: Ancient warrior dreams

### Fuath
**Concept**: Water horrors, drowning spirits
- **Glamour**: 5 | **Willpower**: 4
- **Ariá**: Dioniae (hunting), Araminae (loneliness), Apolliae (protection)
- **Birthright**: Water Form—become liquid
- **Frailty**: Hydrophilia—must be near water
- **Origin**: Fear of drowning, water spirits

### Keremet
**Concept**: Forest spirits, nature guardians
- **Glamour**: 5 | **Willpower**: 4
- **Ariá**: Apolliae (growth), Araminae (decay), Dioniae (wildness)
- **Birthright**: Nature Bond—command plants
- **Frailty**: Rooted—tied to location
- **Origin**: Sacred groves, forest dreams

### Moirae
**Concept**: Fate weavers, destiny shapers
- **Glamour**: 6 | **Willpower**: 5
- **Ariá**: Apolliae (order), Araminae (tragedy), Dioniae (chaos)
- **Birthright**: Fate Sight—see destinies
- **Frailty**: Bound by Fate—cannot defy predictions
- **Origin**: Concepts of fate and destiny

### Naraka
**Concept**: Demon spirits, tempters
- **Glamour**: 5 | **Willpower**: 5
- **Ariá**: Dioniae (temptation), Araminae (punishment), Apolliae (redemption)
- **Birthright**: Temptation—offer irresistible deals
- **Frailty**: Contract Bound—must honor deals
- **Origin**: Fears of damnation, moral struggles

Reference: `lookup.py gallain.adhene adhene`

---

## The Ariá System

Adhene don't have Seelie/Unseelie Legacies. Instead, they have **Ariá**—three mood states that shift.

### The Three Ariá

| Ariá | Nature | Equivalent |
|------|--------|------------|
| **Dioniae** | Passion, excess, chaos | Unseelie-adjacent |
| **Apolliae** | Reason, order, light | Seelie-adjacent |
| **Araminae** | Sorrow, shadow, loss | Neither—melancholy |

### Ariá Mechanics

- Adhene always have one **dominant Ariá**
- Triggers can shift dominant Ariá
- Each Ariá has associated behaviors
- Extreme situations force Ariá shifts

### Ariá Triggers

Each Adhene type has specific triggers:
| Ariá | Trigger Example |
|------|-----------------|
| Dioniae | Intense emotion, battle, passion |
| Apolliae | Success, creation, hope |
| Araminae | Loss, failure, witnessing tragedy |

---

## Creation Differences

| Category | Kithain | Adhene |
|----------|---------|--------|
| Attributes | 7/5/3 | 6/5/4 |
| Abilities | 13/9/5 | 11/8/5 |
| Backgrounds | 5 | 5 |
| Arts | 3 | 4 (Dreaming affinity) |
| Realms | 5 | 5 |
| Glamour | By kith | By kith (often higher) |
| Willpower | By kith | By kith |
| Banality | By seeming | 0 (but extremely vulnerable) |
| Freebies | 15 | 15 |

---

## Creation Steps

1. **Concept** — Adhene type, role, motivation
2. **Ariá** — Dominant and secondary Ariá
3. **Attributes** — 6/5/4 across Physical/Social/Mental
4. **Abilities** — 11/8/5 (cap 3)
5. **Backgrounds** — 5 dots (limited selection)
6. **Arts** — 4 dots
7. **Realms** — 5 dots
8. **Glamour** — By adhene type
9. **Willpower** — By adhene type
10. **Banality** — 0 (special rules)
11. **Birthrights & Frailty** — From type
12. **Freebies** — 15
13. **Validate**

---

## Adhene Backgrounds

Limited selections:

| Background | Available | Notes |
|------------|-----------|-------|
| Chimera | Yes | Native companions |
| Contacts | Limited | Dreaming-based |
| Holdings | Yes | Dreaming freeholds only |
| Mentor | Yes | Elder Adhene |
| Retinue | Yes | Dreaming servants |
| Treasure | Yes | Dreaming items |
| Remembrance | Yes (special) | Deep Dreaming memories |

**Not Available**: Dreamers, Resources (mortal), Title (Kithain)

---

## Banality and Adhene

Adhene have Banality 0 but are **extremely vulnerable**:

| Banality Exposure | Effect |
|-------------------|--------|
| Banal person | Discomfort, -1 dice |
| Banal area | Pain, lose Glamour |
| Autumn Person | Severe damage |
| Cold Iron | Devastating |
| Extended exposure | May be destroyed |

### Survival in Autumn World

Adhene can exist in the mortal world but must:
- Stay in freeholds when possible
- Avoid Banal people/places
- Maintain Glamour constantly
- Take mortal host (difficult)

---

## Husks (Mortal Hosts)

Some Adhene take mortal bodies called **Husks** to survive:

| Method | Effect |
|--------|--------|
| Willing Host | Sharing body, less Banality damage |
| Forced Possession | Control, but host may resist |
| Created Husk | Artificial body, unstable |

**With Husk**: Banality protection, but trapped in mortal concerns.

---

## Output Format

```markdown
# [Character Name]

**Type**: Adhene
**Subtype**: [Acheri/Aonides/etc.]
**Dominant Ariá**: [Dioniae/Apolliae/Araminae]
**Location**: [Dreaming realm or Autumn World]
**Husk**: [None/Description if applicable]

## Concept
[Description of this Dreaming denizen]

## Ariá States

### Dominant: [Ariá]
[Behavior when in this state]

### Secondary: [Ariá]
[Behavior when this emerges]

### Triggers
| To Dioniae | To Apolliae | To Araminae |
|------------|-------------|-------------|
| [Trigger] | [Trigger] | [Trigger] |

## Attributes

### Physical
| Attribute | Rating |
|-----------|--------|
| Strength | ●●●○○ |
| Dexterity | ●●○○○ |
| Stamina | ●●●○○ |

### Social
[etc.]

### Mental
[etc.]

## Abilities
[Standard format]

## Advantages

### Backgrounds
| Background | Rating |
|------------|--------|
| [Background] | ●●○○○ |

### Arts
| Art | Rating |
|-----|--------|
| [Art] | ●●●○○ |

### Realms
| Realm | Rating |
|-------|--------|
| [Realm] | ●●○○○ |

## Birthrights & Frailty

### Birthrights
- **[Birthright Name]**: [Description]

### Frailty
- **[Frailty Name]**: [Description]

## Vital Statistics

| Stat | Rating |
|------|--------|
| Glamour | ●●●●●●○○○○ |
| Willpower | ●●●●●○○○○○ |
| Banality | ○○○○○○○○○○ |

## Appearance
[Dreaming form description]

## Husk (if applicable)
[Mortal host description]

## Dreaming Domain
[Where they originate/dwell in Dreaming]

## History
[Ancient history, how they came to current situation]

## Motivation
[What drives them]
```

---

## Validation

- [ ] Adhene type selected
- [ ] Dominant Ariá specified
- [ ] Ariá triggers defined
- [ ] Attributes: 15 dots (6/5/4)
- [ ] Abilities: 24 dots (11/8/5)
- [ ] Arts: 4 dots
- [ ] Realms: 5 dots
- [ ] Backgrounds: 5 dots (valid selections)
- [ ] Banality: 0
- [ ] Birthrights and Frailty from type
- [ ] Husk described if in Autumn World

---

## Reference Data

```bash
# Adhene types
python scripts/lookup.py gallain.adhene adhene "Moirae"

# Ariá details
python scripts/lookup.py gallain.aria aria "Dioniae"

# Adhene in Autumn World
python scripts/lookup.py gallain.adhene-husks adhene-husks --all
```
