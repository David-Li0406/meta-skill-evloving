# Risen Module

Create Risen characters for W20—wraiths who have reclaimed their physical bodies.

## What is a Risen?

A Risen is a wraith who has:
- Reclaimed their dead physical body
- Returned to the Skinlands in corporal form
- A single-minded purpose driving them
- A dormant (but not gone) Shadow

**Core Concept**: The Risen are driven by a single overwhelming goal. Once achieved, they return to the Underworld.

---

## Risen vs Wraith

| Aspect | Wraith | Risen |
|--------|--------|-------|
| Form | Plasmic (Corpus) | Physical body |
| Location | Underworld | Skinlands |
| Shadow | Active antagonist | Dormant |
| Purpose | Multiple Passions | Single driving goal |
| Duration | Indefinite | Until goal achieved |
| Arcanoi | Full range | Limited + Risen Arts |

---

## Requirements to Rise

A wraith must:
1. Have a single, focused **Driving Goal**
2. Have an intact **physical body** (or reconstruct it)
3. Successfully **reunite** with the body
4. **Suppress** the Shadow (temporarily)

---

## Creation Steps

### Standard Character Creation
1. **Concept** — As per `modules/wraith.md` Steps 1-6
2. **Attributes** — 7/5/3
3. **Abilities** — 13/9/5 (cap 3)
4. **Backgrounds** — 5 dots (reduced from 7)
5. **Arcanoi** — 3 dots (reduced from 5)
6. **Driving Goal** — One paramount Passion (see below)
7. **Fetters** — 5 dots (reduced from 10)

### Risen-Specific Steps
8. **Risen Arts** — 2 dots in Risen-specific powers
9. **Shadow** — Create dormant Shadow (uses `modules/shadow.md`)
10. **Physical Form** — Describe the body's current state
11. **Limitations** — Note Risen restrictions
12. **Freebies** — 15 points

---

## The Driving Goal

The Risen's existence is defined by a **single overwhelming purpose**:

### Requirements
- Must be specific and achievable
- Must be tied to their death or unfinished business
- Cannot be vague ("be happy") or impossible

### Examples
- "Kill the person who murdered me"
- "Protect my daughter until she turns 18"
- "Retrieve the artifact stolen from my grave"
- "Deliver my final message to my wife"

### Resolution
When the Driving Goal is complete:
- The Risen's body dies (again)
- The wraith returns to the Underworld
- New Passions may develop from the experience

---

## Risen Arts

Risen gain access to two unique powers:

### Lifesense
Perceive and interact with the living world.

| Level | Power |
|-------|-------|
| 1 | Sense life force nearby |
| 2 | Read surface emotions |
| 3 | Sense health/illness |
| 4 | Detect supernatural beings |
| 5 | Perfect living-world awareness |

### Misery
Project the grave's cold touch.

| Level | Power |
|-------|-------|
| 1 | Cause unease and discomfort |
| 2 | Inflict chilling cold |
| 3 | Cause pain through touch |
| 4 | Drain vitality |
| 5 | Death's embrace (lethal) |

---

## Physical Form

### Body Condition
The Risen must inhabit their original body. Its condition affects capabilities:

| Condition | Effects |
|-----------|---------|
| Fresh (days) | Minor penalties, pass as living |
| Decayed (weeks) | Obvious signs, social penalties |
| Skeletal (months+) | Major physical changes, cannot pass |
| Reconstructed | Rebuilt with Moliate, varies |

### Maintaining the Body
- Does not heal naturally
- Arcanoi or Risen Arts repair damage
- Severe damage may force return to Underworld
- Cannot truly die again (returns as wraith)

---

## The Dormant Shadow

### During Risen State
- Shadow cannot initiate Catharsis
- Cannot use most Thorns
- Still whispers occasionally
- Accumulates Angst slowly

### Awakening Triggers
- Failing the Driving Goal
- Extreme emotional trauma
- Certain supernatural effects
- Extended time in Risen state

### If Shadow Awakens
- Functions as normal (Catharsis possible)
- Risen state may end
- Body may be abandoned

---

## Risen Limitations

### Cannot Do
- Enter the Underworld voluntarily
- Use Argos (no Tempest travel)
- Regenerate Corpus naturally
- Ignore physical needs (sort of)

### Must Do
- Pursue Driving Goal
- Maintain physical form
- Avoid detection (usually)

### Social Restrictions
- Dead body walking is noticed
- Sunlight reveals decay
- Animals react negatively
- Most people are terrified

---

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Arcanos | 5 |
| Risen Art | 5 |
| Willpower | 2 |
| Fetter | 1 |
| Background | 1 |

---

## Validation

- [ ] Attributes: 15 dots (+ 9 base)
- [ ] Abilities: 27 dots, none > 3
- [ ] Backgrounds: 5 dots
- [ ] Arcanoi: 3 dots
- [ ] Risen Arts: 2 dots
- [ ] Driving Goal: Specific, achievable
- [ ] Fetters: 5 dots
- [ ] Shadow created (dormant)
- [ ] Physical form described
- [ ] Freebies spent exactly

---

## Output Format

```markdown
# [Character Name] (Risen)

## Concept
**Driving Goal**: [The single overwhelming purpose]
**Death**: [How they died]
**Body Condition**: [Current state of corpse]

## Statistics
[Standard stat block]

## Risen Arts
| Art | Rating |
|-----|--------|
| Lifesense | ●●○○○ |
| Misery | ●○○○○ |

## The Body
[Description of physical form]
[Visible signs of death]
[How they conceal their nature]

## The Dormant Shadow
**Archetype**: [Shadow's personality]
**Angst**: [Current level]
**Notes**: [Any warning signs]

## Driving Goal Details
[Expanded description]
[Steps needed to achieve it]
[What happens after]
```

---

## Reference Data

```bash
# Risen-specific rules
cat references/risen/risen-rules.md

# Risen Arts
python scripts/lookup.py risen.risen-arts risen-arts --keys
```
