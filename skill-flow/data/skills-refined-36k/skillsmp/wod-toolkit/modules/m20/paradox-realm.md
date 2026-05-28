# Paradox Realm Module

Create Paradox Realms (punishment dimensions) for M20.

## What is a Paradox Realm?

Pocket dimension created by Paradox to punish vulgar magick abuse. Tailored to the mage's Resonance, paradigm, and transgressions.

## Realm by Triggering Sphere

| Sphere | Realm Nature |
|--------|--------------|
| **Correspondence** | Space is wrong—distances lie, locations shift |
| **Entropy** | Decay and chaos—things break, luck fails |
| **Forces** | Energy wild—storms, extremes, uncontrolled power |
| **Life** | Biological horror—mutation, predators, disease |
| **Matter** | Solid reality—traps, puzzles, crushing weight |
| **Mind** | Mental trials—illusions, madness, identity erosion |
| **Prime** | Quintessence distortion—magical paradoxes |
| **Spirit** | Spirit realm—hostile entities, bargains |
| **Time** | Temporal anomalies—loops, aging, causality breakdown |

```bash
python scripts/lookup.py rules.sphere-levels sphere-levels "[Sphere]"
```

## Paradigm Logic Types

| Paradigm | Logic |
|----------|-------|
| Mechanistic Cosmos | Clockwork, gears, precise laws |
| Chaos | Random, unpredictable, mutable |
| Data | Digital, informational, code |
| Faith | Religious, moral, devotional |
| Antimagick | Hostile to all supernatural |
| Divine Order | Heavenly hierarchy, judgment |
| Scientific Method | Laboratory, experimentation |
| Primal Nature | Wild, natural, animalistic |
| Dream Logic | Surreal, symbolic, fluid |
| Technological | Machine, electronic, systematic |
| Mystical | Traditional occult symbolism |
| Martial | Combat, warfare, challenge |

## Severity and Obstacles

| Severity | Paradox Pts | Primary | Random |
|----------|-------------|---------|--------|
| Mild | 1-5 | 1 | 0-1 |
| Moderate | 6-10 | 2 | 1-2 |
| Severe | 11-15 | 3-4 | 2-3 |
| Catastrophic | 16+ | 4-6 | 3+ |

See `references/paradox-realm/obstacles.md` for obstacle tables.

## Final Obstacle Types

| Type | Escape Requirement |
|------|-------------------|
| Give Secret | Reveal hidden truth |
| Win Game | Complete challenge |
| Solve Riddle | Answer paradigm puzzle |
| Button | Find escape mechanism |
| Maze | Navigate to exit |
| Abnormal Maze | Non-Euclidean navigation |
| Silver Bullet | Find specific weakness |
| Guess Name | Identify realm's true nature |
| Random Sphere | Overcome Sphere challenge |
| Combined | Multiple obstacles |

## Thematic Principles

**Punishment fits crime**: Time mage rewinding → time loops. Life mage transforming others → becomes prey.

**Paradigm inversion**: Realm often inverts mage's paradigm. Technocrat faces mystical nonsense.

**Personal resonance**: Draws on mage's Resonance, fears, history.

**Escapable but costly**: Escape requires sacrifice, insight, or growth.

## Creation Workflow

1. **Triggering Event** — What vulgar magick? How severe?
2. **Primary Sphere** — Which Sphere abused?
3. **Secondary Sphere** (optional)
4. **Paradigm Logic** — Worldview shaping realm
5. **Obstacle Count** — Based on severity
6. **Design Obstacles** — See `references/paradox-realm/obstacles.md`
7. **Final Obstacle** — Escape condition
8. **Atmosphere** — Appearance, sensory details, emotional weight
9. **Consequences** — What happens on failure?

## Output Format

```markdown
# [Realm Name]

**Primary Sphere:** [Sphere] | **Paradigm:** [Type] | **Severity:** [Level]

## Triggering Event
[What caused this]

## Realm Description
[Appearance, atmosphere]

## Primary Obstacles
1. [Obstacle based on Primary Sphere]
2. [...]

## Random Obstacles
1. [Secondary/random]

## Final Obstacle
**Type:** [Type]
[Description of escape condition]

## Consequences of Failure
[What happens if mage fails]

## Lessons
[What the realm teaches]
```

## Validation

- [ ] Primary Sphere matches triggering magick
- [ ] Paradigm consistently shapes logic
- [ ] Obstacle count matches severity
- [ ] Obstacles relate to Spheres
- [ ] Final obstacle is escapable
- [ ] Atmosphere reinforces horror
- [ ] Realm teaches a lesson
- [ ] Failure consequences defined

## Return Format

```
Created: ./paradox_realms/clockwork_prison.md
Name: The Clockwork Prison
Sphere: Time
Severity: Moderate
```
