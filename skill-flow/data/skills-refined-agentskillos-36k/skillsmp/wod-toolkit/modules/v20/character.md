# Character Module

Create mechanically valid Vampire characters for V20.

## PC vs NPC

| Type | Linked Documents | When |
|------|------------------|------|
| **PC** (default) | REQUIRED | Standard creation |
| **NPC** | Not required | "NPC", "quick", "simple", "stat block" |

## Dependencies (PC Only)

**Read `modules/background-expansion.md` for the complete background → module mapping.**

| Background | Action |
|------------|--------|
| Allies, Mentor | Create NPC document(s) |
| Retainers | Read `modules/ghoul.md`, create ghoul document(s) |
| Haven | Read `modules/haven.md`, create haven document |
| Herd | Create herd description |

**DO NOT create a PC with backgrounds as one-line summaries.**

## Creation Steps

1. **PC/NPC** — Default PC
2. **Concept** — Name, Clan, Sect, Generation
3. **Nature & Demeanor** — From `lookup.py character.archetypes archetypes`
4. **Attributes** — 7/5/3 across Physical/Social/Mental (+ 1 base each)
5. **Abilities** — 13/9/5 across Talents/Skills/Knowledges (cap 3)
6. **Disciplines** — 3 dots in Clan Disciplines only
7. **Backgrounds** — 5 dots. Note which need sub-documents
8. **Virtues** — 7 dots (+ 1 base each in Conscience, Self-Control, Courage)
9. **Humanity** — Conscience + Self-Control (typically 5-7)
10. **Willpower** — Equal to Courage rating
11. **Blood Pool** — Start with roll or max based on Generation
12. **Merits & Flaws** — From `lookup.py character.merits-flaws merits-flaws`. Flaws ≤ 7
13. **⛔ BACKGROUNDS (PC)** — Create documents for Allies/Haven/Mentor/Retainers
14. **Freebies** — 15 + Flaws - Merits. Spend exactly.
15. **Specialties** — Required for 4+ traits
16. **Description** — Appearance, dress, mannerisms
17. **Clan Weakness** — Document specific weakness details
18. **Document** — Link all sub-documents
19. **Validate**

---

## Clan Selection

When choosing a Clan, consult the detailed references:

```bash
# Get clan details
python scripts/lookup.py rules.clans clans "Toreador"

# Search for clans by Discipline
python scripts/lookup.py rules.clans clans --find "Dominate"
```

### Clan Overview

| Clan | Sect | Primary Role |
|------|------|--------------|
| Assamite | Independent | Assassin, diablerist |
| Brujah | Camarilla | Rebel, idealist, fighter |
| Followers of Set | Independent | Tempter, corruptor |
| Gangrel | Camarilla* | Survivor, loner |
| Giovanni | Independent | Necromancer, crime family |
| Lasombra | Sabbat | Shadow lord, leader |
| Malkavian | Camarilla | Seer, madman |
| Nosferatu | Camarilla | Spy, information broker |
| Ravnos | Independent | Trickster, wanderer |
| Toreador | Camarilla | Artist, socialite |
| Tremere | Camarilla | Blood sorcerer |
| Tzimisce | Sabbat | Flesh-shaper, scholar |
| Ventrue | Camarilla | Leader, aristocrat |
| Caitiff | Any | Outcast, reject |

*Gangrel officially left the Camarilla in 1999

---

## Disciplines

Characters begin with 3 dots in Clan Disciplines only. Additional Disciplines may be purchased with freebies (7 per dot) but require in-game justification.

### Discipline Reference

```bash
# Get discipline powers
python scripts/lookup.py disciplines.disciplines disciplines "Auspex"

# Search by effect
python scripts/lookup.py disciplines.disciplines disciplines --find "invisible"
```

### Common Discipline Uses

| Effect | Discipline | Level |
|--------|------------|-------|
| Read emotions | Auspex | 2 |
| Turn invisible | Obfuscate | 4 |
| Command someone | Dominate | 1 |
| Superhuman strength | Potence | 1+ |
| Superhuman speed | Celerity | 1+ |
| Resist damage | Fortitude | 1+ |
| Terrify crowd | Presence | 3 |
| Shapeshift | Protean | 3+ |
| Create illusions | Chimerstry | 1+ |
| Summon/bind spirits | Necromancy | varies |
| Blood magic | Thaumaturgy | varies |

---

## Generation

Generation determines power limits. Most starting characters are 13th-10th.

| Generation | Blood Pool | Blood/Turn | Discipline Max | Common For |
|------------|------------|------------|----------------|------------|
| 13th | 10 | 1 | 5 | Neonates |
| 12th | 11 | 1 | 5 | Neonates |
| 11th | 12 | 1 | 5 | Young vampires |
| 10th | 13 | 1 | 5 | Experienced |
| 9th | 14 | 2 | 5 | Ancillae |
| 8th | 15 | 3 | 5 | Elder |

**Freebies**: Generation Background costs 2 freebies per dot.

---

## Humanity & Virtues

### Virtues (7 dots + 3 base)

| Virtue | Governs |
|--------|---------|
| Conscience | Guilt, ethics, degeneration rolls |
| Self-Control | Resisting frenzy from hunger/desire |
| Courage | Resisting Rötschreck (fear frenzy) |

### Humanity Scale

| Humanity | Description | Frenzy Diff |
|----------|-------------|-------------|
| 10 | Saintly | 4 |
| 8-9 | Exemplary | 5 |
| 7 | Average human | 6 |
| 5-6 | Distant | 6-7 |
| 3-4 | Cold, callous | 7 |
| 1-2 | Monster | 8 |
| 0 | The Beast takes over | — |

---

## Allocation Summary

| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Disciplines | 3 (Clan only) |
| Backgrounds | 5 |
| Virtues | 7 (+ 3 base) |
| Humanity | Conscience + Self-Control |
| Willpower | = Courage |
| Freebies | 15 |

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 |
| Discipline (Clan) | 7 |
| Discipline (Non-Clan) | 7 (requires justification) |
| Virtue | 2 |
| Humanity | 2 |
| Willpower | 1 |

---

## Reference Data

```bash
# Clan details (Disciplines, weakness, etc.)
python scripts/lookup.py rules.clans clans "Malkavian"

# Archetypes for Nature/Demeanor
python scripts/lookup.py character.archetypes archetypes "Rebel"

# Attributes
python scripts/lookup.py character.attributes attributes "Charisma"

# Abilities
python scripts/lookup.py character.abilities abilities "Streetwise"

# Backgrounds
python scripts/lookup.py character.backgrounds backgrounds "Haven"

# Merits & Flaws
python scripts/lookup.py character.merits-flaws merits-flaws --find "generation"
python scripts/lookup.py character.merits-flaws merits-flaws "physical"
```

---

## Validation

- [ ] Attributes: 15 dots (+ 9 base = 24 total)
- [ ] Abilities: 27 dots, none > 3
- [ ] Disciplines: 3 dots, all from Clan list
- [ ] Backgrounds: 5 dots
- [ ] Virtues: 10 total (7 + 3 base)
- [ ] Humanity = Conscience + Self-Control
- [ ] Willpower = Courage
- [ ] Flaws ≤ 7 points
- [ ] Freebies spent exactly
- [ ] Clan weakness documented
- [ ] (PC) All relevant backgrounds have documents:
  - [ ] Allies → NPC documents
  - [ ] Haven → Haven document
  - [ ] Mentor → NPC mentor document
  - [ ] Retainers → Ghoul documents
  - [ ] Herd → Herd description
- [ ] All links valid

---

## PC File Structure

```
[character]/
├── [character].md          ← Links to all below
├── npcs/                   ← Allies, Mentors
├── ghouls/                 ← Retainers
├── havens/
└── herd/
```

---

## Output Template

```markdown
# [Character Name]

**Clan**: [Clan]
**Sire**: [Sire Name]
**Generation**: [N]th
**Sect**: [Camarilla/Sabbat/Anarch/Independent]
**Concept**: [Brief concept]

## Personality

**Nature**: [Archetype]
**Demeanor**: [Archetype]

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
| Charisma | ●●○○○ |
| Manipulation | ●●●○○ |
| Appearance | ●●○○○ |

### Mental
| Attribute | Rating |
|-----------|--------|
| Perception | ●●●○○ |
| Intelligence | ●●○○○ |
| Wits | ●●●○○ |

## Abilities

### Talents
| Ability | Rating | Specialty |
|---------|--------|-----------|
| [Ability] | ●●○○○ | |

### Skills
| Ability | Rating | Specialty |
|---------|--------|-----------|
| [Ability] | ●●○○○ | |

### Knowledges
| Ability | Rating | Specialty |
|---------|--------|-----------|
| [Ability] | ●●○○○ | |

## Disciplines

| Discipline | Rating | Powers |
|------------|--------|--------|
| [Discipline] | ●●○○○ | [Powers at this level] |

## Backgrounds

| Background | Rating | Details |
|------------|--------|---------|
| [Background] | ●●○○○ | [Link to document or brief] |

## Virtues & Morality

| Trait | Rating |
|-------|--------|
| Conscience | ●●●○○ |
| Self-Control | ●●●○○ |
| Courage | ●●●○○ |
| Humanity | ●●●●●●○○○○ |

## Secondary Traits

| Trait | Value |
|-------|-------|
| Willpower | ●●●○○○○○○○ |
| Blood Pool | [N]/[Max] |

## Clan Weakness

[Description of how the Clan weakness manifests for this character]

## Merits & Flaws

| Merit/Flaw | Points | Description |
|------------|--------|-------------|
| [Name] | [+/-N] | [Brief description] |

## Description

[Physical appearance, mannerisms, typical dress]

## Background

[Character history, how they were Embraced, relationship with sire]

## Goals & Motivations

[What drives the character]
```
