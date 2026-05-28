# Focus Rules (Prism of Focus)

Focus represents how a mage understands and performs magick. Under the Prism of Focus system, Focus consists of **Tenets** (which form the Paradigm) and **Practices** (which have ratings and mechanical effects).

## Paradigm

A mage's Paradigm is built from **Tenets** - specific beliefs they hold deeply. These form the foundation of how they understand reality and magick.

### Required Tenets

Every mage must have at least **three** Tenets at character creation:

| Tenet Type | Question Answered | Required? |
|------------|-------------------|-----------|
| **Metaphysical** | Why does magick exist? How does the universe work? | Yes |
| **Personal** | Why can I use magick when others cannot? | Yes |
| **Ascension** | What is the ultimate purpose of magick? | Yes |

### Optional Tenets

Additional Tenets can clarify other aspects of belief:

| Category | Examples |
|----------|----------|
| **Social Role** | I Illuminate, I Rule, I Serve |
| **Epistemology** | Mystical Insights, Scientific Experimentation, Divine Revelations |
| **Openness** | Closed Paradigm, Hierarchical Paradigm, Open Paradigm |
| **Afterlife** | Reincarnation, YOLO |

### Tenet Rules

- **Cost**: Acquiring new Tenets is free. Removing or replacing costs XP equal to current number of Tenets.
- **Arete Limit**: Arete cannot exceed the number of Tenets until Arete reaches 6.
- **Practice Bonuses**: Each Tenet has Associated and Limited Practices that affect difficulty.

### Tenet-Practice Interactions

- **Associated Practice**: -1 difficulty when using that Practice
- **Limited Practice**: +1 difficulty when using that Practice
- **Conflict**: If a Practice is Associated with one Tenet but Limited by another, no modifier applies

See `references/rules/tenets.json` for complete Tenet listings with Associated/Limited Practices.

---

## Practices

Practices are the **how** of magick - the methods and techniques a mage uses. Under Prism of Focus, Practices have **ratings from 0 to 5** (and higher for Archmages).

### Practice Ratings

| Rating | Capability |
|--------|------------|
| 0 | Cannot use this Practice |
| 1 | Basic effects (sensing, minor manipulation) |
| 2 | Minor effects (self-affecting, simple changes) |
| 3 | Significant effects (affecting others, notable changes) |
| 4 | Major effects (transformations, permanent changes) |
| 5 | Mastery (create from nothing, large-scale effects) |
| 6+ | Archmaster powers (see Archmastery rules) |

### Acquiring Practices

| Method | Cost |
|--------|------|
| Starting Arete | 1 Practice dot per Arete dot |
| New Practice (Freebies) | 1 |
| Raise Practice (Freebies) | 1 per dot |
| New Practice (XP) | 3 |
| Raise Practice (XP) | Current Rating |

**Ability Requirement**: Must have at least 2 dots in an Associated Ability for each dot of Practice.

### Practice Effects on Magick

- **Effect Limit**: Cannot perform effects higher than your Practice rating
- **Rituals**: Ritual Master's Practice × Willpower = maximum successes
- **Rotes**: Rotes are tied to specific Practices at creation
- **Sanctums**: Sanctum rating grants Practice dots (affects what's Coincidental)
- **Reality Zones**: Can boost or limit specific Practices

### Practice Benefits & Penalties

Every Practice has:
- **Benefit**: Situational difficulty reduction or special ability
- **Penalty**: Situational difficulty increase or limitation

See `references/rules/practices.json` for all Practice details.

### Specialized Practices

Some factions have unique variants of base Practices:

| Base Practice | Specialization | Faction |
|---------------|----------------|---------|
| Alchemy | The Royal Art | Children of Knowledge |
| Animalism | Feralism (Corrupted) | — |
| Art of Desire | Hypereconomics | Syndicate |
| Craftwork | Weaving | Taftani |
| Crazy Wisdom | Occultation | Ahl-i-Batin |
| Cybernetics | Integrative Technology | Iteration X |
| Dominion | Authority | New World Order |
| Elementalism | Wayfinding | Kopa Loei |
| Faith | Harmony | Celestial Chorus |
| Faith | Gladius Domini | Templar Knights |
| Gutter Magick | The Scene | Hollow Ones |
| High Ritual Magick | Ceremonial Magick | Order of Hermes |
| High Ritual Magick | Nyeredzi | Ngoma |
| High Ritual Magick | Bureaucracy | Wu Lung |
| Hypertech | Tecknology | Void Engineers |
| Invigoration | Lakashim | Cult of Ecstasy |
| Martial Arts | Do | Akashayana |
| Medicine-Work | Biotech | Progenitors |
| Medicine-Work | Artemis's Gift | Sisters of Hippolyta |
| Reality Hacking | Reality Coding | Virtual Adepts |
| Shamanism | Spirit Ties | Dreamspeakers |
| Voudoun | Asagwe | Bata'a |
| Weird Science | Ethertech | Society of Ether |
| Witchcraft | The Old Ways | Verbena |
| Yoga | Wheel-Tending | Euthanatos |

Specialized Practices:
- Count as the base Practice for Sanctums, Reality Zones, and rituals
- Are always considered Associated for faction members
- Grant an additional unique benefit

### Corrupted Practices

Dark variants that offer power at terrible cost:

| Corrupted | Base | Price |
|-----------|------|-------|
| Feralism | Animalism | Increasing social penalties with civilization |
| Abyssalism | Crazy Wisdom | Loss of identity and meaning |
| The Black Mass | Faith | Cannot enter holy ground |
| Goetia | High Ritual Magick | Demonic attention and debt |
| Infernal Sciences | Hypertech | Requires souls to power |
| Demonism | Shamanism | Natural spirits refuse contact |
| Vamamarga | Yoga | Addiction and social dysfunction |

**Corruption Mechanic**: Each use requires Practice roll (diff 3 + highest Sphere). Failure = 1 dot Corrupted Resonance. When Corrupted Resonance equals Practice rating, the Practice is replaced by its Corrupted version.

---

## Sanctums and Reality Zones

### Sanctum Integration

For each dot of Sanctum background:
- Gain one dot in a Practice (includes materials needed)
- Magick using that Practice within the Sanctum is always Coincidental
- One level of a different Practice can be made anathema (effects with Spheres ≥ 6-rating become vulgar)

### Reality Zone Practice Ratings

Reality Zones have Practice ratings from -5 to +5:
- **Positive ratings**: Low-level uses (≤ rating) are Coincidental
- **Negative ratings**: High-level uses (≥ 6-|rating|) are Vulgar

*Example: A Hollow One club with Gutter Magick 4 and Hypertech -3 makes most street magic coincidental while making Technocracy effects vulgar.*

---

## Rituals

### Ritual Roles

| Role | Requirements | Contribution |
|------|--------------|--------------|
| **Ritual Master** | Highest Practice rating | Designs ritual, Practice × Willpower = max successes, rolls Arete |
| **Full Participant** | 1+ dots in Practice | May contribute Spheres, rolls Arete (capped by Practice) |
| **Assistant** | 0 dots in Practice | Adds 1 success, makes mundane rolls using Associated Abilities |

### Ritual Mechanics

1. Choose Practice for the ritual
2. Select Ritual Master (usually highest Practice rating)
3. Participants contribute Spheres if Practice rating allows
4. Each participant rolls per the ritual timing
5. Total successes cannot exceed Master's Practice × Willpower

---

## Rotes (Prism of Focus)

### Creating Rotes

1. Define the effect and required Spheres
2. Assign to a Practice (must have sufficient rating)
3. Define how the Practice is used (instruments, actions)
4. Choose dice pool: Attribute + Ability (Ability must be Associated with Practice)
5. Calculate cost: Total Sphere dots required

### Rote Costs

| Source | Cost |
|--------|------|
| Learning from scratch | Sphere dot total |
| Learning from teacher/grimoire | Half sphere dot total |
| **Requirement**: Mentor/Library/Grimoire rating must be at least 1 higher than highest Sphere in rote |

### Starting Rotes

Characters begin with **6 points** of rotes.
Additional points: 4 Freebies = 1 rote point, or 3 XP = 1 rote point

---

## Character Creation Summary

### Focus Selection (Step Four)

1. Choose a **Metaphysical Tenet**
2. Choose a **Personal Tenet**
3. Choose an **Ascension Tenet**
4. Choose **one dot of Practices per dot of Arete**

### Cost Summary

| Trait | Freebies | XP |
|-------|----------|-----|
| New Tenet | 0 | 0 |
| Replace/Remove Tenet | N/A | # of Tenets |
| New Practice | 1 | 3 |
| Raise Practice | 1 | Current Rating |

### Focus Validation

- [ ] At least 3 Tenets (Metaphysical, Personal, Ascension)
- [ ] Arete ≤ number of Tenets (until Arete 6)
- [ ] Practice dots equal to Arete (minimum)
- [ ] 2+ dots in Associated Abilities per Practice dot
- [ ] 6+ rote dots assigned
- [ ] Practices match paradigm concept

---

## Example Focus Configurations

### Hermetic Mage (Order of Hermes)
- **Metaphysical**: A Rational Universe
- **Personal**: I Have Greater Understanding
- **Ascension**: Achieve Full Knowledge
- **Practices**: Ceremonial Magick 3
- **Instruments**: Wand, ritual circle, Enochian, grimoire, planetary hours, incense, robes

### Virtual Adept
- **Metaphysical**: A Rational Universe
- **Personal**: I Am Not Limited
- **Ascension**: Achieve Full Knowledge
- **Practices**: Reality Coding 3
- **Instruments**: Computer, VR rig, code, mathematical formulas, network access

### Verbena Witch
- **Metaphysical**: The Divine is Real
- **Personal**: I Am Special
- **Ascension**: Merge With The Divine
- **Practices**: The Old Ways 3
- **Instruments**: Athame, cauldron, blood, herbs, moon phases, dance, sacred grove

### Syndicate Executive
- **Metaphysical**: Unfathomable Forces at Work
- **Personal**: I Am Not Limited
- **Ascension**: Power is its Own Reward
- **Additional**: I Rule, Open Paradigm
- **Practices**: Hypereconomics 3, Dominion 2
- **Instruments**: Contracts, market data, authority symbols, luxury items

---

## Reference Files

- `references/rules/tenets.json` — Complete Tenet listings with practice associations
- `references/rules/practices.json` — All Practices with benefits, penalties, instruments
- `references/rules/paradigms.json` — Example Paradigms broken into Tenets
- `references/rules/archmastery.json` — Archmage, Exemplar, and Oracle rules
- `references/rules/faction-practices.json` — Faction → Practice mappings
