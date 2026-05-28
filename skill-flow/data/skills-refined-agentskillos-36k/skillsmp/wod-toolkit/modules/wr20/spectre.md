# Spectre Module

Create Spectre antagonists for W20. Spectres are wraiths who have been consumed by their Shadows and now serve Oblivion.

## What is a Spectre?

A Spectre is a wraith whose Shadow has permanently taken control:
- The Psyche is suppressed or destroyed
- The being now serves Oblivion
- They possess Dark Arcanoi and other powers
- They seek to drag other wraiths into the Void

---

## Spectre Castes

Spectres are organized into **castes** based on power and origin:

| Caste | Power Level | Description |
|-------|-------------|-------------|
| **Striplings** | Weakest | Newly fallen, confused |
| **Doppelgangers** | Low-Moderate | Infiltrators, mimics |
| **Mortwights** | Moderate | Standard soldiers |
| **Nephwracks** | High | Leaders, commanders |
| **Shades** | Very High | Ancient, powerful |
| **Malfeans** | Extreme | Near-divine servants |
| **Neverborn** | Godlike | Primordial entities |

```bash
python scripts/lookup.py spectres.castes castes "Nephwrack"
```

---

## Creation by Caste

### Striplings
Newly converted Spectres, still adjusting to their state.

| Trait | Allocation |
|-------|------------|
| Attributes | 6/4/3 |
| Abilities | 9/6/3 |
| Dark Arcanoi | 3 |
| Backgrounds | 2 |
| Angst | 6+ |
| Freebies | 10 |

### Doppelgangers
Infiltrator Spectres who can mimic wraiths.

| Trait | Allocation |
|-------|------------|
| Attributes | 7/5/3 |
| Abilities | 11/7/4 |
| Dark Arcanoi | 5 |
| Backgrounds | 3 |
| Angst | 7+ |
| Freebies | 15 |

**Special**: Doppelgangers can perfectly mimic other wraiths.

### Mortwights
Standard Spectre soldiers and servants.

| Trait | Allocation |
|-------|------------|
| Attributes | 7/5/4 |
| Abilities | 13/9/5 |
| Dark Arcanoi | 6 |
| Backgrounds | 4 |
| Angst | 8+ |
| Freebies | 20 |

### Nephwracks
Powerful Spectre commanders and leaders.

| Trait | Allocation |
|-------|------------|
| Attributes | 8/6/4 |
| Abilities | 15/11/7 |
| Dark Arcanoi | 8 |
| Backgrounds | 5 |
| Angst | 9+ |
| Freebies | 30 |

**Special**: May have Shadecraft arts.

### Shades
Ancient Spectres of tremendous power.

| Trait | Allocation |
|-------|------------|
| Attributes | 9/7/5 |
| Abilities | 18/13/9 |
| Dark Arcanoi | 10 |
| Backgrounds | 7 |
| Angst | 10 |
| Freebies | 50 |

**Special**: Multiple Shadecraft arts, unique powers.

### Malfeans & Neverborn
Plot devices, not standard NPCs. Use narrative description rather than stats.

---

## Spectre Components

### Reversed Shadow
- The **Shadow** is now dominant
- The **Psyche** is suppressed (may still exist, weakened)
- Shadow Archetype becomes the Spectre's personality

### Dark Passions
- All Passions are now Dark Passions
- Focused on destruction, corruption, Oblivion
- May retain twisted versions of original Passions

### Dark Arcanoi
Spectres use **Dark Arcanoi** instead of standard Arcanoi:
- Some overlap with standard powers
- Many unique to Spectres
- Often more destructive/corrupting

```bash
python scripts/lookup.py arcanoi.dark-arcanoi dark-arcanoi --keys
```

### Shadecraft
Higher-caste Spectres may have **Shadecraft** arts—powers to manipulate Shadows directly.

---

## Creation Workflow

1. **Caste** — Determine power level
2. **Origin** — Who was this wraith? How did they fall?
3. **Shadow Archetype** — Now the dominant personality
4. **Attributes** — By caste allocation
5. **Abilities** — By caste allocation
6. **Dark Passions** — Replace regular Passions
7. **Dark Arcanoi** — By caste allocation
8. **Backgrounds** — By caste allocation
9. **Shadecraft** — For Nephwracks and above
10. **Freebies** — By caste allocation
11. **Appearance** — Corrupted, monstrous features
12. **Motivation** — Specific goals
13. **Validate**

---

## The Suppressed Psyche

Some Spectres retain a fragment of their former Psyche:

### Completely Gone
- No trace of original personality
- Pure servant of Oblivion
- No possibility of redemption

### Dormant
- Psyche exists but is powerless
- May surface briefly in extreme circumstances
- Slim possibility of redemption (plot device)

### Struggling
- Psyche actively fights for control
- Creates internal conflict
- May assist PCs under right circumstances
- Rare, dramatic roleplaying opportunity

---

## Dark Arcanoi

### Common Dark Arcanoi

| Dark Arcanos | Function |
|--------------|----------|
| **Shroudspeak** | Communicate through the Shroud (corrupting) |
| **Tempest-Weaving** | Manipulate storm energy |
| **Nihilism** | Create/enlarge Nihils |
| **Hive-Mind** | Spectre telepathic network |
| **Corruption** | Spread Oblivion's taint |
| **Larceny** | Steal Corpus, Pathos, memories |

### Shadecraft Arts

| Art | Function |
|-----|----------|
| **Shadow Call** | Communicate with Shadows |
| **Awaken Shadow** | Strengthen a wraith's Shadow |
| **Possess Shadow** | Take control of another's Shadow |
| **Manifest Shadow** | Give Shadow physical form |

---

## Spectre Appearance

Spectres bear visible marks of Oblivion's corruption:

### Physical Corruption
- Pallid, necrotic appearance
- Glowing or empty eyes
- Exposed bone or organs
- Unnatural proportions

### Atmospheric Effects
- Temperature drops nearby
- Darkness deepens
- Unpleasant smells
- Whispers of despair

### Deathmarks (Exaggerated)
- Original deathmarks become horrific
- Gunshot wounds gape
- Burns spread
- Decay accelerates

---

## Output Format

```markdown
# [Spectre Name]

**Caste**: [Caste]
**Former Identity**: [Who they were]

## Origin
[How they fell to Oblivion]
[What broke them]

## Personality
**Dominant Shadow Archetype**: [Archetype]
[How this manifests]

## Attributes
**Physical**: Strength [N], Dexterity [N], Stamina [N]
**Social**: Charisma [N], Manipulation [N], Appearance [N]
**Mental**: Perception [N], Intelligence [N], Wits [N]

## Abilities
[List key abilities with ratings]

## Dark Passions
| Passion | Emotion | Rating |
|---------|---------|--------|
| [Statement] | [Emotion] | ●●●○○ |

## Dark Arcanoi
| Arcanos | Rating |
|---------|--------|
| [Name] | ●●●○○ |

## Shadecraft (if applicable)
| Art | Rating |
|-----|--------|
| [Name] | ●●○○○ |

## Statistics
**Corpus**: [N]
**Angst**: [N] (permanent)
**Willpower**: [N]

## Appearance
[Physical description]
[Corruption manifestations]

## Tactics
[How this Spectre operates]
[Preferred methods of attack]

## Motivation
[Specific goals]
[What drives this Spectre]

## The Psyche (if applicable)
[Status of the suppressed Psyche]
[Any remaining traces of the original wraith]
```

---

## Validation

- [ ] Caste selected
- [ ] Attributes match caste allocation
- [ ] Abilities match caste allocation
- [ ] Dark Arcanoi match caste allocation
- [ ] Angst ≥ caste minimum
- [ ] Dark Passions defined
- [ ] Shadow Archetype identified
- [ ] Origin story provided
- [ ] Appearance described (with corruption)
- [ ] Motivation established

---

## Reference Data

```bash
# Spectre castes
python scripts/lookup.py spectres.castes castes --keys

# Dark Arcanoi
python scripts/lookup.py arcanoi.dark-arcanoi dark-arcanoi --keys

# Shadecraft
python scripts/lookup.py spectres.shadecraft shadecraft --keys

# Example Spectres
python scripts/lookup.py spectres.examples examples --keys
```
