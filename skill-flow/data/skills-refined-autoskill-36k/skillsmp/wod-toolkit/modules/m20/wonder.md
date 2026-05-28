# Wonder Module

Create Wonders (magical items) for M20 using Prism of Focus Practice integration.

## Dependency

**If Wonder has POWERS:** Read `modules/rote.md`, create full documents.

| Wonder Type | Rote Documents |
|-------------|----------------|
| Talisman | One per power (= Rank) |
| Artifact | One (single power) |
| Charm | One (single power) |
| Periapt | Only if secondary power |

## Prism of Focus Integration

### Practice and Wonder Creation
- Wonders are typically created using specific Practices
- **Alchemy** provides half Quintessence cost for Charms and Gadgets
- **Craftwork** grants -1 difficulty and bonus dice for physical creation
- **Investment** allows stored effects with increased potency over time
- Each Practice may have specific Wonder-creation benefits (see `lookup.py rules.practices practices`)

### Wonder Practice Association
Document which Practice was used to create the Wonder:
- Affects Resonance traits
- Determines activation style
- May provide difficulty modifiers for use

## Wonder Types

| Type | Powers | Arete | Reusable |
|------|--------|-------|----------|
| **Talisman** | Multiple (= Rank) | Yes | Yes |
| **Artifact** | Single | No | Yes |
| **Charm** | Single | Yes | No (one-use) |
| **Periapt** | Optional | Optional | Usually |

## Rank (0-10)

| Rank | Description | Background Cost |
|------|-------------|-----------------|
| 1-2 | Minor | 1-2 |
| 3-4 | Significant | 3-4 |
| 5 | Grand | 5 |
| 6-10 | Legendary | 6-10 |

## Type-Specific Rules

- **Talismans**: Powers = Rank, Arete ≤ Rank, Quintessence = Rank × 5
- **Artifacts**: 1 power, Rank = highest Sphere level
- **Charms**: 1 power, Arete = Rank, destroyed after use
- **Periapts**: Storage (Rank 1: 5-10, Rank 5: 50-100)

## Creation Workflow

1. **Type** — Talisman, Artifact, Charm, or Periapt
2. **Concept** — What is it? Who made it? Paradigm?
3. **Rank** — Based on power/capacity
4. **⛔ POWERS** — If any, read `modules/rote.md`, create documents
5. **Resonance** — Traits totaling ≥ Rank
6. **Physical Form** — Appearance matching paradigm
7. **History** — Origin, wielders, legends
8. **Document** — Link to rote files
9. **Validate**

## Output Format

```markdown
# [Wonder Name]

**Type:** [Talisman/Artifact/Charm/Periapt]
**Rank:** [X] | **Arete:** [X] | **Quintessence:** [X]

## Concept
## Physical Description
## History

## Powers

| Power | Spheres | Document |
|-------|---------|----------|
| [Name](../rotes/file.md) | Sphere N | Brief effect |

**All powers have full documents.**

## Resonance
## Activation
```

## Validation by Type

### Talisman
- [ ] Powers = Rank
- [ ] No power > Arete
- [ ] Each power has rote document

### Artifact
- [ ] Single power only
- [ ] Power has rote document

### Charm
- [ ] Single power
- [ ] Arete = Rank
- [ ] Destruction noted

### Periapt
- [ ] Max charges appropriate for Rank
- [ ] If secondary power: rote document exists

## File Structure

```
[project]/
├── wonders/
│   └── [wonder].md       ← Links to ../rotes/
└── rotes/
    └── [power].md
```

## Reference Data

```bash
python scripts/lookup.py rules.resonance-traits resonance-traits "Forces"
python scripts/lookup.py rules.sphere-levels sphere-levels "Prime"
```

## Return Format (for parent modules)

```
Created: ./wonders/ring_of_fire.md
Name: Ring of Fire
Type: Talisman
Rank: 3
```

---

## Malevolent Treasures (Nephandic Wonders)

Use standard wonder creation. Nephandic items often feature unique characteristics.

### Common Traits

- **Activation cost:** Often require pain, sacrifice, or acts of corruption
- **Binding:** Many contain bound demons or Banes
- **Paradox quirks:** Backlash tends to summon hostile entities rather than normal effects
- **Resonance:** Malignant, often perceptible even to mundane senses
- **Corruption:** Prolonged use may affect the wielder

### Sample Malevolent Treasures

| Item | Effect | Background Cost |
|------|--------|-----------------|
| The Catcher-Snatcher | Trap and steal souls | 5 |
| False Face | Perfect disguise, undetectable | 3 |
| Malign Cutlery | Weapons that enjoy killing (bonus vs. living) | 2-4 |
| The Riotizer | Incite violence in crowds | 4 |
| FIDO | Demonic surveillance device | 3 |
| Gallu's Lash | Whip with psychological domination effects | 4 |
| Portable Hellgate | Summon bound demons on demand | 12 |

### Malevolent Treasure Validation

In addition to standard wonder validation:
- [ ] Activation cost specified
- [ ] Any bound entities detailed
- [ ] Paradox consequences noted
- [ ] Corruption potential indicated
- [ ] Resonance described as malignant
