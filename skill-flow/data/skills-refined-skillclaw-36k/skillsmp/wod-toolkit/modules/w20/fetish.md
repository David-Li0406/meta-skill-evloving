# Fetish Module

Create fetishes (permanent spirit items) and talens (single-use) for W20.

## References
- `lookup.py fetish.fetishes-by-level fetishes-by-level` — Fetish examples by level
- `lookup.py fetish.talen-examples talen-examples` — Talen examples
- `lookup.py fetish.fetish-creation-guide fetish-creation-guide` — **Creation rules and power scaling**

---

## Fetish vs Talen

| Aspect | Fetish | Talen |
|--------|--------|-------|
| Duration | Permanent | One use |
| Creation | Rite of the Fetish | Rite of Binding |
| Attunement | Required | Not required |

---

## Power by Level

| Level | BG Cost | Gnosis | Power Scope | Combat | Examples |
|-------|---------|--------|-------------|--------|----------|
| 1 | 1 | 3-5 | Minor utility, passive effects | None | Harmony Flute, Baneskin |
| 2 | 2 | 4-6 | Specific utility, detection | Indirect support | Feather of Ma'at, Spirit Tracer |
| 3 | 3 | 5-7 | Supernatural powers, weapons | Str+1-4 agg | Fang Dagger, Phoebe's Veil |
| 4 | 4 | 5-8 | Signature weapons, major effects | Str+2-4 agg + extras | Klaive, Feathered Cloak |
| 5 | 5 | 6-10 | Legendary, chronicle-defining | Str+5-6 agg | Grand Klaive, Runestones |

---

## Gnosis Rating Guidelines

| Rating | Meaning | Typical Level |
|--------|---------|---------------|
| 3-4 | Easy activation, minor effect | Level 1 |
| 5 | Standard activation | Level 1-2 |
| 6 | Moderate difficulty | Level 3-4 |
| 7 | Challenging activation | Level 3-5 |
| 8+ | Powerful artifacts | Level 4-5 |

**Silver weapons**: Reduce effective Gnosis by 1 for attunement.

---

## Spirit Types by Effect

| Effect | Spirit Types |
|--------|-------------|
| Combat damage | War, Rage, Predator spirits |
| Anti-vampire | Sun, Fire, Helios servants |
| Stealth/Invisibility | Night, Shadow, Lunes |
| Detection/Truth | Truth, Light, Bird spirits |
| Tracking | Predator, Hound, Wind spirits |
| Protection/Wards | Guardian, Turtle, Ancestor spirits |
| Transformation | Trickster, Illusion, Ancestor spirits |
| Flight | Bird, Wind, Air elementals |
| Divination | Time, Dream, Wisdom, Chimera brood |

---

## Object Selection

| Effect Type | Appropriate Objects |
|-------------|---------------------|
| Weapons | Daggers, swords, hammers, whips, axes |
| Concealment | Cloaks, veils, bags, pouches |
| Detection | Feathers, needles, crystals |
| Communication | Flutes, whistles, bells |
| Protection | Chimes, shields, rings |
| Transformation | Masks, skins, talismans |

**Materials**: Silver (anti-Garou, -1 Gnosis), Gold (sun effects), Iron (anti-Fae), Bone (death/cold), Wood (nature), Feathers (flight/truth)

---

## Creation Steps

1. **Effect** — Define what the fetish does
2. **Level** — Assign based on power (1-5)
3. **Gnosis** — Set based on level and effect strength
4. **Spirit** — Choose thematically appropriate spirit type
5. **Object** — Select matching physical form
6. **Activation** — Roll Gnosis or spend Gnosis point
7. **System** — Write mechanics (rolls, difficulties, durations)
8. **Validate** — Compare to existing fetishes at same level

---

## Attunement

Roll Gnosis (difficulty = fetish's Gnosis rating).
- **Success**: Attuned permanently
- **Failure**: Cannot retry until next story
- **Silver**: Reduces effective Gnosis by 1

---

## Output Format

```markdown
# [Fetish Name]

**Level**: [1-5]
**Gnosis**: [Rating]

## Description
[Physical description of the object]

## Spirit
**Type**: [Spirit type bound]
**Rank**: [Gaffling/Jaggling/etc.]

## Power
[What it does when activated]

## System
**Activation**: [Roll Gnosis difficulty X / Spend 1 Gnosis]
**Effect**: [Mechanical details]
**Duration**: [Scene / Permanent / etc.]

## Creation
**Object**: [Required components]
**Rite**: Rite of the Fetish
```
