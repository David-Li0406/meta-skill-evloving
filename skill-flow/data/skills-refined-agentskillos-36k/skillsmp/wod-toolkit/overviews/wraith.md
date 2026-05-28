# Wr20 Overview — Wraith: The Oblivion 20th Anniversary Edition

Creates mechanically valid Wraith: The Oblivion 20th Anniversary Edition content with automatic dependency resolution and background expansion.

## Workflow

1. **Identify content type** → Select appropriate module
2. **Read module** → Load `modules/wr20/[type].md` before starting
3. **For PCs** → Expand backgrounds via `modules/wr20/background-expansion.md`
4. **Create content** → Follow module workflow
5. **Validate** → Check module validation list
6. **Link documents** → Connect all sub-documents to parent

## Module Selection

### Wraith Characters
| Type | Module |
|------|--------|
| Wraith (PC/NPC) | `modules/wr20/wraith.md` |
| Risen | `modules/wr20/risen.md` |
| Spectre | `modules/wr20/spectre.md` |
| Orpheus Projector | `modules/wr20/orpheus.md` |
| Hue | `modules/wr20/orpheus.md` (Hue section) |
| Serviteur (Mirrorlands) | `modules/wr20/connaissance.md` |

### Mortal Characters
| Type | Module |
|------|--------|
| Medium | `modules/wr20/medium.md` |
| Medium (Lineage) | `modules/wr20/medium.md` (Benandanti/Hidalgo/Zukal) |
| Ghost Hunter | `modules/wr20/ghost-hunter.md` |
| Mortal Ally | `modules/wr20/ally.md` |

### Shadow System
| Type | Module |
|------|--------|
| Shadow creation | `modules/wr20/shadow.md` |
| Harrowing design | `modules/wr20/harrowing.md` |

### Arcanoi
| Type | Module |
|------|--------|
| Standard Arcanoi | `modules/wr20/arcanoi.md` |
| Dark Arcanoi | `modules/wr20/dark-arcanoi.md` |
| Connaissance (Mirrorlands) | `modules/wr20/connaissance.md` |

### Crafting & Items
| Type | Module |
|------|--------|
| Soulforging | `modules/wr20/soulforging.md` |
| Relic | `modules/wr20/relic.md` |
| Artifact | `modules/wr20/artifact.md` |

### Locations
| Type | Module |
|------|--------|
| Haunt | `modules/wr20/haunt.md` |

### Organizations
| Type | Module |
|------|--------|
| Circle (PC group) | `modules/wr20/circle.md` |
| Legion | `modules/wr20/legion.md` |
| Guild | `modules/wr20/guild.md` |

---

## Character Creation Quick Reference

### Wraith
| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Arcanoi | 5 |
| Backgrounds | 5 |
| Passions | 10 (min 3 Passions) |
| Fetters | 10 (min 3 Fetters) |
| Willpower | 5 |
| Pathos | 5 + Memoriam |
| Corpus | 10 |
| Freebies | 15 |

### Mortal (Medium/Ghost Hunter)
| Category | Dots |
|----------|------|
| Attributes | 6/4/3 (+ 9 base) |
| Abilities | 11/7/4 (cap 3) |
| Numina | 5 |
| Backgrounds | 5 |
| Willpower | 5 |
| Freebies | 21 |

### Freebie Costs
| Trait | Wraith | Mortal |
|-------|--------|--------|
| Attribute | 5 | 5 |
| Ability | 2 | 2 |
| Arcanos | 5 | — |
| Numina Path | — | 7 |
| Background | 1 | 1 |
| Passion | 1 | — |
| Fetter | 1 | — |
| Willpower | 1 | 1 |
| Pathos | 1 | — |

---

## Shadow Archetypes

### Core Archetypes
| Archetype | Approach |
|-----------|----------|
| The Abuser | Cruel tormentor |
| The Director | Controlling manipulator |
| The False Friend | Betraying companion |
| The Id | Pure impulse |
| The Martyr | Self-sacrificer |
| The Monster | Violent beast |

### Book of Oblivion Archetypes
| Archetype | Approach |
|-----------|----------|
| The Alien | Claims non-human origin |
| The Conqueror | Seeks total domination |
| The Destroyer | Wants to wreck everything |
| The Narcissist | Believes itself superior |
| The Obsessed | One difficult goal above all |

---

## Spectre Castes

| Caste | Power Level |
|-------|-------------|
| Striplings | Weakest |
| Doppelgangers | Low-Moderate |
| Mortwights | Moderate |
| Nephwracks | High |
| Shades | Very High |

**Note**: Spectres are Shadow-consumed wraiths, NOT spirits.

---

## Medium Lineages

| Lineage | Origin | Special Power |
|---------|--------|---------------|
| Benandanti | Italian | Ekstasis (spirit projection) |
| Hidalgo | Mexican/Maya | Maya necromancy |
| Zukal | Bohemian | Nadané (summoning/binding) |

---

## Mortal Numina

### Hedge Magic Paths
| Path | Function |
|------|----------|
| Whistling | Storm-based ghost manipulation |
| Black Hat | Tech-based spirit interaction |

### Psychic Paths
| Path | Function |
|------|----------|
| Starlight | Shadowlands travel with protection |
| Shade | Concealment from spirits (renamed from Shadow) |
| Divination | Prophecy through communion with dead |

---

## Data Lookup

```bash
# Arcanoi
python scripts/lookup.py wr20.arcanoi arcanoi --keys

# Shadow
python scripts/lookup.py wr20.shadow archetypes --keys
python scripts/lookup.py wr20.shadow thorns --keys

# Factions
python scripts/lookup.py wr20.factions legions --keys
python scripts/lookup.py wr20.factions guilds --keys

# Soulforging
python scripts/lookup.py wr20.soulforging styles --keys

# Mortals
python scripts/lookup.py wr20.mortals numina --keys

# Archetypes (shared)
python scripts/lookup.py shared.core archetypes "Martyr"
```

---

## Reference Files

### Wr20-Specific (`references/wr20/`)
- `arcanoi/` — Standard Arcanoi, Dark Arcanoi
- `character/` — Abilities, backgrounds, attributes
- `shadow/` — Shadow archetypes, Thorns
- `factions/` — Legions, Guilds
- `soulforging/` — Styles, alloys, techniques
- `spectres/` — Castes, Dark Arcanoi
- `mortals/` — Numina, medium lineages, ghost hunter organizations
- `mirrorlands/` — Connaissance, Serviteurs

### Shared (`references/shared/`)
- `umbra/` — Dark Umbra / Shadowlands structure
- `core/` — Archetypes, attributes, abilities
