# M20 Overview — Mage: The Ascension 20th Anniversary Edition

Creates mechanically valid Mage: The Ascension 20th Anniversary Edition content with automatic dependency resolution and background expansion. Supports Technocracy Reloaded, Book of the Fallen (Nephandi), Rich Bastard's Guide, and Lore of the Traditions.

## Workflow

1. **Identify content type** → Select appropriate module
2. **Read module** → Load `modules/m20/[type].md` before starting
3. **For PCs** → Expand backgrounds via `modules/m20/background-expansion.md`
4. **Create content** → Follow module workflow
5. **Validate** → Check module validation list
6. **Link documents** → Connect all sub-documents to parent

## Module Selection

### Characters
| Type | Module |
|------|--------|
| Tradition Mage (including Nephandi) | `modules/m20/character.md` |
| Disparate Craft Mage | `modules/m20/character.md` |
| Technocrat (any Convention) | `modules/m20/technocrat.md` |
| Sorcerer/Hedge Wizard/Psychic | `modules/m20/sorcerer.md` |
| Human companion (acolyte, consor) | `modules/m20/human-companion.md` |
| Familiar | `modules/m20/familiar.md` |
| Spirit/Bygone/Construct | `modules/m20/other-companion.md` |
| Technocratic Being (HIT Mark, clone) | `modules/m20/technocratic-being.md` |
| Goetic demons | `modules/m20/goetic-demon.md` |
| Nephandic servitors | `modules/m20/nephandic-servitor.md` |

### Magical Content
| Type | Module |
|------|--------|
| Rote (Tradition) | `modules/m20/rote.md` |
| Procedure/Adjustment (Technocracy) | `modules/m20/procedure.md` |
| Wonder/Talisman | `modules/m20/wonder.md` |
| Technocratic Equipment | `modules/m20/technocratic-equipment.md` |
| Grimoire (including Black Books) | `modules/m20/grimoire.md` |
| Library | `modules/m20/library.md` |
| Weapon | `modules/m20/weapon.md` |
| Sorcerer ritual | `modules/m20/sorcerer-ritual.md` |
| Sorcerer alchemy | `modules/m20/sorcerer-alchemy.md` |
| Sorcerer enchantment | `modules/m20/sorcerer-enchantment.md` |

### Locations
| Type | Module |
|------|--------|
| Chantry (Tradition) | `modules/m20/chantry.md` |
| Construct (Technocracy) | `modules/m20/construct.md` |
| Horizon Realm | `modules/m20/horizon-realm.md` |
| Paradox Realm | `modules/m20/paradox-realm.md` |
| Node | `modules/m20/node.md` |
| Sanctum | `modules/m20/sanctum.md` |
| Sector (Digital Web) | `modules/m20/sector.md` |

### Organizations
| Type | Module |
|------|--------|
| Amalgam (Technocratic team) | `modules/m20/amalgam.md` |
| Nephandic cult | `modules/m20/nephandic-cult.md` |
| Nephandic faction | `modules/m20/nephandic-faction.md` |

### Customization
| Type | Module |
|------|--------|
| Custom Tenet | `modules/m20/tenet.md` |
| Custom Practice | `modules/m20/practice.md` |
| New sorcerer Path | `modules/m20/sorcerer-path.md` |
| New psychic phenomenon | `modules/m20/psychic.md` |
| Qlippothic progression | `modules/m20/qlippoth.md` |
| Infernal pacts | `modules/m20/infernal-pact.md` |

---

## Tradition vs Technocracy vs Disparate Quick Reference

| Element | Tradition | Technocracy | Disparate Craft |
|---------|-----------|-------------|-----------------|
| Primary Stat | Arete | Enlightenment | Arete |
| Magic Effects | Rotes | Procedures | Rotes |
| Organization | Tradition + Sect | Convention + Methodology | Craft + subfaction |
| Group | Cabal | Amalgam | Cabal/Creyente/Conclave |
| Location | Chantry | Construct | Varies by Craft |
| Focus Binding | Can transcend | Permanently bound | Can transcend |

---

## The Disparate Alliance

The Disparate Alliance is a loose coalition of Crafts — magickal traditions that exist outside both the Council of Nine Traditions and the Technocratic Union. Use `modules/m20/character.md` for Craft mages with the appropriate faction selection.

### Alliance Structure
| Tier | Crafts | Commitment |
|------|--------|------------|
| **Forerunners** | Ngoma, Templar Knights, Taftani, Hollow Ones | Most committed to Alliance |
| **Middlers** | Ahl-i-Batin, Kahu, Sisters of Hippolyta, Wu Lung | Cautiously supportive |
| **Outsiders** | Bata'a, Children of Knowledge, Orphans | Tentatively involved |

### Quick Craft Reference
| Craft | Affinity | Alt Affinity | Focus |
|-------|----------|--------------|-------|
| Ahl-i-Batin | Correspondence | Mind | Unity through subtlety |
| Bata'a | Spirit (varies by Clan) | — | African Diaspora/Voudoun |
| Children of Knowledge | Matter | Prime | Alchemy, transformation |
| Hollow Ones | Entropy | Any | Post-modern eclecticism |
| Kahu | Spirit | Forces | Hawaiian mana guardians |
| Ngoma | Spirit | Prime | African scholar-priests |
| Orphans | Any | — | Self-taught independents |
| Sisters of Hippolyta | Life | Spirit/Mind | Amazon warrior-mystics |
| Taftani | Forces | Matter | Persian weavers of truth |
| Templar Knights | Prime | Forces | Christian warrior-mystics |
| Wu Lung | Spirit | — | Chinese celestial mages |

### Bata'a Seven Clans
| Clan | Affinity | Instrument |
|------|----------|------------|
| Kongo | Correspondence | Transmission |
| Igbo | Entropy | Augury |
| Akan | Forces | Cleromancy |
| Mande | Life | Rootwork |
| Fon | Correspondence | Transmission |
| Ewe | Mind | Clairvoyance |
| Yoruba | Spirit | Possession |

### Data Lookup for Crafts
```bash
# All Crafts with subfactions
python scripts/lookup.py m20.rules subfactions crafts

# Specific Craft
python scripts/lookup.py m20.rules subfactions crafts Kahu

# Craft-specific rotes
python scripts/lookup.py m20.rote crafts

# Craft merits/flaws
python scripts/lookup.py --search "craft" m20.character
```

---

## Character Creation Quick Reference

### Mage
| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Backgrounds | 7 |
| Spheres | 6 (Affinity free) |
| Arete | 1 |
| Willpower | 5 |
| Quintessence | Avatar rating |
| Freebies | 15 |

### Sorcerer/Psychic
| Category | Dots |
|----------|------|
| Attributes | 6/4/3 (+ 9 base) |
| Abilities | 11/7/4 (cap 3) |
| Backgrounds | 5 |
| Numina (Paths or Psychic) | 5 |
| Willpower | 5 |
| Freebies | 21 |

### Freebie Costs
| Trait | Mage | Sorcerer |
|-------|------|----------|
| Attribute | 5 | 5 |
| Ability | 2 | 2 |
| Background | 1 | 1 |
| Willpower | 1 | 1 |
| Arete | 4 | — |
| Sphere | 7 | — |
| Path/Psychic | — | 7 |
| Ritual | — | 2 |

---

## The Five Conventions (Technocracy)

| Convention | Focus | Affinity Spheres |
|------------|-------|------------------|
| Iteration X | Technology, cybernetics | Data, Forces, Matter, Prime |
| New World Order | Information, control | Data, Entropy, Mind |
| Progenitors | Biology, genetics | Entropy, Life, Mind, Prime |
| Syndicate | Economics, desire | Entropy, Mind, Prime |
| Void Engineers | Space, dimensions | Correspondence, Dim Sci, Forces |

### 6TP Rank System
| Rank | Title | Enlightened? |
|------|-------|--------------|
| T0 | Affiliate/Citizen | No |
| T1 | Operative | Usually No |
| T1+ | Initiated Operative | Yes |
| T2 | Agent | Yes |
| T3 | Supervisor | Yes |
| T4 | Symposium Member | Yes |
| T5 | Upper Management | Yes |

### Equipment Categories (= Wonder Equivalents)
| Category | Equivalent | Reusability |
|----------|------------|-------------|
| Gadget | Charm | Single-use |
| Trinket | Minor item | Reusable, simple |
| Device | Talisman | Reusable, complex |
| Invention | Artifact | Unique |
| Enhancement | Implant | Permanent |
| Matrix | Periapt | Power source |
| Primer | Grimoire | Consumable text |

---

## Sphere Quick Reference

| Rank | Capability |
|------|------------|
| 1 | Perception only |
| 2 | Manipulate existing |
| 3 | Significant manipulation, conjure (+Prime 2) |
| 4 | Drastic transformation |
| 5 | Mastery |

### Technocratic Sphere Names
| Traditional | Technocratic |
|-------------|--------------|
| Correspondence | Data |
| Spirit | Dimensional Science |
| Others | Same |

---

## Data Lookup

```bash
# Traditions/Conventions
python scripts/lookup.py m20.character tradition-npcs --keys
python scripts/lookup.py m20.technocracy conventions "Iteration_X"

# Spheres
python scripts/lookup.py references/m20/spheres/correspondence.md
python scripts/lookup.py references/m20/spheres/forces.md

# Equipment
python scripts/lookup.py m20.technocracy equipment --keys
python scripts/lookup.py m20.wonder common-effects --find "teleport"

# Sorcery
python scripts/lookup.py m20.sorcerer paths --keys
python scripts/lookup.py m20.sorcerer psychic-phenomena "Telepathy"

# Archetypes (shared)
python scripts/lookup.py shared.core archetypes "Visionary"

# Spirits (shared)
python scripts/lookup.py shared.spirits charms --keys
```

---

## Reference Files

### M20-Specific (`references/m20/`)
- `character/` — abilities, backgrounds, merits-flaws, tradition-npcs
- `spheres/` — individual sphere descriptions
- `technocracy/` — conventions, equipment, methodologies
- `sorcerer/` — paths, psychic-phenomena, affiliations
- `nephandi/` — qlippoth, investments
- `wonder/` — common-effects, templates
- `grimoire/` — templates, merits-flaws
- `horizon-realm/` — creation rules, templates
- `node/` — resonance, templates
- `rote/` — lore-of-traditions-rotes, templates

### Shared (`references/shared/`)
- `spirits/` — hierarchy, charms, types (for familiars, umbrood)
- `umbra/` — structure (for Spirit travel)
- `core/` — archetypes, attributes, abilities
