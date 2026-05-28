# Psychic Phenomena Module

Rules for psychic characters and creating custom psychic phenomena in M20 Sorcerer.

## Overview

Psychic phenomena are **innate mental powers** that don't require training, rituals, or foci. Unlike hedge magic Paths:

- **No Practice or Ability cap** — Phenomena are pure talent
- **No rituals** — All effects are instant
- **Simpler activation** — Typically Attribute + Phenomenon rating
- **Often more focused** — Each phenomenon does one thing well

## System

### Dice Pool
Varies by phenomenon, typically:
- **Perception** + Phenomenon (sensing powers)
- **Intelligence** + Phenomenon (complex mental powers)
- **Willpower** + Phenomenon (forceful powers)

### Difficulty
Generally 6-8, modified by circumstances.

### No Witnesses Penalty
Psychic phenomena are invisible — no Sleeper witness penalties (usually).

---

## Psychic vs Hedge Magic

| Aspect | Psychic | Hedge Magic |
|--------|---------|-------------|
| Ability Cap | None | Path ≤ Ability |
| Rituals | None | Can learn rituals |
| Foci | Usually none | Practice-dependent |
| Flexibility | Narrow focus | Broader applications |
| XP for new type | 21 XP for secondary | 21 XP for secondary |

---

## All Phenomena Quick Reference

```bash
python scripts/lookup.py sorcerer.psychic-phenomena psychic-phenomena --keys
```

| Phenomenon | Primary Use |
|------------|-------------|
| Animal Psychics | Communicate/control animals |
| Anti-Psychic | Suppress supernatural powers |
| Astral Projection | Project consciousness outside body |
| Biocontrol | Control own biological functions |
| Channeling | Allow spirits to possess you |
| Clairvoyance | Remote viewing |
| Cyberkinesis | Control electronics with mind |
| Cyberpathy | Mental interface with computers |
| Ectoplasmic Generation | Create physical ghostly matter |
| Mind Shields | Mental defense |
| Precognition | See the future |
| Psychic Healing | Heal through mental power |
| Psychic Hypnosis | Hypnotize and control |
| Psychic Invisibility | Become mentally unnoticeable |
| Psychic Vampirism | Drain life energy |
| Psychokinesis | Telekinesis |
| Psychometry | Read object history |
| Psychoportation | Teleport self |
| Pyrokinesis | Create/control fire |
| Shadow | Manipulate darkness |
| Synergy | Link minds, enhance groups |
| Telepathy | Read/project thoughts |

---

## Detailed Phenomenon Mechanics

### Telepathy
**Dice Pool**: Perception + Telepathy vs Willpower  
**Range**: Line of sight (higher levels extend)

| Level | Capability |
|-------|------------|
| • | Sense emotional states |
| •• | Read surface thoughts, send messages |
| ••• | Deep mind reading, telepathic conversation |
| •••• | Memory access, mental commands |
| ••••• | Complete control, rewrite memories |

### Psychokinesis
**Dice Pool**: Willpower + Psychokinesis  
**Difficulty**: Based on weight/complexity

| Level | Weight Limit |
|-------|--------------|
| • | Few ounces, slow movement |
| •• | Few pounds, normal speed |
| ••• | ~100 lbs, precise control |
| •••• | ~500 lbs, great force |
| ••••• | Cars/heavy objects, molecular control |

### Precognition
**Dice Pool**: Perception + Precognition  
**Notes**: Future is mutable — visions show possibilities

| Level | Clarity |
|-------|---------|
| • | Vague feelings about immediate future |
| •• | Flash visions of significant events |
| ••• | Detailed visions, specific questions |
| •••• | See multiple possible futures |
| ••••• | Perfect clarity, influence probability |

### Mind Shields
**Dice Pool**: Passive or Willpower + Mind Shields  
**Effect**: Adds difficulty to read your mind

| Level | Protection |
|-------|------------|
| • | +1 diff to read |
| •• | +2 diff, detect intrusion attempts |
| ••• | +3 diff, extend to nearby allies |
| •••• | Counter-attack intruders |
| ••••• | Mental fortress, damage attackers |

---

## Creating Custom Phenomena

### Step 1: Define the Concept
What mental ability does this represent?
- Must be achievable through mental power alone
- Should be focused (not a grab-bag of abilities)
- Consider if it overlaps existing phenomena

### Step 2: Determine Dice Pool
Choose appropriate combination:
- **Perception** — Sensing, detecting, observing
- **Intelligence** — Complex operations, analysis
- **Willpower** — Force, resistance, projection
- **Charisma** — Influence, projection
- **Manipulation** — Subtle control

### Step 3: Define Levels

| Level | Guideline |
|-------|-----------|
| • | Sensing, minor self-affecting |
| •• | Basic manipulation, affect one target |
| ••• | Significant power, affect area/multiple |
| •••• | Major effects, supernatural-tier |
| ••••• | Mastery, legendary capabilities |

### Step 4: Consider Limitations
- Does it work on the unwilling?
- What range limitations?
- Duration of effects?
- Can it be resisted? How?

---

## Phenomenon Template

```markdown
# [Phenomenon Name]

**Dice Pool**: [Attribute] + [Phenomenon]
**Difficulty**: [Base difficulty and modifiers]
**Resistance**: [How targets resist, if applicable]

## Effects by Level

| Level | Capability |
|-------|------------|
| • | [First level] |
| •• | [Second level] |
| ••• | [Third level] |
| •••• | [Fourth level] |
| ••••• | [Fifth level] |

## Notes
[Special rules, limitations, interactions]
```

---

## Example Custom Phenomena

### Technopathy
**Concept**: Feel the "emotions" of machines, sense malfunctions

**Dice Pool**: Perception + Technopathy

| Level | Capability |
|-------|------------|
| • | Sense whether machines are "healthy" or malfunctioning |
| •• | Diagnose specific problems, sense machine "mood" |
| ••• | Communicate simple concepts to machines |
| •••• | Machines respond favorably (+1 die to Technology) |
| ••••• | Machines actively assist, reveal hidden functions |

**Notes**: Doesn't control machines (see Cyberkinesis), just understands them.

### Probability Sight
**Concept**: See likelihood of events in real-time

**Dice Pool**: Perception + Probability Sight

| Level | Capability |
|-------|------------|
| • | Sense if something is likely/unlikely in next few seconds |
| •• | See probability percentages for immediate actions |
| ••• | See branching possibilities for next few minutes |
| •••• | Perceive optimal path through complex situations |
| ••••• | See far-reaching probability cascades |

**Notes**: Vision only — doesn't change probability (see Fortune Path).

---

## Psychic Merits & Flaws

See `lookup.py sorcerer.merits-flaws merits-flaws` for psychic-specific options:

**Merits**:
- Detached (4pt) — No wound penalties on powers until Incapacitated
- Twin Link (4/6pt) — Permanent connection to another psychic

**Flaws**:
- Psychic Feedback (1/2/6pt) — Powers take physical toll
- Psi Focus (3/4/5pt) — Require external elements

---

## Validation Checklist

- [ ] Concept is focused (not too broad)
- [ ] Distinct from existing phenomena
- [ ] Appropriate dice pool chosen
- [ ] Reasonable power progression
- [ ] Limitations defined
- [ ] Resistance mechanics (if applicable)
- [ ] Achievable through mental power alone
