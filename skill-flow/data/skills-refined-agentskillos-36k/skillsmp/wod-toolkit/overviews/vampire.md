# V20 Overview — Vampire: The Masquerade 20th Anniversary Edition

Creates mechanically valid Vampire: The Masquerade 20th Anniversary Edition content with automatic dependency resolution and background expansion.

## Workflow

1. **Identify content type** → Select appropriate module
2. **Read module** → Load `modules/v20/[type].md` before starting
3. **For PCs** → Expand backgrounds via `modules/v20/background-expansion.md`
4. **Create content** → Follow module workflow
5. **Validate** → Check module validation list
6. **Link documents** → Connect all sub-documents to parent

## Module Selection

### Characters
| Type | Module |
|------|--------|
| Vampire (PC/NPC) | `modules/v20/character.md` |
| Ghoul (Vassal/Independent/Elder) | `modules/v20/ghoul.md` |
| Revenant | `modules/v20/revenant.md` |
| Mortal | `modules/v20/mortal.md` |
| Animal Ghoul | `modules/v20/animal-ghoul.md` |

### Bloodlines (Lore of the Bloodlines)
| Bloodline | Module |
|-----------|--------|
| Baali | `modules/v20/bloodline.md` |
| Daughters of Cacophony | `modules/v20/bloodline.md` |
| Gargoyle (all variants) | `modules/v20/gargoyle.md` |
| Harbingers of Skulls | `modules/v20/bloodline.md` |
| Kiasyd | `modules/v20/bloodline.md` |
| Nagaraja | `modules/v20/bloodline.md` |
| Salubri (all branches) | `modules/v20/salubri.md` |
| Samedi | `modules/v20/bloodline.md` |
| True Brujah | `modules/v20/bloodline.md` |

### War Ghouls & Monstrous Creations
| Type | Module |
|------|--------|
| Szlachta | `modules/v20/monstrous-creations.md` |
| Vozhd | `modules/v20/monstrous-creations.md` |

### Organizations
| Type | Module |
|------|--------|
| Ghoul Organizations | `modules/v20/ghoul-organizations.md` |
| Coterie | `modules/v20/coterie.md` |

### Locations
| Type | Module |
|------|--------|
| Haven | `modules/v20/haven.md` |
| Domain | `modules/v20/domain.md` |
| Major Landmarks | `modules/v20/locations.md` |

### Blood Magic
| Type | Module |
|------|--------|
| Thaumaturgy (Tremere) | `modules/v20/thaumaturgy.md` |
| Necromancy (Giovanni) | `modules/v20/necromancy.md` |
| Abyss Mysticism (Lasombra) | See `lookup.py v20.disciplines blood-sorcery-lotc` |
| Dur-An-Ki (Assamite) | See `lookup.py v20.disciplines blood-sorcery-lotc` |

### Setting & Lore
| Type | Module |
|------|--------|
| Sects (Camarilla/Sabbat/Anarch) | `modules/v20/sects.md` |
| Paths of Enlightenment | `modules/v20/paths-of-enlightenment.md` |

### Social Systems (V20 Companion)
| Type | Module |
|------|--------|
| Titles & Positions | `modules/v20/titles.md` |
| Prestation & Boons | `modules/v20/prestation.md` |

---

## Character Creation Quick Reference

### Vampire
| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Disciplines | 3 (Clan only) |
| Backgrounds | 5 |
| Virtues | 7 (+ 3 base) |
| Humanity | Conscience + Self-Control |
| Willpower | Courage |
| Freebies | 15 |

### Ghoul
| Category | Dots |
|----------|------|
| Attributes | 6/4/3 (+ 9 base) |
| Abilities | 11/7/4 (cap 3) |
| Disciplines | 1 |
| Backgrounds | 5 |
| Virtues | 7 Camarilla/Independent; 5 Sabbat (+ 3 base) |
| Humanity | Conscience + Self-Control |
| Willpower | Courage |
| Freebies | 21 |

### Revenant
| Category | Dots |
|----------|------|
| Attributes | 6/4/3 (+ 9 base) |
| Abilities | 11/7/4 (cap 3) |
| Disciplines | 1 family + 1 Potence |
| Backgrounds | 5 |
| Virtues | 5 (+ 3 base) |
| Humanity/Path | Max 5 at creation |
| Willpower | Courage |
| Freebies | 21 |

---

## Generation Quick Reference

| Generation | Max Blood Pool | Blood/Turn | Max Trait |
|------------|----------------|------------|-----------|
| 13th | 10 | 1 | 5 |
| 12th | 11 | 1 | 5 |
| 11th | 12 | 1 | 5 |
| 10th | 13 | 1 | 5 |
| 9th | 14 | 2 | 5 |
| 8th | 15 | 3 | 5 |
| 7th | 20 | 5 | 6 |
| 6th | 30 | 6 | 7 |

---

## Clan Quick Reference

| Clan | Disciplines | Weakness |
|------|-------------|----------|
| Assamite | Celerity, Obfuscate, Quietus | Damaged by Kindred blood |
| Brujah | Celerity, Potence, Presence | +2 diff to resist frenzy |
| Followers of Set | Obfuscate, Presence, Serpentis | +2 diff in bright light |
| Gangrel | Animalism, Fortitude, Protean | Gain animal features in frenzy |
| Giovanni | Dominate, Necromancy, Potence | Feeding causes extra damage |
| Lasombra | Dominate, Obtenebration, Potence | No reflection |
| Malkavian | Auspex, Dementation, Obfuscate | Permanent derangement |
| Nosferatu | Animalism, Obfuscate, Potence | Appearance 0 |
| Ravnos | Animalism, Chimerstry, Fortitude | Must indulge vice |
| Toreador | Auspex, Celerity, Presence | Entranced by beauty |
| Tremere | Auspex, Dominate, Thaumaturgy | Blood bonded to Clan |
| Tzimisce | Animalism, Auspex, Vicissitude | Must rest with native soil |
| Ventrue | Dominate, Fortitude, Presence | Restricted feeding |
| Caitiff | (Any three) | No Clan support, social stigma |

---

## Freebie Costs

| Trait | Vampire | Ghoul/Revenant |
|-------|---------|----------------|
| Attribute | 5 | 5 |
| Ability | 2 | 2 |
| Discipline | 7 | 10 |
| Background | 1 | 1 |
| Virtue | 2 | 2 |
| Humanity/Path | 2 | 1 |
| Willpower | 1 | 1 |

---

## Data Lookup

```bash
# Clans
python scripts/lookup.py v20.rules clans "Brujah"

# Bloodlines (LotB)
python scripts/lookup.py v20.rules bloodlines "Salubri"

# Disciplines
python scripts/lookup.py v20.disciplines disciplines "Potence"

# Abilities
python scripts/lookup.py v20.character abilities "Brawl"

# Backgrounds
python scripts/lookup.py v20.character backgrounds "Herd"

# Merits & Flaws
python scripts/lookup.py v20.character merits-flaws --find "generation"

# Archetypes (shared)
python scripts/lookup.py shared.core archetypes "Rebel"
```

---

## Reference Files

### Character (`references/v20/character/`)
- `attributes.json` — Physical/Social/Mental Attributes
- `abilities.json` — Talents, Skills, Knowledges
- `backgrounds.json` — All Backgrounds
- `ghoul-backgrounds.json` — Ghoul-specific Backgrounds
- `archetypes.json` → Use `lookup.py shared.core archetypes`
- `merits-flaws.json` — All Merits and Flaws
- `clan-merits-flaws.json` — Clan-specific Merits and Flaws
- `bloodline-merits-flaws.json` — Bloodline-specific Merits and Flaws
- `ghoul-merits-flaws.json` — Ghoul-specific Merits and Flaws
- `revenant-families.json` — Revenant family data
- `paths.json` — Paths of Enlightenment

### Rules (`references/v20/rules/`)
- `clans.json` — All 13 Clans + Caitiff
- `bloodlines.json` — All 9 bloodlines
- `generation.json` — Generation chart
- `titles.json` — Sect titles
- `prestation.json` — Boon system

### Disciplines (`references/v20/disciplines/`)
- `disciplines.json` — All Discipline powers 1-5
- `bloodline-disciplines.json` — Unique bloodline Disciplines
- `combination-disciplines.json` — Combination Disciplines
- `elder-disciplines.json` — Level 6+ powers
