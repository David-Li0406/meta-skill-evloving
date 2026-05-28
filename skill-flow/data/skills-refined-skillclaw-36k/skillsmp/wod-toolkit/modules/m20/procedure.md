# Procedure Module

Create Procedures (blatant) and Adjustments (subtle) for Technocratic characters.

## When to Use

Use this module instead of `rote.md` when creating magical effects for:
- Technocracy operatives
- Technocratic equipment powers
- Any effect framed in Technocratic paradigm

## Procedure vs Adjustment

| Type | Vulgarity | Masses Reaction | Risk |
|------|-----------|-----------------|------|
| **Adjustment** | Subtle | Accept as normal technology | Low Paradox |
| **Procedure** | Blatant | Cannot rationalize | Full Paradox |

### Adjustments (Preferred)

Effects the Masses can accept as advanced (but possible) technology:
- Enhanced surveillance (Data/Mind)
- Faster-than-normal hacking (Data)
- Exceptional marksmanship (Entropy/Forces)
- Persuasion techniques (Mind)
- Advanced medical treatment (Life)
- Superior materials analysis (Matter)

### Procedures (Emergency Only)

Effects that violate consensus beliefs:
- Teleportation (Correspondence 3+)
- Blatant mind control (Mind 4+)
- Creating matter from nothing (Matter 3 + Prime 2)
- Visible energy manipulation (Forces 3+ without concealment)
- Dimensional travel (Dimensional Science 3+)

**Rule:** Most starting Technocrats should have 4-5 Adjustments and 1-2 Procedures.

---

## Creation Workflow

1. **Name** — Technical designation (e.g., "Neural Pattern Disruption Protocol")
2. **Type** — Adjustment or Procedure
3. **Spheres** — Use Technocratic names (Data, Dimensional Science)
4. **Effect** — What it does, framed technologically
5. **Apparatus** — REQUIRED equipment to perform
6. **System** — Dice pools, difficulties, successes needed
7. **Vulgar/Coincidental** — Context matters (same effect can be either)
8. **Document** — Full write-up

---

## Technocratic Sphere Names

| Traditional | Technocratic | Notes |
|-------------|--------------|-------|
| Correspondence | Data | Information location/transfer |
| Spirit | Dimensional Science | Umbra, spirits, Gauntlet |
| Entropy | Entropy | Same |
| Forces | Forces | Same |
| Life | Life | Same |
| Matter | Matter | Same |
| Mind | Mind | Same |
| Prime | Prime | Often called "Primal Energy manipulation" |
| Time | Time | Same (rare among Technocrats) |

---

## Sample Adjustments (from Technocracy: Reloaded)

### The Master's Edge (Mind 2; +Entropy 1-2)
**Type:** Adjustment
**Apparatus:** Eye contact, social positioning, possibly smart drugs
**Effect:** Manipulate target's emotional state through body language and non-verbal cues. Reduces difficulty of social rolls.

**System:**
- Roll Enlightenment vs target's Willpower (min difficulty 4)
- Target resists with Willpower (difficulty 6)
- Net successes reduce difficulty of related social rolls by up to 3
- With Entropy 1: Gain insight into target's responses (+1 to target's resist difficulty)
- With Entropy 2: Environmental factors enhance mood (can split successes)

### Frequency Analysis (Dimensional Science 1/Forces 1/Prime 1)
**Type:** Adjustment
**Apparatus:** Field Material Analyzer (FMA)
**Effect:** Detect extradimensional energies or Primal Energy signatures in a sample.

### Mass Spectrometry (Entropy 1/Life 1/Matter 1)
**Type:** Adjustment
**Apparatus:** Field Material Analyzer (FMA)
**Effect:** Determine complete biological and material composition of a sample. Destroys sample.

### Quantum Analysis (Data 1/Mind 1/Time 1)
**Type:** Adjustment
**Apparatus:** Field Material Analyzer (FMA)
**Effect:** Detect Data connections, emotional resonance, and temporal anomalies in a sample.

---

## Sample Procedures (from Technocracy: Reloaded)

### All Triggers Locked (Forces 2/Matter 2)
**Type:** Procedure (EXTREMELY VULGAR)
**Apparatus:** None visible—pure Enlightened will channeled through hands
**Effect:** Snatch all firearms in area, merge into single weapon, fire simultaneously.

**System:**
- Difficulty 7, requires 6+ successes
- 3 turns: grab (turn 1), fuse (turn 2), fire (turn 3)
- 15-foot half-circle blast area
- 7 dice lethal damage per turn for 3 turns to everyone in area
- Considered measure of absolute last resort

### Memory Stabilization (Mind 3)
**Type:** Procedure
**Apparatus:** Neuro-Optical Transmitter (NOT / "Flashy Thing")
**Effect:** Erase memories of Reality Deviance, replace with consensus-acceptable memories.

**System:**
- Target witnesses anomalous event
- NOT flashes, roll activation
- Successes determine completeness of memory replacement
- Higher Mind levels allow more sophisticated alterations

### Pandimensional Anomaly Shutdown (Dimensional Science 3/Forces 3/Life 4/Prime 2)
**Type:** Procedure
**Apparatus:** PAWS Taser
**Effect:** Force shapeshifter into human form by disrupting dimensional carrier waves.

**System:**
- Attack roll: Dexterity + Energy Weapons, difficulty 7
- On hit: Target forced into Homid form
- Also inflicts electrocution damage
- Typically coincidental (witnesses see "powerful taser" vs monster)

### Dimensional Exile (Correspondence 4/Dimensional Science 4/Entropy 2)
**Type:** Procedure
**Apparatus:** NIMBY-50
**Effect:** Banish target to random Umbral location.

**System:**
- Attack: Dexterity + Energy Weapons, difficulty 7
- Targets with Gnosis/Pathos: Sent to random Umbra location
- Targets without: Teleported several miles in random direction
- Net successes = turns target cannot step sideways

---

## Apparatus Requirements

**CRITICAL:** Technocrats CANNOT perform Procedures or Adjustments without appropriate apparatus.

### Common Apparatus by Convention

| Convention | Typical Apparatus |
|------------|-------------------|
| **Iteration X** | Computers, cybernetics, weapons, tools |
| **NWO** | Suits, badges, phones, surveillance gear |
| **Progenitors** | Lab equipment, medical devices, syringes |
| **Syndicate** | Money, cards, phones, contracts |
| **Void Engineers** | Ships, suits, weapons, alien tech |

### Documenting Apparatus

Every Procedure/Adjustment must list:
1. Primary apparatus (required)
2. Secondary apparatus (optional enhancements)
3. What happens without apparatus (nothing—effect fails)

---

## Naming Conventions

Use technical, clinical language:

| Mystic Style | Technocratic Style |
|--------------|-------------------|
| Fireball | Directed Energy Discharge |
| Mind Control | Neural Pattern Override |
| Teleport | Spatial Translocation Protocol |
| Healing | Accelerated Cellular Regeneration |
| Scrying | Remote Surveillance Interface |
| Spirit Summoning | Extradimensional Entity Manifestation |
| Enchantment | Primal Energy Infusion |

---

## Output Template

```markdown
# [Procedure/Adjustment Name]

**Type:** [Adjustment/Procedure]
**Spheres:** [Sphere N, Sphere N]
**Convention:** [Primary Convention that uses this]

## Effect
[Technical description of what happens]

## Apparatus Required
- **Primary:** [Main equipment needed]
- **Secondary:** [Optional enhancements]

## System
**Roll:** [Attribute + Ability]
**Difficulty:** [Base difficulty]
**Duration:** [How long effect lasts]

[Detailed mechanics]

## Vulgarity Assessment
- **With witnesses:** [Adjustment/Procedure]
- **Without witnesses:** [Adjustment/Procedure]
- **Rationale:** [Why Masses would/wouldn't accept this]

## Variations
[Convention-specific variations if any]
```

---

## Reference Data

```bash
# Sphere capabilities
python scripts/lookup.py rules.sphere-details sphere-details "Mind 3"

# Common conjunctions
cat references/spheres/conjunctions.md

# Technocratic equipment (for apparatus)
python scripts/lookup.py technocracy.equipment equipment "NOT"
```

---

## Validation

- [ ] Type specified (Adjustment or Procedure)
- [ ] Spheres use Technocratic names where applicable
- [ ] Effect described in technical language
- [ ] Apparatus listed (cannot be "none" for Technocrats)
- [ ] System mechanics complete
- [ ] Vulgarity assessment included
- [ ] Naming follows technical conventions

---

## File Structure

```
[operative]/
├── [operative].md
└── procedures/
    ├── neural_pattern_override.md
    ├── spatial_translocation.md
    └── accelerated_regeneration.md
```

---

## Linking in Character Documents

```markdown
## Procedures

| Procedure | Spheres | Type | Document |
|-----------|---------|------|----------|
| [Neural Override](./procedures/neural_override.md) | Mind 3 | Procedure | Mental control |
| [Data Intercept](./procedures/data_intercept.md) | Data 2 | Adjustment | Remote hacking |
```
