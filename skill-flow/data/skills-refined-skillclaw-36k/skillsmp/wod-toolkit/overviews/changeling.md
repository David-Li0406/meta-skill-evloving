# C20 Overview — Changeling: The Dreaming 20th Anniversary Edition

Creates mechanically valid Changeling: the Dreaming 20th Anniversary Edition content with automatic dependency resolution and background expansion.

## Workflow

1. **Identify content type** → Select appropriate module
2. **Read module** → Load `modules/c20/[type].md` before starting
3. **For PCs** → Expand backgrounds via `modules/c20/background-expansion.md`
4. **Create content** → Follow module workflow
5. **Validate** → Check module validation list
6. **Link documents** → Connect all sub-documents to parent

## Module Selection

### Characters
| Type | Module |
|------|--------|
| Kithain (standard changeling) | `modules/c20/character.md` |
| Kinain (fae-blooded mortal) | `modules/c20/kinain.md` |
| Thallain (dark fae) | `modules/c20/thallain.md` |
| Dauntain (corrupted changeling) | `modules/c20/dauntain.md` |
| Adhene/Denizen | `modules/c20/adhene.md` |
| Nunnehi | `modules/c20/nunnehi.md` |
| Inanimae | `modules/c20/inanimae.md` |

### Creatures & Items
| Type | Module |
|------|--------|
| Chimera (companion/creature) | `modules/c20/chimera.md` |
| Treasure | `modules/c20/treasure.md` |

### Locations & Organizations
| Type | Module |
|------|--------|
| Freehold | `modules/c20/freehold.md` |
| Glade | `modules/c20/glade.md` |
| Motley/Oathcircle | `modules/c20/motley.md` |
| Noble Household | `modules/c20/household.md` |

### Systems
| Type | Module |
|------|--------|
| Oath | `modules/c20/oath.md` |

---

## Character Creation Quick Reference

### Kithain
| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Arts | 3 |
| Realms | 5 |
| Backgrounds | 5 |
| Glamour | by Seeming |
| Willpower | by Seeming |
| Banality | by Seeming |
| Freebies | 15 |

### Seeming Values
| Seeming | Glamour | Willpower | Banality |
|---------|---------|-----------|----------|
| Childling | 5 | 1 | 1 |
| Wilder | 4 | 2 | 3 |
| Grump | 3 | 5 | 5 |

### Freebie Costs
| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Art | 5 |
| Realm | 3 |
| Background | 1 |
| Glamour | 3 |
| Willpower | 1 |

---

## Standard Kiths

| Kith | Affinity | Frailty |
|------|----------|---------|
| Boggan | Actor | Cannot abide laziness |
| Clurichaun | Actor | Addiction to revelry |
| Eshu | Scene | Wanderlust |
| Nocker | Prop | Creations always flawed |
| Piskie | Actor | Kleptomaniac tendencies |
| Pooka | Nature | Cannot resist a prank |
| Redcap | Nature | Must consume flesh |
| Satyr | Fae | Slave to passions |
| Selkie | Nature | Coat vulnerability |
| Sidhe (Arcadian) | Time | Banality wounds |
| Sidhe (Autumn) | Prop | Must honor oaths |
| Sluagh | Prop | Cannot speak above whisper |
| Troll | Fae | Oath-bound |

---

## Regional Fae

### African (Land of Ancient Dreams)
| Kith | Concept | Affinity |
|------|---------|----------|
| Biloko | Traditional guardians | Nature |
| Okubili | Duality seekers | Fae |
| Djedi | Urban magicians | Fae |
| Kuino | Merchants/traders | Prop |
| Obambo | Relic collectors | Prop |

### South American (Bellatierra)
| Kith | Concept | Affinity |
|------|---------|----------|
| Alicanto | Metal-eating treasure hunters | Prop |
| Boraro | Nature guardians | Nature |
| Encantado | Freshwater shape-shifters | Actor |
| Llorona | Grief-bearers | Actor |
| Sachamama | Giant serpent gossips | Actor |

### Australian (Dreamtime Spirit Beings)
| Kith | Concept | Affinity |
|------|---------|----------|
| Dulklorrkelorrkeng | Night-flying wish-granters | Fae |
| Mimis | Land caretakers | Nature |
| Rainmakers | Law keepers | Nature |
| Yawkyawk | Water protectors | Nature |

### Middle Eastern (Al-Hilal Al-Khaseeb Jinn)
| Kith | Concept | Affinity |
|------|---------|----------|
| Ifrit | Fire warriors | Fae |
| Lilin | Seducers | Actor |
| Qareen | Spiritual doubles | Fae |
| Shaytan | Tempters | Actor |

---

## Arts & Realms Quick Reference

### Arts (Magic Types)
| Art | Domain |
|-----|--------|
| Chicanery | Deception, illusion |
| Legerdemain | Sleight of hand, theft |
| Primal | Nature, elements |
| Soothsay | Fate, prophecy |
| Sovereign | Authority, command |
| Wayfare | Travel, movement |
| Chronos | Time manipulation |
| Dream-Craft | Dream manipulation |
| Infusion | Crafting, enchantment |
| Metamorphosis | Shapeshifting |
| Naming | True names |
| Pyretics | Fire, heat |
| Skycraft | Air, weather |
| Spirit Link | Spirit communication |
| Tale-Craft | Stories, narrative |

### Realms (Targets)
| Realm | Targets |
|-------|---------|
| Actor | Mortals, humans |
| Fae | Changelings, chimera, Glamour |
| Nature | Animals, plants |
| Prop | Crafted objects |
| Scene | Areas, environments |
| Time | Duration, timing |

---

## Data Lookup

```bash
# Kiths
python scripts/lookup.py c20.kith kiths "sidhe"
python scripts/lookup.py c20.kith regional-africa --keys

# Arts & Realms
python scripts/lookup.py c20.arts chicanery --keys
python scripts/lookup.py c20.realms realms --keys

# Thallain
python scripts/lookup.py c20.antagonist thallain --keys

# Gallain
python scripts/lookup.py c20.gallain adhene --keys

# Archetypes (shared)
python scripts/lookup.py shared.core archetypes "Trickster"
```

---

## Reference Files

### C20-Specific (`references/c20/`)
- `kith/` — Standard kiths, regional fae
- `arts/` — Art powers by level
- `realms/` — Realm descriptions
- `character/` — Abilities, backgrounds
- `freehold/` — Freehold creation rules
- `chimera/` — Chimera creation
- `antagonist/` — Thallain
- `gallain/` — Adhene, Inanimae
- `rules/` — Cantrip casting, Banality

### Shared (`references/shared/`)
- `core/` — Archetypes, attributes, abilities

## The Dreaming

The Dreaming is **connected but separate** from the Umbra. It is the realm of dreams, Glamour, and fae essence.

### Layers
- **Near Dreaming**: Close to mortal dreams, relatively safe
- **Far Dreaming**: Deeper, stranger, more dangerous
- **Deep Dreaming**: The most ancient and alien regions

### Connections
- **Arcadia Gateway**: Near Realm that borders the Dreaming
- **Trods**: Ancient pathways crossing both Umbra and Dreaming

**Note**: Chronos (C20 time Art) is entirely separate from the Time Sphere (M20).
