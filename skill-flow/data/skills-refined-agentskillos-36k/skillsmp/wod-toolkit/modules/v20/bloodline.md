# Bloodline Module

Create mechanically valid Bloodline characters for V20 using Lore of the Bloodlines.

## Overview

Bloodlines are vampire lineages distinct from the 13 main Clans. They may be:
- Offshoots of existing Clans (Kiasyd from Lasombra)
- Survivors of destroyed Clans (Salubri, Harbingers of Skulls)
- Artificial creations (Gargoyles)
- Independent origins (Baali, Nagaraja, True Brujah)

## Bloodline Selection

| Bloodline | Disciplines | Weakness | Sect |
|-----------|-------------|----------|------|
| Baali | Daimonion, Obfuscate, Presence | Vulnerable to faith, attracts pestilence | Independent |
| Daughters of Cacophony | Fortitude, Melpominee, Presence | Hear constant "Fugue" music | Independent |
| Gargoyles | Flight, Fortitude, Visceratika | Mind control susceptibility (WP treated as -2) | Camarilla/Independent |
| Harbingers of Skulls | Auspex, Fortitude, Necromancy | Appearance 0, corpse-like appearance | Sabbat |
| Kiasyd | Dominate, Mytherceria, Obtenebration | Cold iron vulnerability, compelled to count | Independent |
| Nagaraja | Auspex, Dominate, Necromancy | Must consume flesh as well as blood | Tal'Mahe'Ra |
| Salubri | Auspex, Fortitude, Obeah | Third eye, hunted by Tremere | Independent |
| Samedi | Fortitude, Obfuscate, Thanatosis | Appearance 0, rotting appearance | Independent |
| True Brujah | Potence, Presence, Temporis | Cannot frenzy, cannot spend WP for auto-successes | Tal'Mahe'Ra |

---

## Special Bloodline Rules

### Gargoyles
Use `modules/gargoyle.md` for Gargoyle characters. They have:
- Three variants (Scout, Sentinel, Warrior) with different Disciplines
- Two creation methods (ritual vs. Embrace)
- Special rituals that can be cast on them

### Salubri
Use `modules/salubri.md` for Salubri characters. They have:
- Two branches: Healers (Obeah) and Warriors (Valeren)
- Eastern variant (Wu Zao)
- Antitribu in the Sabbat

### Kiasyd
May optionally take Necromancy instead of Dominate, but gain:
- Clan Enmity (Giovanni) — no freebie compensation
- Clan Enmity (Harbingers of Skulls) — no freebie compensation

---

## Creation Steps

1. **PC/NPC** — Default PC
2. **Concept** — Name, Bloodline, Sect, Generation
3. **Nature & Demeanor** — From `lookup.py character.archetypes archetypes`
4. **Attributes** — 7/5/3 across Physical/Social/Mental (+ 1 base each)
5. **Abilities** — 13/9/5 across Talents/Skills/Knowledges (cap 3)
6. **Disciplines** — 3 dots in Bloodline Disciplines only
7. **Backgrounds** — 5 dots. Note which need sub-documents
8. **Virtues** — 7 dots (+ 1 base each in Conscience, Self-Control, Courage)
9. **Humanity** — Conscience + Self-Control (typically 5-7)
10. **Willpower** — Equal to Courage rating
11. **Blood Pool** — Start with roll or max based on Generation
12. **Merits & Flaws** — Include bloodline-specific options from `lookup.py character.bloodline-merits-flaws bloodline-merits-flaws`
13. **⛔ BACKGROUNDS (PC)** — Create documents for Allies/Haven/Mentor/Retainers
14. **Freebies** — 15 + Flaws - Merits. Spend exactly.
15. **Specialties** — Required for 4+ traits
16. **Description** — Include bloodline-specific physical markers
17. **Bloodline Weakness** — Document specific weakness details
18. **Document** — Link all sub-documents
19. **Validate**

---

## Bloodline-Specific Notes

### Baali
- **Weakness**: Vulnerable to True Faith. Characters with True Faith deal their rating in aggravated damage per turn of holy symbol contact.
- **Unique**: Often have demonic patrons or coven affiliations
- **Social**: Viewed as devils by most Kindred; must maintain secrecy

### Daughters of Cacophony
- **Weakness**: The Fugue — constant background music only they hear. Can be distracting.
- **Unique**: Many have performance backgrounds (singers, musicians, speakers)
- **Factions**: Choristers (groups), Soloists (loners), Sisters of the Fugue (mystics), Quiet Celebrities (industry)

### Gargoyles
- **Weakness**: Willpower treated as 2 lower for resisting mind control
- **Unique**: May have additional variant weakness (see `modules/gargoyle.md`)
- **Appearance**: Stone-like skin, wings, inhuman features

### Harbingers of Skulls
- **Weakness**: Appearance 0, corpse-like/skull-faced appearance
- **Unique**: Must wear masks or concealing clothing in public
- **Goal**: Vengeance against Giovanni

### Kiasyd
- **Weakness**: Cold iron deals 1 aggravated per turn of contact. Compelled to count scattered objects.
- **Appearance**: Tall, pale, solid black eyes, elongated features
- **Unique**: Blood alchemy, scholarly obsession

### Nagaraja
- **Weakness**: Must eat flesh equal to blood consumed (roughly 1 lb per blood point). Feeding is always lethal.
- **Unique**: Part of Tal'Mahe'Ra (True Black Hand)
- **Social**: Must be extremely careful about Masquerade

### Salubri
- **Weakness**: Third eye opens when using Disciplines or sensing pain. Eye weeps blood when feeding (lose 1 BP). Hunted by Tremere.
- **Branches**: Healers (Obeah), Warriors (Valeren)
- **Social**: Must hide identity; many pose as Caitiff

### Samedi
- **Weakness**: Appearance 0, rotting corpse appearance with real decay and smell
- **Unique**: Strong voudoun connections
- **Social**: Often work in death-related industries

### True Brujah
- **Weakness**: Cannot frenzy. Cannot spend Willpower for automatic successes.
- **Unique**: Often infiltrate regular Brujah
- **Factions**: Unmakers (seek revenge), Guardians (preserve lore)

---

## Discipline References

```bash
# Get bloodline discipline powers
python scripts/lookup.py disciplines.bloodline-disciplines bloodline-disciplines "Temporis"

# Get bloodline combination disciplines
python scripts/lookup.py disciplines.bloodline-combination-disciplines bloodline-combination-disciplines --find "true_brujah"

# Get bloodline merits and flaws
python scripts/lookup.py character.bloodline-merits-flaws bloodline-merits-flaws --find "kiasyd"
```

---

## Allocation Summary

| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Disciplines | 3 (Bloodline only) |
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
| Discipline (Bloodline) | 7 |
| Discipline (Non-Bloodline) | 7 (requires justification) |
| Virtue | 2 |
| Humanity | 2 |
| Willpower | 1 |

---

## Validation

- [ ] Attributes: 15 dots (+ 9 base = 24 total)
- [ ] Abilities: 27 dots, none > 3
- [ ] Disciplines: 3 dots, all from Bloodline list
- [ ] Backgrounds: 5 dots
- [ ] Virtues: 10 total (7 + 3 base)
- [ ] Humanity = Conscience + Self-Control
- [ ] Willpower = Courage
- [ ] Flaws ≤ 7 points
- [ ] Freebies spent exactly
- [ ] Bloodline weakness documented with specific details
- [ ] Bloodline-specific appearance noted (if applicable)
- [ ] (PC) All relevant backgrounds have documents
- [ ] All links valid

---

## Output Template

```markdown
# [Character Name]

**Bloodline**: [Bloodline]
**Sire**: [Sire Name]
**Generation**: [N]th
**Sect**: [Camarilla/Sabbat/Anarch/Independent/Tal'Mahe'Ra]
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

## Bloodline Weakness

[Detailed description of how the bloodline weakness manifests for this character]

## Merits & Flaws

| Merit/Flaw | Points | Description |
|------------|--------|-------------|
| [Name] | [+/-N] | [Brief description] |

## Description

[Physical appearance, bloodline-specific features, mannerisms, typical dress]

## Background

[Character history, how they were Embraced, relationship with sire, bloodline-specific history]

## Goals & Motivations

[What drives the character]
```
