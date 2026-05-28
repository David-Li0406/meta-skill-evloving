# Grimoire Module

Create mechanically valid Grimoires for M20 using Prism of Focus Practice integration.

## Dependency

**If grimoire contains ROTES:** Read `modules/rote.md`, create full documents.

## What is a Grimoire?

A magical instructional text teaching: Practices (with ratings), Spheres, Abilities, Rotes, and potentially Awakening (Primers).

## Prism of Focus Integration

### Teaching Practice Ratings
Under Prism of Focus, grimoires teach **Practice ratings**, not just practices as binary traits:
- Grimoire Rank = maximum Practice rating it can teach
- Reader can learn Practice dots up to the grimoire's teaching level
- Practice dots from grimoires still require 2+ Associated Ability dots per Practice dot

### Learning Rotes from Grimoires
- Grimoire Rank must exceed the highest Sphere in the rote
- Rote cost is **halved** when learning from a grimoire
- Rotes must use Practices taught in the grimoire

## Rank and Points

| Rank | Description | Points | Max Teaching |
|------|-------------|--------|--------------|
| 1 | Primer | 3 | 1 |
| 2 | Journeyman | 6 | 2 |
| 3 | Advanced | 9 | 3 |
| 4 | Master's | 12 | 4 |
| 5 | Legendary | 15 | 5 |

**Points = 3 × Rank**

## Free Content (Every Grimoire)

- 1 Practice (teaches up to Rank dots)
- 1 Ability (associated with that Practice)
- 1 Sphere (up to Rank)

## Point Costs

| Content | Cost |
|---------|------|
| Additional Practice | 2 |
| Additional Sphere | 2 |
| Additional Ability | 1 |
| Rote | Sum of Sphere dots |
| Primer (Arete training) | 3 |

## Content Count Rule

```
Rotes + Practices + Spheres + Abilities + (1 if Primer) = Rank + 3
```

## Creation Workflow

1. **Concept** — Faction, purpose
2. **Rank** — 1-5
3. **Faction** — Query practices
4. **Free Content** — 1 Practice + 1 Ability + 1 Sphere
5. **Purchase Additional** — Stay within budget
6. **⛔ ROTES** — If any, read `modules/rote.md`, create documents
7. **Merits/Flaws** — See `references/grimoire/grimoire-merits-flaws.md`
8. **Physical Form** — Medium, language
9. **Verify Content Count** — Must = Rank + 3
10. **Document** — Link to rote files
11. **Validate**

## Point Validation Block

```
Base Points:           [3 × Rank] = X
+ Flaw Points:                    + X
= Available:                      = X

Spent:
- Additional Practices (N × 2):   - X
- Additional Spheres (N × 2):     - X  
- Additional Abilities (N × 1):   - X
- Rotes (total dots):             - X
= Remaining:                      = X (≥ 0)

Content: Rotes(X) + Practices(X) + Spheres(X) + Abilities(X) = X
Required: Rank + 3 = X
Status: [VALID/INVALID]
```

## Validation

- [ ] Rank 1-5
- [ ] Points spent ≤ available
- [ ] Content count = Rank + 3
- [ ] No trait above Rank
- [ ] All Abilities associated with a Practice in grimoire
- [ ] (If rotes) All rote files exist
- [ ] Rotes use only grimoire's Practices/Spheres/Abilities

## File Structure

```
[project]/
├── grimoires/
│   └── [grimoire].md     ← Links to ../rotes/
└── rotes/
    └── [rote].md
```

## Reference Data

```bash
python scripts/lookup.py rules.faction-practices faction-practices "Order of Hermes"
python scripts/lookup.py rules.practice-abilities practice-abilities "High Ritual Magick"
```

## Return Format (for library module)

```
Created: ./grimoires/zenos_mirror.md
Title: Zeno's Mirror
Rank: 2
```

---

## Black Books (Nephandic Grimoires)

Black Books are grimoires containing Fallen lore and dark rotes. Use standard grimoire creation with these additions.

### Additional Elements

- **Corruption potential:** Reading may require Willpower rolls to resist influence
- **Resonance:** Malignant, Destructive, Entropic, Corruptive
- **Prerequisites:** Some require Lore: Nephandi or specific Qlippothic advancement to comprehend
- **Danger rating:** Note how dangerous the book is to non-Fallen readers

### Sample Black Books

| Title | Contents | Faction Association |
|-------|----------|---------------------|
| Akaa' Et Nuon Ta ("Cry of the World") | Pre-human Malfean prophecies | Malfeans |
| The Annotated Protocols of Damian | Infernalist doctrine, pact templates | Infernalists |
| The Blargarian Mythos | K'llashaa cosmic horror, Lovecraftian entities | K'llashaa |
| The Ebon Broomstick Series | "Beginner's" corruption texts, gateway material | General |
| The Six Seals of Ganzir | Underworld gate rituals | Malfeans |
| The Hunter and the Prey | Lex Praedatorius philosophy | General |
| The Malleus Nefandorum | Anti-Nephandi hunting guide (used BY and AGAINST) | Hunters/Nephandi |
| The Sebel-el-Mafouh Whash | Egyptian dark magick | Infernalists |
| The Squirebook | Digital grimoire, meme magic | Heralds of Basilisk |
| The Thirteen Hours | Mammonite exploitation manual | Mammonites |

### Black Book Validation

In addition to standard grimoire validation:
- [ ] Corruption potential noted
- [ ] Resonance specified as malignant
- [ ] Prerequisites listed if any
- [ ] Danger to non-Fallen readers indicated
