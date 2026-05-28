# Vampire Hunter Module (Hunters Hunted II)

Create mortal vampire hunters using the rules from V20: The Hunters Hunted II.

## Overview

Hunters are mortals who have discovered the existence of vampires and chosen to fight back. Unlike generic mortals, hunters are defined by their motivation, methodology, and the terrible knowledge they carry.

## Hunter Types

| Type | Description | Example Concepts |
|------|-------------|------------------|
| **Lone Wolf** | Solo operator, often paranoid | Obsessed detective, vengeful survivor |
| **Cell Member** | Part of small hunting group (3-6 ideal) | Team specialist, recruited amateur |
| **Organization Agent** | Works for established hunter group | Inquisitor, government operative, Arcanum scholar |
| **Criminal Hunter** | Underworld figure hunting vampires | Mafia enforcer, Bratva mercenary |
| **Religious Crusader** | Faith-driven hunter | Priest, nun, lay believer with True Faith |

---

## Character Creation

### Step 1: Concept & Motivation

**Concept**: Who were they before becoming a hunter?
- Burnout (escaped ghoul, reformed cultist, vitae addict)
- Crusader (former Inquisitor, militant priest, modern knight)
- Scientist (behavioral psychologist, biologist, researcher)
- Survivor (attack victim, witness, bereaved family member)
- Professional (detective, soldier, journalist, EMT)

**Motivation**: Why do they hunt?
- How were they introduced to the supernatural?
- Why fight rather than flee or deny?
- What drives them to continue?
- What do they believe vampires are?

### Step 2: Nature & Demeanor

Select from standard V20 Archetypes (pp. 87-96 of V20).

Common hunter Natures: Soldier, Fanatic, Survivor, Judge, Martyr
Common hunter Demeanors: Traditionalist, Director, Bravo, Loner, Conformist

### Step 3: Attributes (6/4/3)

Prioritize Physical, Social, Mental categories.

> **Variant (HH2 p.35)**: Storytellers may use 7/5/3 to put hunters on more even footing with vampires.

### Step 4: Abilities (13/9/5)

Prioritize Talents, Skills, Knowledges. No Ability above 3 at this stage.

> **Note**: This differs from generic mortals (11/7/4). Use 13/9/5 for dedicated hunter characters per HH2.

**Key Hunter Abilities**:
- Investigation, Alertness, Streetwise (finding prey)
- Firearms, Melee, Brawl (fighting prey)
- Occult, Academics (understanding prey)
- Stealth, Survival (surviving prey)

### Step 5: Backgrounds (5 dots)

Standard backgrounds plus hunter-specific options:

| Background | Description |
|------------|-------------|
| **Armory** | Weapons, ammunition, armor cache |
| **Base of Operations** | Secure staging area (Luxury/Size/Security) |
| **Guide** | Mysterious spiritual entity advisor |
| Allies | Fellow hunters, sympathetic authorities |
| Contacts | Informants, specialists, fences |
| Resources | Funding for equipment and operations |
| Mentor | Experienced hunter or organization elder |

See `lookup.py v20.hunter backgrounds` for details.

### Step 6: Virtues (7 dots)

- Conscience (or Conviction): starts at 1
- Self-Control (or Instinct): starts at 1
- Courage: starts at 1
- Distribute 7 additional dots

Hunters typically have high Courage (facing monsters requires it).

### Step 7: Humanity & Willpower

- **Humanity** = Conscience + Self-Control
- **Willpower** = Courage

> **Warning**: Hunting erodes Humanity. Breaking and entering, lying, killing ghouls, collateral damage — all take their toll.

### Step 8: Freebie Points (21)

| Trait | Cost |
|-------|------|
| Attribute | 5 per dot |
| Ability | 2 per dot |
| Background | 1 per dot |
| Virtue | 2 per dot |
| Humanity | 2 per dot |
| Willpower | 1 per dot |
| Numina | 7 per dot |

> **Variant Note**: HH2 uses Humanity cost of 2 per dot. Standard V20 mortals use 1 per dot.

### Step 9: Merits & Flaws (Optional, max 7 pts Flaws)

See `lookup.py v20.hunter merits-flaws` for hunter-specific options.

### Step 10: Numina (Optional)

Hunters may possess supernatural abilities. See Chapter Four of HH2 or `lookup.py v20.hunter numina`.

**Types**:
- **Hedge Magic**: Folklore-based magic (Curses, Divination, Healing)
- **Psychic Phenomena**: Mental powers (Pyrokinesis, Telekinesis, Astral Projection)
- **True Faith**: Divine protection and miracles

**Limitations**:
- Rarely possess more than one type of Numina
- Some paths are mutually exclusive
- Acquiring new paths requires story justification

---

## Hunter Organizations

Hunters may belong to established groups. See `lookup.py v20.hunter organizations`.

| Organization | Type | Key Features |
|--------------|------|--------------|
| **Society of Leopold** | Catholic Inquisition | Faith-based, militant, sub-orders |
| **Project Twilight** | US Government | Resources, legal cover, compromised leadership |
| **The Arcanum** | Academic | Knowledge-focused, non-interventionist officially |
| **Criminal Networks** | Underworld | Mafia, Bratva, Cartels with vampire vendettas |
| **Ikhwan al-Safa** | Islamic | Middle Eastern, Taftâni mage allies |
| **Akritai** | Orthodox Christian | Eastern European, no formal hierarchy |
| **Knights of St. George** | Interfaith | Global, includes sorcerers |

---

## Hunting Tactics

### Cell Operations

Ideal hunting party: 3-6 members

| Role | Function | Key Traits |
|------|----------|------------|
| Leader | Coordination, decisions | Leadership, Tactics |
| Scout | Reconnaissance, surveillance | Stealth, Investigation |
| Researcher | Intel, occult knowledge | Academics, Occult, Computer |
| Muscle | Direct combat | Brawl, Firearms, Melee |
| Tech | Equipment, communications | Technology, Science |
| Face | Social engineering, covers | Subterfuge, Expression |

### Planning Phase (Optional System)

1. Gather information about target
2. Each player contributes to plan
3. Roll relevant Abilities, pool successes
4. Divide total by number of players = **Plan Dice**
5. Plan Dice can be spent during mission for bonus dice

### Threat Assessment

| Threat Level | Target Description |
|--------------|-------------------|
| Low | Young, isolated vampire; no haven security |
| Moderate | Established vampire; ghouls, basic haven |
| High | Elder or well-connected; multiple ghouls, fortified haven |
| Extreme | Primogen/Prince level; extensive resources, political cover |
| Suicidal | Methuselah; ancient powers, vast influence |

---

## What Hunters Know

Hunters piece together vampire lore from observation, not Kindred terminology.

| What Hunters Call It | What It Actually Is |
|---------------------|---------------------|
| "The C Word" / "Catamaran" | Camarilla |
| "The Other Ones" / "Cultists" | Sabbat |
| "Prince" | Prince (they got this one right) |
| "Blood slaves" | Ghouls |
| "Turning" | The Embrace |
| "Mind control" | Dominate, Presence |
| "Vanishing" | Obfuscate |
| "Shapeshifting" | Protean, other forms |

**Key Insights**:
- Being bitten doesn't automatically turn you
- Vampires have politics and factions
- Some vampires can be negotiated with (dangerous)
- Killing the wrong vampire brings consequences
- Vampires have human allies in positions of power

---

## Survival Guidelines

From experienced hunters:

1. **Know what you know** — and what you don't
2. **If you've seen one vampire, you've seen one vampire** — don't generalize
3. **One eye on the door** — always have escape routes
4. **To be known is to be dead** — protect your identity
5. **Information now is better than crisis later** — research before attacking
6. **Stay off the grid** — digital footprints get you killed

---

## The Cost of Hunting

### Humanity Erosion

Hunting requires moral compromises:
- Breaking and entering havens
- Lying to authorities, loved ones
- Killing ghouls (enslaved humans)
- Collateral damage
- Becoming what you hunt

### Social Isolation

- Can't discuss the truth with normal people
- Relationships suffer from paranoia and schedule
- Other hunters may turn on you
- Authorities may pursue you for "crimes"

### Physical Toll

- No supernatural healing
- Sleep deprivation from night operations
- Addiction risks (stimulants to stay awake, vitae temptation)
- Cumulative injuries

---

## Output Template

```markdown
# [NAME]
## Vampire Hunter

**Concept**: [One-line concept]
**Motivation**: [Why they hunt]
**Nature**: [Archetype]
**Demeanor**: [Archetype]
**Organization**: [If any]

### Attributes
**Physical**: Strength [X], Dexterity [X], Stamina [X]
**Social**: Charisma [X], Manipulation [X], Appearance [X]
**Mental**: Perception [X], Intelligence [X], Wits [X]

### Abilities
**Talents**: [List with ratings]
**Skills**: [List with ratings]
**Knowledges**: [List with ratings]

### Backgrounds
[List with ratings, expand Armory/Base/Guide if taken]

### Virtues
Conscience [X], Self-Control [X], Courage [X]

### Other Traits
**Humanity**: [X]
**Willpower**: [X]

### Numina (if any)
[Path]: [Rating]
- [Level abilities known]

### Merits & Flaws
[List with point values]

### Equipment
[Standard loadout]
[Special items from Armory]

### Description
[Physical appearance]

### Background
[How they discovered vampires]
[Key experiences since]
[Current situation]

### Hunting Style
[Methodology: aggressive, cautious, research-focused, etc.]
[Preferred tactics]
[Known vampire intel]

### Connections
[Cell members, organization contacts, mortal ties]
[Enemies made]

### Vulnerabilities
[Psychological weaknesses]
[People who can be threatened]
[Practical limitations]
```

---

## Validation Checklist

- [ ] Concept and motivation defined
- [ ] Attributes: 6/4/3 (or 7/5/3 variant)
- [ ] Abilities: 13/9/5, none above 3 before freebies
- [ ] Backgrounds: 5 dots, hunter-specific considered
- [ ] Virtues: 7 dots distributed
- [ ] Humanity = Conscience + Self-Control
- [ ] Willpower = Courage
- [ ] Freebies: 21 points spent legally
- [ ] Numina paths compatible (if multiple)
- [ ] Organization membership makes sense for concept
- [ ] Survival strategy considered
- [ ] Ties to mortal world established

---

## Reference Commands

```bash
# Hunter backgrounds
python scripts/lookup.py v20.hunter backgrounds

# Hunter merits and flaws
python scripts/lookup.py v20.hunter merits-flaws

# Hunter Numina
python scripts/lookup.py v20.hunter numina

# Hunter organizations
python scripts/lookup.py v20.hunter organizations

# Society of Leopold details
python scripts/lookup.py v20.hunter organizations "Society of Leopold"
```
