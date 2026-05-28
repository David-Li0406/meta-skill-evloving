# Technocrat Module

Create mechanically valid Technocratic Union characters for M20.

## When to Use This Module

Use this module (not `character.md`) when creating:
- Any Technocracy character (Enlightened or unEnlightened)
- Agents, operatives, supervisors of any Convention
- HIT Marks, clones, androids (see also `modules/technocratic-being.md`)

## Key Differences from Tradition Mages

| Element | Tradition Mage | Technocrat |
|---------|---------------|------------|
| Primary Stat | Arete | Enlightenment |
| Magic Effects | Rotes | Procedures/Adjustments |
| Coincidental | Can become unfocused | Always requires apparatus |
| Organization | Tradition + Sect | Convention + Methodology |
| Rank | Informal | 6TP System (T0-T5) |
| Focus Binding | Can transcend tools | **Permanently bound to apparatus** |
| Quintessence | Quintessence | Primal Energy |
| Avatar | Avatar | Genius |
| Chantry | Chantry | Construct |
| Cabal | Cabal | Amalgam |

**CRITICAL:** Technocrats can NEVER cast magic without their apparatus. This is permanent and cannot be transcended.

## PC vs NPC

| Type | Linked Documents | When |
|------|------------------|------|
| **PC** (default) | REQUIRED | Standard creation |
| **NPC** | Not required | "NPC", "quick", "simple", "stat block" |

## Dependencies (PC Only)

**Read `modules/background-expansion.md` for background → module mapping.**

| Background | Action |
|------------|--------|
| (all PCs) | Read `modules/procedure.md`, create Procedures |
| Requisitions | Equipment via `modules/technocratic-equipment.md` |
| Construct | Read `modules/construct.md` |
| Node, Sanctum | See `modules/background-expansion.md` |
| Allies, Retainers | See `modules/background-expansion.md` |

## Creation Steps

1. **PC/NPC** — Default PC
2. **Convention** — One of five (see Convention Selection)
3. **Methodology** — Subdivision of Convention
4. **6TP Rank** — T0 through T5 (see Rank System)
5. **Concept** — Name, role, specialty, affinity Sphere
6. **Nature & Demeanor** — From `lookup.py character.archetypes archetypes`
7. **Attributes** — 7/5/3 across Physical/Social/Mental
8. **Abilities** — 13/9/5 across Talents/Skills/Knowledges (cap 3)
9. **Backgrounds** — 7 dots (use Technocratic versions)
10. **Enlightenment** — Base 1, max 3 with freebies (4/dot)
11. **Spheres** — Use Technocratic names. 1 free Affinity + 5 dots (capped at Enlightenment)
12. **Focus** — See Technocratic Focus section (permanently bound)
13. **Resonance** — 1 trait, rating 1-5
14. **⛔ PROCEDURES (PC)** — Read `modules/procedure.md`, create 6 dots worth
15. **Merits & Flaws** — From `lookup.py character.merits-flaws merits-flaws`
16. **⛔ EQUIPMENT (PC)** — Via `modules/technocratic-equipment.md`
17. **Freebies** — 15 + Flaws - Merits. Spend exactly.
18. **Derived** — Willpower 5+, Primal Energy = Genius, Paradox 0
19. **Document** — Link all sub-documents
20. **Validate**

---

## Convention Selection

| Convention | Focus | Affinity Spheres |
|------------|-------|------------------|
| **Iteration X** | Technology, machines, mathematics | Data (Corr), Forces, Matter, Prime |
| **New World Order** | Information, control, social engineering | Data (Corr), Entropy, Mind |
| **Progenitors** | Biology, genetics, medicine | Entropy, Life, Mind, Prime |
| **Syndicate** | Economics, desire, wealth | Entropy, Mind, Prime |
| **Void Engineers** | Space, dimensions, exploration | Correspondence, Dimensional Science (Spirit), Forces |

### Technocratic Sphere Names

| Traditional | Technocratic |
|-------------|--------------|
| Correspondence | Data (or Dimensional Science for spatial) |
| Spirit | Dimensional Science |
| All others | Same names |

Reference: `lookup.py technocracy.conventions conventions`

---

## Methodology Selection

Select one Methodology within your Convention:

### Iteration X
| Methodology | Focus |
|-------------|-------|
| BioMechanics | Cyborg integration, human-machine interface |
| Macrotechnicians | Large-scale systems, climate, infrastructure |
| Statisticians | Mathematics, predictions, Time Tables |
| TMM (Time-Motion Managers) | Manufacturing, quantum physics, nanotech |

### New World Order
| Methodology | Focus |
|-------------|-------|
| The Ivory Tower (Watchers) | Intelligence gathering, analysis |
| Q Division (Operatives) | Field operations, enforcement |
| The Feed | Media control, propaganda |
| Neutralization Specialists | Elimination of threats |

### Progenitors
| Methodology | Focus |
|-------------|-------|
| Applied Sciences | Practical field application |
| Damage Control | Crisis response, cleanup |
| FACADE Engineers | Clones, constructs, surgery |
| Genegineers | Genetic modification, evolution |
| Pharmacopoeists | Drugs, chemical enhancement |

### Syndicate
| Methodology | Focus |
|-------------|-------|
| Disbursements | Resource allocation, Union funding |
| Enforcers | Criminal networks, "Hollow Men" |
| Financiers | Global economics, market manipulation |
| Media Control | Desire management, advertising |
| Special Projects Division | [CLASSIFIED] |

### Void Engineers
| Methodology | Focus |
|-------------|-------|
| BCD (Border Corps Division) | Gauntlet defense, Earthside |
| EFD (Earth Frontier Division) | Search and rescue |
| NSC (Neutralization Specialist Corps) | Combat, threat elimination |
| PDC (Pan-Dimensional Corps) | Deep space/Umbra exploration |
| REC (Research and Execution) | R&D, alien tech |

Reference: `lookup.py technocracy.methodologies methodologies`

---

## 6TP Rank System

| Rank | Title | Description | Enlightened? |
|------|-------|-------------|--------------|
| **T0** | Affiliate/Citizen | Support personnel, unaware masses | No |
| **T1** | Operative (Low-Light) | Field agents, basic clearance | Usually No |
| **T1+** | Initiated Operative | Low-Light with Enlightenment | Yes |
| **T2** | Agent | Full operative status | Yes |
| **T3** | Supervisor | Construct/team management | Yes |
| **T4** | Symposium Member | Regional authority | Yes |
| **T5** | Upper Management | Convention leadership | Yes |

### Rank Effects

| Rank | Starting Resources | Security Clearance |
|------|-------------------|-------------------|
| T0 | Minimal | None |
| T1 | Standard field kit | Low |
| T2 | Full requisitions access | Medium |
| T3 | Construct resources | High |
| T4+ | Convention resources | Maximum |

**Starting PCs:** Usually T1 (Initiated) or T2.

---

## Technocratic Backgrounds

Use these instead of/in addition to standard backgrounds:

| Background | Replaces | Description |
|------------|----------|-------------|
| **Genius** | Avatar | Connection to Enlightened understanding |
| **Requisitions** | Wonder | Access to Technocratic equipment |
| **Secret Weapons** | — | Personal hypertech cache |
| **Cloaking** | Arcane | Institutional erasure of identity |
| **Clearance** | — | Security access level |

Standard backgrounds that apply:
- Allies, Contacts, Influence, Resources, Retainers
- Node (yes, the Technocracy uses Nodes)
- Sanctum (personal lab/office)
- Library (databases, archives)

Reference: `lookup.py character.backgrounds backgrounds`

---

## Technocratic Focus

### CRITICAL: Permanent Apparatus Dependency

Unlike mystic mages, **Technocrats can NEVER transcend their instruments**. A Technocrat without their apparatus is powerless. This is not a limitation to overcome—it is fundamental to Technocratic paradigm.

### Paradigms (Common)

| Paradigm | Description |
|----------|-------------|
| A Mechanistic Cosmos | Reality is a machine following rules |
| Tech Holds All Answers | Technology reveals truth |
| Everything is Data | Reality is information to be processed |
| A World of Gods and Monsters | We fight supernatural threats |
| Embrace the Threshold | Evolution/transformation is key |
| A Holographic Reality | Physical world is simulation |

Reference: `lookup.py technocracy.focus focus`

### Practices (Common)

| Practice | Primary Conventions |
|----------|---------------------|
| Hypertech | All (primary) |
| Cybernetics | Iteration X, Progenitors, Void Engineers |
| Dominion | NWO, Syndicate |
| Reality Hacking | Iteration X, Virtual Adepts allies |
| Weird Science | Void Engineers, Progenitors |
| Art of Desire/Hypereconomics | Syndicate |
| Martial Arts | NWO, Iteration X |
| Psionics | NWO (some) |

### Instruments (Apparatus)

All Technocrats use technological apparatus:

| Category | Examples |
|----------|----------|
| Computer Gear | Laptops, tablets, ES-Phones, VDAS |
| Devices and Machines | Lab equipment, vehicles, weapons |
| Cybernetic Implants | Neural jacks, enhanced limbs |
| Formulae and Math | Calculations, algorithms |
| Labs and Gear | Research equipment |
| Fashion | Suits, uniforms (NWO especially) |
| Drugs and Poisons | Pharmacopoeist specialty |
| Weapons | Energy weapons, firearms |

Reference: `lookup.py technocracy.focus focus`

---

## Allocation Summary

| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Backgrounds | 7 |
| Spheres | 5 + 1 Affinity |
| Enlightenment | 1 (max 3) |
| Willpower | 5 |
| Procedures | 6 dots |
| Freebies | 15 |
| **Tenets** | 3 minimum |
| **Practice dots** | = Enlightenment |

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 (×2 for Sanctum/Enhancement) |
| Willpower | 1 |
| Sphere | 7 |
| Enlightenment | 4 |
| New Practice | 1 |
| Practice dot | 1 |

---

## Procedures vs Adjustments

| Type | Vulgarity | Masses React |
|------|-----------|--------------|
| **Adjustment** | Subtle | Accept as normal |
| **Procedure** | Blatant | Cannot rationalize |

Starting Technocrats should have mostly Adjustments with 1-2 Procedures for emergencies.

See `modules/procedure.md` for creation details.

---

## Reference Data

```bash
# Conventions
python scripts/lookup.py technocracy.conventions conventions "Iteration X"

# Methodologies
python scripts/lookup.py technocracy.methodologies methodologies "FACADE"

# Technocratic Focus
python scripts/lookup.py technocracy.focus focus "Hypertech"

# Equipment
python scripts/lookup.py technocracy.equipment equipment "ES-Phone"

# Standard references also apply
python scripts/lookup.py character.merits-flaws merits-flaws "Enhanced"
python scripts/lookup.py rules.sphere-details sphere-details "Forces 3"
```

---

## Validation

- [ ] Convention and Methodology specified
- [ ] 6TP Rank appropriate for character type
- [ ] Attributes: 15 dots (+ 9 base)
- [ ] Abilities: 27 dots, none > 3
- [ ] Backgrounds: 7 dots (using Technocratic versions)
- [ ] Spheres: 6 total, none > Enlightenment
- [ ] Enlightenment ≤ 3
- [ ] Tenets: 3+ (Metaphysical, Personal, Ascension)
- [ ] Enlightenment ≤ number of Tenets
- [ ] Practice dots = Enlightenment (minimum)
- [ ] 2+ Associated Ability dots per Practice dot
- [ ] All apparatus documented (cannot cast without them)
- [ ] Flaws ≤ 7 points
- [ ] Freebies spent exactly
- [ ] (PC) All Procedures have documents
- [ ] (PC) Equipment requisitioned via proper module
- [ ] All links valid

---

## PC File Structure

```
[operative]/
├── [operative].md          ← Links to all below
├── procedures/
├── equipment/
├── companions/             ← Enhanced beings, constructs
└── construct/              ← If part of a Construct
```

---

## Terminology Reference

Always use Technocratic terminology in character documents:

| Instead of... | Use... |
|---------------|--------|
| Arete | Enlightenment |
| Rote | Procedure (blatant) or Adjustment (subtle) |
| Quintessence | Primal Energy |
| Avatar | Genius |
| Awakening | Enlightenment (the event) |
| Seeking | Requisitions Review / Performance Evaluation |
| Vulgar magic | Procedure |
| Coincidental magic | Adjustment |
| Chantry | Construct |
| Cabal | Amalgam |
| Tradition | Convention |
| Willworker | Operative / Agent |
| Sleeper | Citizen / The Masses |
| Reality Deviant | RD (any non-Technocratic Awakened) |

---

## Output Template

```markdown
# [Operative Name]

**Convention:** [Convention] | **Methodology:** [Methodology]
**Rank:** [T0-T5] | **Enlightenment:** [X] | **Willpower:** [X]

## Concept
[Role, background, specialty]

## Attributes

### Physical
Strength ●●○○○ | Dexterity ●●●○○ | Stamina ●●○○○

### Social
Charisma ●●○○○ | Manipulation ●●●○○ | Appearance ●●○○○

### Mental
Perception ●●●○○ | Intelligence ●●●●○ | Wits ●●●○○

## Abilities
[Organized by Talents/Skills/Knowledges]

## Backgrounds
| Background | Rating | Notes |
|------------|--------|-------|
| Genius | ●●○○○ | |
| Requisitions | ●●●○○ | [Link to equipment] |

## Spheres
| Sphere | Rating | Notes |
|--------|--------|-------|
| Data | ●●○○○ | Affinity |
| Forces | ●●●○○ | |

## Focus

### Paradigm
**[Paradigm Name]**

### Tenets
| Type | Tenet |
|------|-------|
| Metaphysical | [Tenet] |
| Personal | [Tenet] |
| Ascension | [Tenet] |

### Practices
| Practice | Rating | Instruments |
|----------|--------|-------------|
| Hypertech | ●●○○○ | Computer gear, devices, labs |

### Apparatus (REQUIRED)
[List ALL instruments needed to use magic—character is powerless without these]

## Procedures

| Procedure | Spheres | Type | Document |
|-----------|---------|------|----------|
| [Name](./procedures/file.md) | Data 2 | Adjustment | Brief effect |

## Equipment

| Item | Category | Document |
|------|----------|----------|
| [ES-Phone](./equipment/es_phone.md) | Device | Standard field kit |

## Merits & Flaws

## Resonance
**[Trait]** ●●○○○

## Description
[Physical appearance, typical attire, mannerisms]

## History
[Background, recruitment, notable operations]
```
