# Character Module

Create mechanically valid Kithain (changeling) characters for C20.

## PC vs NPC

| Type | Linked Documents | When |
|------|------------------|------|
| **PC** (default) | REQUIRED | Standard creation |
| **NPC** | Not required | "NPC", "quick", "simple", "stat block" |

## Dependencies (PC Only)

**Read `modules/background-expansion.md` for the complete background → module mapping.**

| Background | Action |
|------------|--------|
| Chimera | Read `modules/chimera.md`, create chimera document |
| Holdings | Read `modules/freehold.md`, create freehold document |
| Title | Read `modules/household.md`, create household + retainer docs |
| Treasure | Read `modules/treasure.md`, create treasure document |
| Retinue | Create NPC companion documents |
| Mentor | Create mentor NPC document |

**DO NOT create a PC with backgrounds as one-line summaries.**

## Creation Steps

1. **PC/NPC** — Default PC
2. **Concept** — Name, kith, court, seeming
3. **Legacy** — Seelie and Unseelie Legacies (one primary based on Court)
4. **House** (if noble) — Noble House affiliation
5. **Attributes** — 7/5/3 across Physical/Social/Mental
6. **Abilities** — 13/9/5 across Talents/Skills/Knowledges (cap 3)
7. **Backgrounds** — 5 dots. Note which need sub-documents
8. **Arts** — 3 dots (capped at 3 at creation)
9. **Realms** — 5 dots
10. **Glamour** — Base by kith
11. **Willpower** — Base by kith
12. **Banality** — Base by seeming
13. **Birthrights & Frailty** — From kith
14. **⛔ BACKGROUNDS (PC)** — Create documents for Chimera/Holdings/Title/Treasure/etc.
15. **Merits & Flaws** — From `lookup.py character.merits-flaws merits-flaws`. Flaws ≤ 7
16. **Freebies** — 15 + Flaws - Merits. Spend exactly.
17. **Specialties** — Required for 4+ traits
18. **Description** — Mortal seeming and fae mien
19. **Document** — Link all sub-documents
20. **Validate**

---

## Kith Selection

### Commoner Kiths

| Kith | Glamour | Willpower | Concept |
|------|---------|-----------|---------|
| Boggan | 4 | 4 | Helpful homemakers, keepers of hearth |
| Clurichaun | 5 | 3 | Fun-loving collectors, mercurial tempers |
| Eshu | 4 | 5 | Wandering storytellers, serendipitous travelers |
| Nocker | 4 | 4 | Foul-mouthed inventors, perfectionist crafters |
| Piskie | 6 | 2 | Innocent wanderers, irresistible thieves |
| Pooka | 5 | 3 | Shapeshifting tricksters, compulsive liars |
| Redcap | 5 | 3 | Monstrous gluttons, violent troublemakers |
| Satyr | 5 | 4 | Passionate hedonists, fierce warriors |
| Selkie | 4 | 4 | Skinchanging seadwellers, cautious romantics |
| Sluagh | 4 | 4 | Whispering secrets-keepers, underworld dwellers |
| Troll | 4 | 5 | Honorable giants, oath-bound warriors |

### Noble Kiths

| Kith | Glamour | Willpower | Concept |
|------|---------|-----------|---------|
| Sidhe (Arcadian) | 4 | 6 | Returned rulers, body-stealers |
| Sidhe (Autumn) | 4 | 5 | Reborn nobles, mortal-bonded |

Reference: `lookup.py kith.kithain kithain`

---

## Seeming Selection

| Seeming | Banality | Description | Mechanical Notes |
|---------|----------|-------------|------------------|
| **Childling** | 1 | Children, full of wonder | Cannot have Resources 3+; social limitations |
| **Wilder** | 3 | Teens/young adults, passionate | Standard; most common |
| **Grump** | 5 | Adults, world-weary | Highest starting Banality |

**Seeming affects starting Banality and roleplay expectations.**

---

## Court & Legacy

### Courts
| Court | Philosophy |
|-------|------------|
| **Seelie** | Honor, tradition, protection of the Dreaming |
| **Unseelie** | Change, passion, personal freedom |

### Legacy Selection
Every changeling has TWO Legacies:
- **Primary Legacy** — Matches Court affiliation
- **Secondary Legacy** — From opposite Court

**Seelie Legacies**: Bumpkin, Courtier, Crafter, Dandy, Hermit, Orchid, Paladin, Panderer, Regent, Sage, Saint, Squire, Troubadour, Wayfarer

**Unseelie Legacies**: Beast, Fatalist, Fool, Grotesque, Knave, Outlaw, Pandora, Peacock, Rake, Riddler, Ringleader, Savage, Schismatic, Wretch

Reference: `lookup.py character.legacies legacies`

### Legacy Mechanics
- **Quest**: Fulfilling primary Legacy's Quest = regain Willpower
- **Ban**: Violating primary Legacy's Ban = lose Willpower

---

## Noble Houses (Sidhe & Ennobled Commoners)

### Seelie Houses
| House | Concept | Boon | Flaw |
|-------|---------|------|------|
| Beaumayn | Seers, cursed visionaries | Prophetic visions | Haunted by visions |
| Dougal | Practical builders, craftsmen | Craft affinity | Hide deformity |
| Eiluned | Mystics, keepers of secrets | Magic affinity | Mistrusted |
| Fiona | Passionate romantics, rebels | Love's inspiration | Reckless passion |
| Gwydion | Noble warriors, rightful rulers | Leadership aura | Prone to fury |
| Liam | Mortal protectors, scholars | Human empathy | Stigma of disgrace |
| Scathach | Shadow warriors, stayed behind | Combat prowess | Outsider status |

### Unseelie Houses
| House | Concept | Boon | Flaw |
|-------|---------|------|------|
| Ailil | Master manipulators, strategists | Political acumen | Paranoid rivalry |
| Balor | Brutal dominators, marked | Raw power | Visible deformity |
| Daireann | Keeper of lost secrets | Ancient knowledge | Bound by tradition |

Reference: `lookup.py character.houses houses`

---

## Arts Selection

Arts are the "what" of changeling magic (cantrips). Starting characters receive 3 dots.

### Common Arts
| Art | Domain | Key Uses |
|-----|--------|----------|
| Chicanery | Illusion, misdirection | Hide, disguise, confuse |
| Legerdemain | Sleight of hand, theft | Move objects, snatch, teleport items |
| Primal | Nature, elements | Control plants, weather, animals |
| Soothsay | Fate, prophecy | Read fate, bless/curse, omens |
| Sovereign | Authority, command | Give orders, inspire, dominate |
| Wayfare | Movement, travel | Speed, leap, teleport, flight |

### Advanced Arts
| Art | Domain | Restrictions |
|-----|--------|--------------|
| Autumn | Banality manipulation | Unseelie-associated |
| Chronos | Time manipulation | Rare, dangerous |
| Dream-Craft | Chimera creation | Requires training |
| Infusion | Object enchantment | Crafting focus |
| Metamorphosis | Shapeshifting | Body-focused |
| Naming | True names, identity | Ancient, powerful |
| Oneiromancy | Dream-walking | Dream-focused |
| Pyretics | Fire and passion | Destructive |
| Skycraft | Air and weather | Elemental |
| Spirit Link | Spirit communication | Spirit-focused |
| Tale Craft | Narrative magic | Story-focused |

Reference: `lookup.py arts.arts arts`

---

## Realms Selection

Realms are the "who/what" of cantrips (targets). Starting characters receive 5 dots.

| Realm | Targets | Examples |
|-------|---------|----------|
| **Actor** | Mortals, humans | Enchant a person, affect a crowd |
| **Fae** | Changelings, chimera, Glamour | Target another kithain, affect chimera |
| **Nature** | Animals, plants, natural elements | Command animals, shape plants |
| **Prop** | Crafted objects, tools | Enchant a sword, animate a car |
| **Scene** | Areas, environments | Affect a room, create an area effect |
| **Time** | Duration, timing | Extend effects, delay triggers |

### Realm Levels
| Level | Scope |
|-------|-------|
| 1 | Basic/simple targets |
| 2 | Typical/common targets |
| 3 | Complex/unusual targets |
| 4 | Powerful/rare targets |
| 5 | Legendary/extreme targets |

Reference: `lookup.py realms.realms realms`

---

## Backgrounds

| Background | Description |
|------------|-------------|
| Chimera | Companion creatures, chimerical items |
| Contacts | Mortal information sources |
| Dreamers | Mortals who provide Glamour |
| Holdings | Freehold access/ownership |
| Mentor | Teacher, guide |
| Resources | Wealth, income |
| Retinue | Servants, followers |
| Title | Noble rank, political power |
| Treasure | Magical items |

Reference: `lookup.py character.backgrounds backgrounds`

---

## Allocation Summary

| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 3 base each) |
| Abilities | 13/9/5 (cap 3) |
| Backgrounds | 5 |
| Arts | 3 |
| Realms | 5 |
| Glamour | By kith (typically 4-6) |
| Willpower | By kith (typically 3-6) |
| Banality | By seeming (1/3/5) |
| Freebies | 15 |

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 |
| Art | 5 |
| Realm | 3 |
| Glamour | 3 |
| Willpower | 1 |

---

## Birthrights & Frailties

Each kith has unique Birthrights (benefits) and a Frailty (weakness).

**Example — Boggan**:
- **Birthright: Craftwork** — Accomplish mundane tasks in 1/3 time when unobserved
- **Birthright: Social Dynamics** — Know social connections instantly
- **Frailty: Call of the Needy** — Must help those who ask (Willpower to resist)

Reference: `lookup.py kith.kithain kithain` for complete Birthright/Frailty lists.

---

## Reference Data

```bash
# Kith details
python scripts/lookup.py kith.kithain kithain "Boggan"
python scripts/lookup.py kith.kithain kithain "Sidhe"

# Legacies
python scripts/lookup.py character.legacies legacies "Paladin"
python scripts/lookup.py character.legacies legacies --type "unseelie"

# Noble Houses
python scripts/lookup.py character.houses houses "Fiona"

# Arts
python scripts/lookup.py arts.arts arts "Chicanery"

# Realms
python scripts/lookup.py realms.realms realms "Actor"

# Merits & Flaws
python scripts/lookup.py character.merits-flaws merits-flaws --find "Surreal Quality"
```

---

## Validation

- [ ] Attributes: 15 dots (+ 9 base = 24 total across 9 Attributes)
- [ ] Abilities: 27 dots, none > 3
- [ ] Backgrounds: 5 dots
- [ ] Arts: 3 dots, none > 3
- [ ] Realms: 5 dots
- [ ] Glamour matches kith base
- [ ] Willpower matches kith base
- [ ] Banality matches seeming (Childling 1, Wilder 3, Grump 5)
- [ ] Seelie AND Unseelie Legacy chosen
- [ ] Primary Legacy matches Court
- [ ] Birthrights and Frailty noted from kith
- [ ] Flaws ≤ 7 points
- [ ] Freebies spent exactly
- [ ] (PC) All relevant backgrounds have documents:
  - [ ] Chimera → Chimera document(s)
  - [ ] Holdings → Freehold document
  - [ ] Title → Household document + retainer NPCs
  - [ ] Treasure → Treasure document(s)
  - [ ] Mentor → Mentor NPC document
  - [ ] Retinue → Retainer NPC documents
- [ ] All links valid

---

## PC File Structure

```
[character]/
├── [character].md          ← Links to all below
├── chimera/
├── treasures/
├── companions/             ← Retinue, Mentor
├── freehold/               ← If Holdings background
└── household/              ← If Title background
```

---

## Output Template

```markdown
# [Character Name]

**Kith**: [Kith]
**Seeming**: [Childling/Wilder/Grump]
**Court**: [Seelie/Unseelie]
**House**: [House or "Commoner"]
**Seelie Legacy**: [Legacy] | **Unseelie Legacy**: [Legacy]

## Concept
[2-3 sentences describing the character]

## Attributes

### Physical
| Attribute | Rating |
|-----------|--------|
| Strength | ●●○○○ |
| Dexterity | ●●●○○ |
| Stamina | ●●○○○ |

### Social
| Attribute | Rating |
|-----------|--------|
| Charisma | ●●●○○ |
| Manipulation | ●●○○○ |
| Appearance | ●●●○○ |

### Mental
| Attribute | Rating |
|-----------|--------|
| Perception | ●●○○○ |
| Intelligence | ●●●○○ |
| Wits | ●●○○○ |

## Abilities

### Talents
[List with ratings]

### Skills
[List with ratings]

### Knowledges
[List with ratings]

## Advantages

### Backgrounds
| Background | Rating | Document |
|------------|--------|----------|
| [Background] | ●●●○○ | [Link if applicable] |

### Arts
| Art | Rating |
|-----|--------|
| [Art] | ●●○○○ |

### Realms
| Realm | Rating |
|-------|--------|
| [Realm] | ●●●○○ |

## Birthrights & Frailty

### Birthrights
- **[Birthright Name]**: [Description]

### Frailty
- **[Frailty Name]**: [Description]

## Merits & Flaws

### Merits
| Merit | Points |
|-------|--------|
| [Merit] | [N] |

### Flaws
| Flaw | Points |
|------|--------|
| [Flaw] | [N] |

## Vital Statistics

| Stat | Rating |
|------|--------|
| Glamour | ●●●●○○○○○○ |
| Willpower | ●●●●●○○○○○ |
| Banality | ●●●○○○○○○○ |

## Appearance

### Mortal Seeming
[Description of human appearance]

### Fae Mien
[Description of true faerie appearance]

## History
[Character background]

## Freebie Expenditure
| Trait | Cost | Total |
|-------|------|-------|
| [Trait] | [N] | [Running total] |
| **Total** | | **15** |
```
