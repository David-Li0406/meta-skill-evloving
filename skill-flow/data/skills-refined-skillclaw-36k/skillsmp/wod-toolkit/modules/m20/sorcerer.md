# Sorcerer Character Module

Create mechanically valid M20 Sorcerer characters (hedge wizards and psychics).

## Key Differences from Mages

- **No Paradox**: Sorcerers work within reality's confines
- **Paths instead of Spheres**: Linear, focused magical abilities
- **Rituals**: Extended workings that expand Path capabilities
- **No Awakened Avatar**: Sorcerers cannot learn true magick

## PC vs NPC

| Type | Linked Documents | When |
|------|------------------|------|
| **PC** (default) | REQUIRED | Standard creation |
| **NPC** | Not required | "NPC", "quick", "simple", "stat block" |

## Dependencies (PC Only)

**Read `modules/background-expansion.md` for the complete background → module mapping.**

| Background/Feature | Action |
|--------------------|--------|
| (Hedge Wizard PCs) | Select 1 ritual per Path level; occasionally **invent** 1 custom ritual (read `modules/sorcerer-ritual.md`) |
| Library, Artifact, Allies, Retainers, Mentor | See `modules/background-expansion.md` |
| Alchemy Path | Read `modules/sorcerer-alchemy.md`, create 1-2 signature recipes |
| Enchantment Path | Read `modules/sorcerer-enchantment.md`, create 1-2 signature items |

**DO NOT create a PC with backgrounds as one-line summaries.**

### Custom Ritual Creation

For unique sorcerer PCs, **occasionally invent one custom ritual** that reflects their personal style or history:
- Read `modules/sorcerer-ritual.md` for creation guidelines
- Choose a Path the character knows
- Create ritual level ≤ (Path rating - 1)
- Document the ritual's in-character origin (teacher, self-discovery, stolen secrets)
- Link the ritual document from the character sheet

**When to create custom rituals**:
- Character has 3+ dots in a Path
- Character has a distinctive Practice or concept
- Character's background suggests unique training
- NOT for basic/generic characters

## Creation Steps

### Step 1: Character Concept

1. **Type**: Hedge Wizard OR Psychic (determines Numina pool)
2. **Concept**: Core character idea
3. **Affiliation**: From `lookup.py sorcerer.affiliations affiliations` or Lone Practitioner
4. **Nature & Demeanor**: From `lookup.py character.archetypes archetypes`
5. **Essence**: Dynamic, Pattern, Primordial, or Questing

### Step 2: Attributes (6/4/3)

Prioritize Physical, Social, Mental (+ 9 base = 1 each).

**Affiliation Guidance**: Use Affiliation's Favored Attributes as a guide.

```bash
python scripts/lookup.py sorcerer.affiliations affiliations "Arcanum"
```

### Step 3: Abilities (11/7/4)

Prioritize Talents, Skills, Knowledges. **Maximum 3 at creation.**

**Critical**: The Ability chosen for each Path **caps that Path's rating**.

### Step 4: Backgrounds (5 dots)

Standard Backgrounds from `lookup.py character.backgrounds backgrounds`.

**Special**: Sorcerers may take Artifact background (see `lookup.py sorcerer.merits-flaws merits-flaws`).

### Step 5: Numina (5 dots)

Choose ONE type:
- **Hedge Magic Paths** — From `lookup.py sorcerer.paths paths`
- **Psychic Phenomena** — From `lookup.py sorcerer.psychic-phenomena psychic-phenomena`

**Cannot mix** at character creation. Secondary Numina costs 21 XP later.

#### Hedge Wizard Setup

1. **Casting Attribute**: Choose from Affiliation's Favored Attributes
2. **Affinity Path**: Choose one from Affiliation's Favored Paths
3. **For each Path purchased**:
   - Choose a **Practice** (flavors how you cast)
   - Choose a **Path Ability** (caps the Path rating)
   - Select one **Ritual per Path level** from existing options
   - **PC Only**: Consider inventing 1 custom ritual (see Dependencies above)

```bash
# Check Path details
python scripts/lookup.py sorcerer.paths paths "Alchemy"

# Check Aspects for spell building
python scripts/lookup.py sorcerer.aspects aspects "Duration"

# Check existing rituals
python scripts/lookup.py sorcerer.rituals rituals "Divination"
```

#### Ritual Selection Guidelines

| Path Level | Known Rituals | Custom Ritual? |
|------------|---------------|----------------|
| 1 | 1 existing | No |
| 2 | 2 existing | No |
| 3 | 3 existing | Optional (if unique concept) |
| 4 | 4 existing | Encouraged |
| 5 | 5 existing | Expected |

**PC**: At least document ALL rituals; create custom if Path ≥ 3 and character is distinctive.

#### Psychic Setup

No Practice or Ability cap — Psychic phenomena are innate. Just allocate dots.

```bash
python scripts/lookup.py sorcerer.psychic-phenomena psychic-phenomena "Telepathy"
```

### Step 6: Willpower (5)

Base Willpower is 5. Can increase with freebies.

### Step 7: Freebie Points (21)

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Path/Phenomena | 7 |
| Ritual | 3 |
| Background | 1 |
| Willpower | 1 |

### Step 8: Merits & Flaws (Optional)

See `lookup.py sorcerer.merits-flaws merits-flaws`. Maximum 7 points of Flaws.

### Step 9: Finishing Touches

- **Specialties**: Required for any trait at 4+
- **Description**: Appearance, mannerisms, history
- **Equipment**: Including any magical tools/foci

---

## Path Magic Mechanics

### Dice Pool
`Casting Attribute + Path Ability` at difficulty `Path Level + 4`

### Spells vs Rituals

| Type | Time | Power |
|------|------|-------|
| Spells | 1 turn per Path level | Standard Aspects |
| Rituals | 10 minutes per level | Enhanced effects |

### Aspect Costs
1 success per Aspect level. Max Aspect = Path rating.

```bash
# Quick Aspect lookup
python scripts/lookup.py sorcerer.aspects aspects --keys
```

### Witnesses (Sleepers)
| Witnesses | Successes Removed |
|-----------|-------------------|
| 1 | 1 |
| 2-5 | 2 |
| 6-10 | 3 |
| 20-100 | 4 |
| 100+ | 5 |

---

## Paths Quick Reference

| Path | Type | Key Abilities |
|------|------|---------------|
| Alchemy | Ritual | Esoterica, Science, Crafts |
| Conjuration | Spell | Occult, Esoterica |
| Conveyance | Spell | Survival, Occult, Technology |
| Divination | Spell | Occult, Awareness, Investigation |
| Ephemera | Spell | Occult, Empathy, Esoterica |
| Enchantment | Ritual | Crafts, Esoterica, Technology |
| Fascination | Spell | Expression, Subterfuge, Empathy |
| Fortune | Spell | Occult, Esoterica |
| Healing | Spell | Medicine, Empathy, Esoterica |
| Hellfire | Spell | Occult, Science, Esoterica |
| Illusion | Spell | Expression, Subterfuge, Art |
| Maelstroms | Spell | Survival, Occult, Science |
| Necromancy | Both | Occult, Esoterica, Lore (Wraith) |
| Oneiromancy | Spell | Occult, Empathy, Meditation |
| Quintessence Manipulation | Spell | Occult, Esoterica, Awareness |
| Shadows | Spell | Stealth, Occult, Subterfuge |
| Shapeshifting | Spell | Survival, Athletics, Esoterica |
| Summoning/Binding/Warding | Ritual | Occult, Esoterica, Intimidation |
| Weather Control | Spell | Survival, Science, Occult |

---

## Validation Checklist

- [ ] Concept, Affiliation, Nature, Demeanor, Essence defined
- [ ] Attributes: 22 dots (6+4+3 + 9 base)
- [ ] Abilities: 22 dots (11+7+4), none > 3
- [ ] Backgrounds: 5 dots
- [ ] Numina: 5 dots (all one type)
- [ ] (Hedge Wizard) Each Path has:
  - [ ] Casting Attribute selected
  - [ ] Path Ability selected (Path ≤ Ability rating)
  - [ ] Practice chosen
  - [ ] Rituals selected (1 per Path level)
  - [ ] (PC, Path 3+) Consider custom ritual
- [ ] Willpower: 5
- [ ] Freebies: 21 spent exactly
- [ ] Merits/Flaws: Flaws ≤ 7 points
- [ ] Specialties for any trait at 4+

### PC Background Dependencies
- [ ] Library background → Library document exists, linked
- [ ] Artifact background → Enchanted item document exists, linked
- [ ] Allies/Retainers → Companion documents exist, linked
- [ ] Alchemy Path (PC) → 1-2 signature recipes documented
- [ ] Enchantment Path (PC) → 1-2 signature items documented
- [ ] Custom rituals (if any) → Ritual documents exist, linked

---

## Character Output Template

```markdown
# [Character Name]

## Concept
**Type**: Hedge Wizard / Psychic  
**Affiliation**: [Name]  
**Nature**: [Archetype]  
**Demeanor**: [Archetype]  
**Essence**: [Type]

## Attributes

### Physical
| Attribute | Rating |
|-----------|--------|
| Strength | ••○○○ |
| Dexterity | •••○○ |
| Stamina | ••○○○ |

### Social
| Attribute | Rating |
|-----------|--------|
| Charisma | ••○○○ |
| Manipulation | •••○○ |
| Appearance | ••○○○ |

### Mental
| Attribute | Rating |
|-----------|--------|
| Perception | •••○○ |
| Intelligence | ••••○ |
| Wits | •••○○ |

## Abilities

### Talents
| Ability | Rating |
|---------|--------|
| [Name] | ••○○○ |

### Skills
| Ability | Rating |
|---------|--------|
| [Name] | ••○○○ |

### Knowledges
| Ability | Rating |
|---------|--------|
| [Name] | ••○○○ |

## Backgrounds
| Background | Rating | Details |
|------------|--------|---------|
| [Name] | ••○○○ | [Description] |

## Numina

### Casting Attribute: [Attribute]

### Paths / Phenomena
| Path/Phenomenon | Rating | Practice | Ability |
|-----------------|--------|----------|---------|
| [Name] (Affinity) | •••○○ | [Practice] | [Ability] |

### Rituals
| Ritual | Path | Level | Effect |
|--------|------|-------|--------|
| [Name] | [Path] | • | [Brief effect] |

## Advantages

**Willpower**: ••••• ○○○○○

## Merits & Flaws
| Merit/Flaw | Points | Effect |
|------------|--------|--------|
| [Name] | +/- X | [Brief description] |

## Freebie Expenditure
| Purchase | Cost |
|----------|------|
| [Trait] | X |
| **Total** | 21 |

## Description
[Physical description, mannerisms, history]

## Equipment
[Notable possessions, foci, tools]

## Linked Documents (PC Only)
| Type | Document |
|------|----------|
| [Custom Ritual] | [ritual_name.md](./rituals/ritual_name.md) |
| [Library] | [library_name.md](./libraries/library_name.md) |
| [Enchanted Item] | [item_name.md](./items/item_name.md) |
| [Companion] | [companion_name.md](./companions/companion_name.md) |
```

---

## PC File Structure

```
[character]/
├── [character].md          ← Links to all below
├── rituals/                ← Custom rituals
├── libraries/              ← If Library background
│   └── grimoires/
├── items/                  ← Alchemy recipes & enchanted items
└── companions/             ← If Allies/Retainers
```
