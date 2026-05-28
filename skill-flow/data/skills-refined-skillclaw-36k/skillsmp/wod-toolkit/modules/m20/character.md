# Character Module

Create mechanically valid Mage characters for M20 using the Prism of Focus system.

## PC vs NPC

| Type | Linked Documents | When |
|------|------------------|------|
| **PC** (default) | REQUIRED | Standard creation |
| **NPC** | Not required | "NPC", "quick", "simple", "stat block" |

## Dependencies (PC Only)

**Read `modules/background-expansion.md` for the complete background → module mapping.**

| Background | Action |
|------------|--------|
| (all PCs) | Read `modules/rote.md`, create 6 dots of rotes |
| Library, Node, Sanctum, Wonder, Chantry | See `modules/background-expansion.md` |
| Allies, Retainers, Cult, Spies, Backup | See `modules/background-expansion.md` |
| Familiar | Read `modules/familiar.md`, create the familiar |

**DO NOT create a PC with backgrounds as one-line summaries.**

## Creation Steps

1. **PC/NPC** — Default PC
2. **Concept** — Name, faction, subfaction, affinity Sphere
3. **Nature & Demeanor** — From `lookup.py character.archetypes archetypes`
4. **Attributes** — 7/5/3 across Physical/Social/Mental
5. **Abilities** — 13/9/5 across Talents/Skills/Knowledges (cap 3)
6. **Backgrounds** — 7 dots. Note which need sub-documents
7. **Arete** — Base 1, max 3 with freebies (4/dot)
8. **Spheres** — 1 free Affinity + 5 dots (capped at Arete). See Sphere Selection section.
9. **Focus (Prism of Focus)** — See Focus section below
10. **Resonance** — 1 trait, rating 1-5
11. **⛔ ROTES (PC)** — Read `modules/rote.md`, create 6 dots worth
12. **Merits & Flaws** — From `lookup.py character.merits-flaws merits-flaws`. Flaws ≤ 7
13. **⛔ BACKGROUNDS (PC)** — Create documents for Library/Node/Sanctum/Wonder/Chantry
14. **Freebies** — 15 + Flaws - Merits. Spend exactly.
15. **Derived** — Willpower 5+, Quintessence = Avatar, Paradox 0
16. **Specialties** — Required for 4+ traits
17. **Description** — Appearance, dress, mannerisms
18. **Document** — Link all sub-documents
19. **Validate**

---

## Sphere Selection

When choosing Spheres, consult the detailed sphere references to understand what each level can do:

### Sphere Reference Files
Use the efficient JSON lookup for quick queries:

```bash
# Get sphere level details
python scripts/lookup.py rules.sphere-details sphere-details "Forces 3"

# Search for capabilities
python scripts/lookup.py rules.sphere-details sphere-details --find "teleport"
```

For deep dives (edge cases), use markdown files:

| Sphere | Reference | Primary Uses |
|--------|-----------|--------------|
| Correspondence | `references/spheres/correspondence.md` | Space, distance, teleportation, gates |
| Entropy | `references/spheres/entropy.md` | Fate, fortune, decay, probability |
| Forces | `references/spheres/forces.md` | Energy, elements, weather, telekinesis |
| Life | `references/spheres/life.md` | Healing, shapeshifting, bodies |
| Matter | `references/spheres/matter.md` | Objects, transmutation |
| Mind | `references/spheres/mind.md` | Thoughts, telepathy, control, astral |
| Prime | `references/spheres/prime.md` | Quintessence, enchantment, agg damage |
| Spirit | `references/spheres/spirit.md` | Umbra, spirits, Gauntlet, Fetishes |
| Time | `references/spheres/time.md` | Temporal manipulation (most dangerous) |

### Sphere Level Summary
| Rank | Capability |
|------|------------|
| 1 | Perception only |
| 2 | Manipulate existing phenomena |
| 3 | Significant manipulation, conjure (+ Prime 2) |
| 4 | Drastic transformation |
| 5 | Mastery—create, destroy, fundamentally alter |

### Common Effect Quick Reference
For "How do I do X?" questions, check `references/spheres/conjunctions.md`:

| Effect | Spheres |
|--------|---------|
| Teleport self | Corr 3 |
| Heal others | Life 3 |
| Mind control | Mind 4 |
| Create fire | Forces 3 + Prime 2 |
| Step sideways | Spirit 3 |
| See future | Time 2 |

### Sphere Selection Strategy
1. **Start with concept** — What does your mage DO?
2. **Check conjunctions** — What Spheres achieve those effects?
3. **Read detailed files** — What else can those Spheres do at each level?
4. **Consider synergies** — Prime 2 enables creation; Correspondence extends range
5. **Match to Practice** — Your Practice rating must meet your highest Sphere

---

## Focus (Prism of Focus System)

Focus consists of **Tenets** (forming Paradigm) and **Practices** (with ratings).

### Step 9a: Choose Tenets

Select at least 3 Tenets:

| Required Tenet | Purpose | Examples |
|----------------|---------|----------|
| **Metaphysical** | Why magick exists | A Rational Universe, The Divine is Real, Reality is a Lie |
| **Personal** | Why YOU can use magick | I Am Chosen, I Am Special, I Have Greater Understanding |
| **Ascension** | Ultimate purpose of magick | Build a Utopia, Achieve Full Knowledge, Power is its Own Reward |

**Optional Tenets**: Social Role, Epistemology, Openness, Afterlife

**Important**: Arete cannot exceed number of Tenets until Arete 6.

Reference: `lookup.py rules.tenets tenets`

### Step 9b: Choose Practices

- Gain **1 Practice dot per dot of Arete**
- Additional dots cost 1 Freebie each
- Must have **2+ dots in Associated Abilities** per Practice dot

| Rating | Effect Capability |
|--------|-------------------|
| 1 | Perception, sensing |
| 2 | Minor manipulation, self-affecting |
| 3 | Significant effects, affect others |
| 4 | Major transformations |
| 5 | Create from nothing, large-scale |

**Practice-Tenet Interaction**:
- Associated Practice (from Tenet): -1 difficulty
- Limited Practice (from Tenet): +1 difficulty
- Faction Specialized Practice: Always counts as Associated

Reference: `lookup.py rules.practices practices`

### Step 9c: Instruments

Instruments are determined by Practice. Each Practice has a set of **common_instruments** in `lookup.py rules.practices practices`.

When documenting a character's Focus, list all common instruments for each Practice they have.

---

## Allocation Summary

| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Backgrounds | 7 |
| Spheres | 5 + 1 Affinity |
| Arete | 1 (max 3) |
| Willpower | 5 |
| Rotes | 6 dots |
| Freebies | 15 |
| **Tenets** | 3 minimum |
| **Practice dots** | = Arete |

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 (×2 for Sanctum/Enhancement/Totem) |
| Willpower | 1 |
| Sphere | 7 |
| Arete | 4 |
| **New Practice** | 1 |
| **Practice dot** | 1 |
| **Tenet** | 0 |

## Reference Data

```bash
# Faction practices
python scripts/lookup.py rules.faction-practices faction-practices "Verbena"

# Subfaction affinity spheres
python scripts/lookup.py rules.subfactions subfactions "Order of Hermes"

# Tenet details
python scripts/lookup.py rules.tenets tenets "metaphysical"

# Practice details
python scripts/lookup.py rules.practices practices "Alchemy"

# Example paradigms
python scripts/lookup.py rules.paradigms paradigms "A Mechanistic Cosmos"

# Sphere details (PRIMARY - capabilities, conjunctions, vulgarity)
python scripts/lookup.py rules.sphere-details sphere-details "Life 3"
python scripts/lookup.py rules.sphere-details sphere-details --find "heal"

# Quick sphere level lookup (one-line summaries)
python scripts/lookup.py rules.sphere-levels sphere-levels "Forces"
```

### Sphere References (Deep Dives)
For complex edge cases only:
- `references/spheres/[sphere].md` — Extended examples and special rules
- `references/spheres/conjunctions.md` — Effect → Spheres required
- `references/spheres/mechanics.md` — Successes, vulgarity, special rules

### Internal References
- `lookup.py character.attributes attributes`
- `lookup.py character.abilities abilities` — Primary and Secondary Abilities with full details
- `lookup.py character.backgrounds backgrounds`
- `lookup.py character.archetypes archetypes`
- `lookup.py character.merits-flaws merits-flaws` — Merits/Flaws from M20 core and Book of Secrets
- `lookup.py character.genetic-flaws genetic-flaws` — Enhancement rules, Genetic Flaws, Derangements
- `references/character/focus-rules.md`
- `references/character/output-template.md`

### Rules References
- `lookup.py rules.tenets tenets`
- `lookup.py rules.practices practices`
- `lookup.py rules.paradigms paradigms`
- `lookup.py rules.archmastery archmastery`

## Validation

- [ ] Attributes: 15 dots (+ 9 base)
- [ ] Abilities: 27 dots, none > 3
- [ ] Backgrounds: 7 dots
- [ ] Spheres: 6 total, none > Arete
- [ ] Arete ≤ 3
- [ ] **Tenets: 3+ (Metaphysical, Personal, Ascension)**
- [ ] **Arete ≤ number of Tenets**
- [ ] **Practice dots = Arete (minimum)**
- [ ] **2+ Associated Ability dots per Practice dot**
- [ ] Flaws ≤ 7 points
- [ ] Freebies spent exactly
- [ ] (PC) All rotes have documents
- [ ] (PC) All relevant backgrounds have documents:
  - [ ] Library → Library + Grimoire documents
  - [ ] Node → Node document
  - [ ] Sanctum → Sanctum document
  - [ ] Wonder → Wonder document(s)
  - [ ] Chantry → Chantry document
  - [ ] Allies/Retainers → Companion documents
  - [ ] Familiar → Familiar document
- [ ] All links valid

## PC File Structure

```
[character]/
├── [character].md          ← Links to all below
├── rotes/
├── libraries/
│   └── grimoires/
├── nodes/
├── sanctums/
├── wonders/
├── companions/             ← Allies, Retainers, Familiars
└── chantry/                ← If Chantry background
```

## Focus Section Template

Include this section in character documents:

```markdown
## Focus

### Paradigm
**[Paradigm Name or Custom]**

### Tenets
| Type | Tenet |
|------|-------|
| Metaphysical | [Tenet Name] |
| Personal | [Tenet Name] |
| Ascension | [Tenet Name] |
| [Optional] | [Tenet Name] |

### Practices
| Practice | Rating | Benefit | Penalty | Instruments |
|----------|--------|---------|---------|-------------|
| [Name] | [1-5] | [From practices.json] | [From practices.json] | [All common_instruments from practices.json] |
```

Look up each Practice in `lookup.py rules.practices practices` for `common_instruments`, `benefit`, and `penalty`.

---

## Fallen Mages (Book of the Fallen)

Nephandi ARE mages. Use standard character creation with these additions.

### Origin (required for Fallen)

| Type | Description |
|------|-------------|
| **Barabbi** | Converted mage. Had a faction (Tradition/Technocracy/Disparate) before Falling |
| **Widderslainte** | Reborn with Nephandic Avatar from past life. Usually retains former faction memories |
| **Caul-born** | Awakened directly through the Caul into darkness. No prior faction |

### Former Faction

- **Barabbi:** MUST specify which faction they came from (Tradition, Convention, Craft, etc.)
- **Widderslainte:** Usually remember a former faction (Storyteller's choice)
- **Caul-born:** No former faction

This is crucial for characterization—a Fallen Hermetic acts differently than a Fallen Etherite.

### Nephandic Faction (optional)

See `modules/nephandic-faction.md` for the 8 factions:

**Unholy Trinity (well-known):**
- Infernalists, K'llashaa, Malfeans

**Secret Scourge (require Lore: Nephandi 3+ to identify):**
- Baphies (Goatkids), Exies (Obliviates), Heralds of Basilisk, Ironhands, Mammonites

Many Fallen operate independently or in small cabals without formal faction ties. Mark as "Independent" if applicable.

### Nephandic Avatar Essences

When a mage passes through the Caul, their Avatar is transformed:

| Essence | Nature |
|---------|--------|
| Chaotic (Primordial) | Primal chaos, formlessness, the Void before creation |
| Destructive (Dynamic) | Active annihilation, the joy of unmaking |
| Frozen (Static) | Crystallized entropy, the stillness of death |
| Tormented (Questing) | Suffering and seeking, never satisfied |

### Qlippothic Status

Track which Qlipha the character has reached (see `modules/qlippoth.md`):

| Status | Meaning |
|--------|---------|
| Pre-Caul | On the path but hasn't passed through Daath |
| Lilith - Gha'ag Sheblah | Standard post-Caul progression (stages 10-4) |
| Post-Daath | Satariel, Ghagiel, Thaumiel (stages 3-1, extremely powerful) |

**Note:** Arete and Qlippothic stage don't map 1:1. A mage might be stuck at a stage while advancing Arete.

### Focus Considerations

**Paradigms:** Use standard paradigms from `lookup.py rules.paradigms paradigms`. Fallen paradigms often feature:
- "Annihilation is Freedom" Ascension Tenet
- Emphasis on predation, power, and transgression

**Practices:** Use corrupted versions in `lookup.py rules.practices practices`:
- Abyssalism, Black Mass, Demonism, Goetia, Vamamarga, Feralism, Infernal Sciences

**Malign Instruments:** In addition to standard instruments:
- Atrocity, Perversion, Mutilation, Torment, Trolling/Cyberbullying, Violation

### Nephandic Merits & Flaws

See `lookup.py character.merits-flaws merits-flaws` for full details:

| Trait | Type | Cost |
|-------|------|------|
| Shadow Appeal | Merit | 1-3 |
| Innocuous Aura | Merit | 5 |
| Abyssal Mastery | Merit | 5 |
| Saint of the Pit | Merit | 7 |
| Qlippothic Radiance | Flaw | 1-5 |
| Spectral Presence | Flaw | 3 |
| Abyssal Lunatic | Flaw | 5 |
| Widderslainte (Taint of Corruption) | Flaw | 7 |

### Additional Validation (if Fallen)

- [ ] Origin type specified (barabbi/widderslainte/caul-born)
- [ ] Former faction specified (if barabbi or widderslainte with memories)
- [ ] Nephandic Avatar essence assigned
- [ ] Qlippothic status noted
- [ ] Uses at least one corrupted practice or Maleficia
- [ ] Any Nephandic Merits/Flaws properly costed
