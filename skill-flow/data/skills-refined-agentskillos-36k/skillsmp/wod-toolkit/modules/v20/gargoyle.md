# Gargoyle Module

Create mechanically valid Gargoyle characters for V20, including variants and special rules.

## Overview

Gargoyles are artificial vampires created by Tremere blood magic in the 12th century. They were originally slaves but won freedom after the Montmartre Pact of 1489. They are:

- Created from Gangrel, Nosferatu, and Tzimisce blood
- Capable of flight (unique among vampires)
- Stone-skinned and monstrous in appearance
- Susceptible to mind control

## Creation Method

Gargoyles can be created two ways:

### 1. Ritual Creation (At Our Command It Breathes)
- Created via Tremere Level 5 Thaumaturgy ritual
- Original method, produces "pure" Gargoyles
- **Creates infertile Gargoyles** (cannot Embrace)
- Tremere officially ceased this practice after the Montmartre Pact

**Ritual Details** (from *Rites of the Blood*):

**Requirements**:
- At least 2 vampires of Nosferatu, Tzimisce, or Gangrel Clans
- Subjects must be prepared for a full lunar month
- Fed small amounts of cursed/defiled blood
- Starved to near-wassail
- Tortured nightly to break sanity

**Process**:
1. Stake prepared subjects
2. Dismember victims (ritual prevents dust)
3. Sew bodies together into humanoid shape
4. Wrap in stretched womb of deer or horse
5. Leave undisturbed for 3 months
6. Perform nightly incantations throughout

**System**:
- Blood cost: 5 points per Cainite used
- Final roll: Intelligence + Occult (difficulty 9), needs 3 successes
- -1 die for each missed night of incantations
- **Morality cost**: Lose 1 point from morality path (regardless of path)
- Single success = viable Gargoyle
- Failure = fetal Gargoyle dies, cannot be revived

**Created Gargoyles**: Use standard character creation rules but are absolutely infertile.

### 2. Embrace
- Free Gargoyles learned to Embrace (origin unknown)
- Childer are true Gargoyles with all bloodline traits
- **Embrace erases childe's memories**
- More common in modern nights
- Produces fertile Gargoyles (can Embrace others)

**For character creation, both methods use the same character creation rules.**

### The Montmartre Pact (1489)
- Formally granted Gargoyle freedom
- Tremere agreed to cease creating new Gargoyles
- Ritual creation now technically forbidden
- Some chantries secretly continue experiments

---

## Variant Selection

Gargoyles come in three distinct variants, each with different in-Clan Disciplines and weaknesses:

### Standard Gargoyle
| Trait | Value |
|-------|-------|
| **Disciplines** | Flight, Fortitude, Visceratika |
| **Weakness** | Willpower treated as 2 lower for resisting mind control |
| **Role** | General purpose |

### Scout Gargoyle
| Trait | Value |
|-------|-------|
| **Disciplines** | Auspex, Obfuscate, Flight |
| **Weakness** | Health penalties from injuries double as body turns to stone. Only removed when awakening with no damage. |
| **Role** | Reconnaissance, spying |
| **Note** | Visceratika is out-of-Clan |

### Sentinel Gargoyle
| Trait | Value |
|-------|-------|
| **Disciplines** | Flight, Potence, Fortitude |
| **Weakness** | All dice pools halved when truly alone without master, mate, ally, or friend |
| **Role** | Guarding locations, protection |
| **Note** | Visceratika is out-of-Clan |

### Warrior Gargoyle
| Trait | Value |
|-------|-------|
| **Disciplines** | Flight, Fortitude, Protean |
| **Weakness** | During frenzy, a body part turns to stone. Choose body part and associated Attribute; all rolls requiring that Attribute automatically fail until next evening. |
| **Role** | Combat, warfare |
| **Note** | Visceratika is out-of-Clan |

**All variants retain the base weakness**: Willpower treated as 2 lower when resisting Dominate, Presence, or similar mind control powers.

---

## Creation Steps

1. **PC/NPC** — Default PC
2. **Variant** — Standard, Scout, Sentinel, or Warrior
3. **Concept** — Name, Generation, Sect affiliation (if any)
4. **Nature & Demeanor** — From `lookup.py character.archetypes archetypes`
5. **Attributes** — 7/5/3 across Physical/Social/Mental (+ 1 base each)
   - **Note**: Appearance is typically low due to monstrous form
6. **Abilities** — 13/9/5 across Talents/Skills/Knowledges (cap 3)
7. **Disciplines** — 3 dots in Variant Disciplines only
8. **Backgrounds** — 5 dots
   - Gargoyles often have Mentor (Tremere master or free elder)
   - Haven is important (need secure roosting location)
9. **Virtues** — 7 dots (+ 1 base each)
10. **Humanity** — Conscience + Self-Control
11. **Willpower** — Equal to Courage rating
12. **Blood Pool** — Start with roll or max based on Generation
13. **Merits & Flaws** — Include Gargoyle-specific options
14. **⛔ BACKGROUNDS (PC)** — Create documents as needed
15. **Freebies** — 15 + Flaws - Merits. Spend exactly.
16. **Physical Description** — REQUIRED: Detail stone-like features
17. **Weakness Documentation** — Note both base and variant weaknesses
18. **Validate**

---

## Gargoyle Appearance

All Gargoyles have distinctive physical features. Document:

- **Skin**: Stone-like texture, coloration (grey, brown, mottled)
- **Wings**: Type, span, condition
- **Face**: Monstrous features, fangs, horns if any
- **Body**: Build, claws, tail if any
- **Other**: Unique features from creation or age

### Appearance Rating
- Most Gargoyles have Appearance 1-2
- Some may qualify for Appearance 0 (use Nosferatu rules)
- The Merit "Rugged Bad Looks" (from Nosferatu) may apply

---

## Gargoyle-Specific Merits & Flaws

### Merits
| Merit | Points | Effect |
|-------|--------|--------|
| Stillness of Death | 2 | +2 difficulty to find you when perfectly still |
| Heavy Hands | 3 | -1 difficulty to unarmed damage rolls |

### Flaws
| Flaw | Points | Effect |
|------|--------|--------|
| Stone Tongue | 3 | +2 difficulty to Social rolls requiring speech |
| Blood Weakness | 4 | Gain Gangrel OR Tzimisce weakness; one Discipline becomes out-of-Clan |
| Blood Weakness (Severe) | 7 | Gain BOTH Gangrel AND Tzimisce weakness; one Discipline becomes out-of-Clan |

---

## Gargoyle Rituals

Tremere can permanently enchant Gargoyles using Enchant Talisman. These "Gargoyle Rituals" require:

1. Cast Enchant Talisman on the Gargoyle
2. Cast desired ritual for 6 hours/night for 1 week per ritual level
3. Gargoyle can then activate the ritual at will

### Activation Rules
- No roll required to cast
- Lasts one scene or until dismissed
- Gargoyle spends own blood/Willpower as if they were caster
- If ritual normally has no cost, costs 1 blood point to activate
- Gargoyle is considered the "item" for ritual purposes

### Ward of the Winged Sepulcher (Level 3)
**Preparation**: Small cube (half-inch) cut from tombstone of empty grave. Dab each side with blood, whisper incantation, ingest cube.

**Effect**: When sunlight touches Gargoyle's skin, wings unfurl and wrap around self (and one passenger if grappled). Both protected from sunlight until sunset.

**Cost**: If Gargoyle lacks wings normally, deals 1 aggravated damage if protecting self only, 2 if protecting self and another.

**Activation**: Automatic when sunlight contacts skin.

---

## Gargoyle Society

### Relationship with Tremere
- **Slave Gargoyles**: Still serve Tremere willingly or by compulsion
- **Free Gargoyles**: Guard their freedom fiercely
- **Montmartre Pact (1489)**: Formally granted freedom, Tremere agreed to stop creating new Gargoyles
- Invoking **Virstania** (creator who fought for their freedom) gains respect

### Gargoyle Broods
- Free Gargoyles often form loose "broods"
- May claim territories (often Gothic architecture)
- Share information about Tremere activities
- Notable: The Sixpence Pinch (London, early 20th century)

### Haven Considerations
- Need roosting locations (high places preferred)
- Gothic architecture provides camouflage
- Must be secure during day (stone sleep is distinctive)

---

## Sample Concepts

### Impeccable Majordomo
Loyal servant to a Tremere regent (by choice). Manages the chantry, protects its inhabitants, and handles tasks beneath the dignity of warlocks. Takes pride in service well done.

### The Thing in the Basement
Lives in the subbasements of a building, protecting it from threats. The mortal inhabitants don't know you exist, but strange protectors have saved them more than once.

### Abolitionist
Dedicated to freeing enslaved Gargoyles from Tremere bondage. Track down chantries still illegally creating or enslaving Gargoyles and liberate your kin.

---

## Discipline Reference

### Flight
| Level | Power | Effect |
|-------|-------|--------|
| 1 | Glide | Safe falls, short gliding hops |
| 2 | Hover | Remain stationary in air (1 BP/scene) |
| 3 | Fly | True flight up to 30 mph (1 BP/scene) |
| 4 | Swoop | Diving attacks (+2 damage dice) |
| 5 | Aerial Combat | No BP cost for flight, -2 difficulty to maneuvers |

### Visceratika
| Level | Power | Effect |
|-------|-------|--------|
| 1 | Skin of the Chameleon | +2-3 Stealth near stone |
| 2 | Scry the Hearthstone | See through stone |
| 3 | Bond with the Mountain | +2 soak touching stone |
| 4 | Armor of Terra | +4 soak all damage (-1 Dex) |
| 5 | Flow Within the Mountain | Merge with stone completely |

---

## Validation

- [ ] Variant selected and documented
- [ ] Attributes: 15 dots (+ 9 base = 24 total)
- [ ] Abilities: 27 dots, none > 3
- [ ] Disciplines: 3 dots from VARIANT'S in-Clan list
- [ ] Backgrounds: 5 dots
- [ ] Virtues: 10 total (7 + 3 base)
- [ ] Humanity = Conscience + Self-Control
- [ ] Willpower = Courage
- [ ] Flaws ≤ 7 points
- [ ] Freebies spent exactly
- [ ] **Base weakness documented**: Mind control susceptibility
- [ ] **Variant weakness documented** (if applicable)
- [ ] **Physical appearance detailed**: Stone features, wings, etc.
- [ ] (PC) All relevant backgrounds have documents
- [ ] All links valid

---

## Output Template

```markdown
# [Character Name]

**Bloodline**: Gargoyle ([Variant])
**Sire/Creator**: [Name or "Ritual Creation"]
**Generation**: [N]th
**Sect**: [Camarilla/Independent/None]
**Concept**: [Brief concept]

## Variant

**Type**: [Standard/Scout/Sentinel/Warrior]
**In-Clan Disciplines**: [List]
**Variant Weakness**: [Description]

## Physical Appearance

**Skin**: [Stone-like texture, coloration]
**Wings**: [Type, span, condition]
**Face**: [Monstrous features]
**Body**: [Build, claws, other features]
**Height**: [Gargoyles are often large]

## Personality

**Nature**: [Archetype]
**Demeanor**: [Archetype]

## Attributes

[Standard attribute tables]

## Abilities

[Standard ability tables]

## Disciplines

| Discipline | Rating | Powers |
|------------|--------|--------|
| Flight | ●●○○○ | [Powers] |
| [Other] | ●●○○○ | [Powers] |

## Backgrounds

| Background | Rating | Details |
|------------|--------|---------|
| Haven | ●●○○○ | [Roosting location] |
| [Other] | ●●○○○ | [Details] |

## Virtues & Morality

[Standard virtue table]

## Secondary Traits

| Trait | Value |
|-------|-------|
| Willpower | ●●●○○○○○○○ |
| Blood Pool | [N]/[Max] |

## Weaknesses

### Base Weakness (All Gargoyles)
Willpower is treated as 2 points lower when resisting Dominate, Presence, or similar mind control powers.

### Variant Weakness ([Variant Name])
[Specific variant weakness and how it manifests for this character]

## Merits & Flaws

[Standard M&F table]

## History

[Creation circumstances, service history (if any), how freedom was gained (if applicable)]

## Relationships

**With Tremere**: [Attitude toward former/current masters]
**With Other Gargoyles**: [Brood membership, allies]
**With Others**: [Other notable relationships]

## Goals & Motivations

[What drives the character]
```
