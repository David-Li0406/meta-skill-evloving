# Library Module

Create Libraries (magical text collections) for M20.

## Invoked By

This module is called when creating:
- **Mage PCs** with Library background
- **Sorcerer PCs** with Library background
- **Chantries** that include a library
- Standalone libraries for campaign use

When invoked from character creation, Library rank = Background rating.

## Dependency

**BEFORE creating any library:**
1. Read `modules/grimoire.md`
2. Create 2-4 full grimoire documents
3. Then create library linking to them

## Library Statistics

### Rank (1-5)

| Rank | Description | Max Teaching |
|------|-------------|--------------|
| 1 | Basic introductory | 1 |
| 2 | Solid collection | 2 |
| 3 | Excellent, rare | 3 |
| 4 | Outstanding, unique | 4 |
| 5 | Legendary, priceless | 5 |

### Required Grimoire Count

| Library Rank | Grimoires |
|--------------|-----------|
| 1 | 2 |
| 2 | 2-3 |
| 3 | 3-4 |
| 4 | 3-4 |
| 5 | 4 |

## Creation Workflow

1. **Concept** — Faction, focus, location
2. **Rank** — 1-5
3. **Faction** — Dominant paradigm
4. **Focus** — Specializations
5. **⛔ GRIMOIRES** — Read `modules/grimoire.md`, create 2-4 documents
6. **Physical Space** — Description, organization
7. **Curator** — Who manages it?
8. **Document** — Link to grimoire files
9. **Validate**

## Output Format

```markdown
# [Library Name]

**Rank:** [1-5] | **Faction:** [Name] | **Focus:** [Specialty]

## Concept
[1-2 paragraphs]

## Statistics

| Stat | Value |
|------|-------|
| Rank | [1-5] |
| Faction | [Name] |
| Max Teaching | [= Rank] |

## Notable Grimoires

| Title | Rank | Document |
|-------|------|----------|
| [Name](../grimoires/file.md) | X | Brief summary |

**All grimoires have full documents.**

## Physical Description
## Access
## Curator
## Story Hooks
```

## Validation

- [ ] Rank 1-5
- [ ] 2-4 grimoire documents exist
- [ ] All grimoire links valid
- [ ] No grimoire rank > library rank
- [ ] Faction alignment coherent

## File Structure

```
[project]/
├── libraries/
│   └── [library].md      ← Links to ../grimoires/
├── grimoires/
│   └── [grimoire].md     ← Links to ../rotes/
└── rotes/
```

## Reference Data

```bash
python scripts/lookup.py rules.faction-practices faction-practices "Order of Hermes"
```

## Return Format (for parent modules)

```
Created: ./libraries/paradox_codices.md
Name: The Paradox Codices
Rank: 2
Grimoires: [./grimoires/tome_a.md, ./grimoires/tome_b.md]
```
