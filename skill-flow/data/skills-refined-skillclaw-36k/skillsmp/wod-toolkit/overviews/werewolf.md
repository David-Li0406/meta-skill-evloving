# W20 Overview — Werewolf: The Apocalypse 20th Anniversary Edition

Creates mechanically valid Werewolf: The Apocalypse 20th Anniversary Edition content.

## Workflow

1. **Identify content type** → Select module from tables below
2. **Read module** → Load `modules/w20/[type].md` before starting
3. **For PCs** → Expand backgrounds via `modules/w20/background-expansion.md`
4. **Create content** → Follow module workflow
5. **Validate** → Check module validation list

## Module Selection

### Characters
| Type | Module |
|------|--------|
| Garou (Werewolf) | `modules/w20/character.md` |
| Kinfolk | `modules/w20/kinfolk.md` |
| Fera/Changing Breed | `modules/w20/changing-breed.md` |
| Fomor | `modules/w20/fomor.md` |
| Kami | `modules/w20/kami.md` |

### Groups
| Type | Module |
|------|--------|
| Pack | `modules/w20/pack.md` |

### Antagonists (Book of the Wyrm)
| Type | Module |
|------|--------|
| Black Spiral Dancer | `modules/w20/black-spiral-dancer.md` |
| Mockery Breed | `modules/w20/mockery-breed.md` |
| Fallen Fera | `modules/w20/fallen-fera.md` |

### Spiritual Content
| Type | Module |
|------|--------|
| Gift | `modules/w20/gift.md` |
| Rite | `modules/w20/rite.md` |
| Fetish | `modules/w20/fetish.md` |
| Talen | `modules/w20/talen.md` |
| Spirit | `modules/shared/spirit.md` (unified) |
| Bane | `modules/w20/bane.md` |
| Totem | `modules/w20/totem.md` |

### Locations
| Type | Module |
|------|--------|
| Caern | `modules/w20/caern.md` |
| Sept | `modules/w20/sept.md` |
| Umbral Realm | `modules/w20/umbral-realm.md` |
| Umbral Phenomena | `modules/w20/umbral-phenomena.md` |
| Anchorhead | `modules/w20/anchorhead.md` |

---

## Garou Quick Reference

| Category | Allocation |
|----------|------------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Backgrounds | 5 |
| Gifts | 3 (1 breed, 1 auspice, 1 tribe) |
| Freebies | 15 |

**Freebie Costs**: Attribute 5, Ability 2, Background 1, Gift (L1) 7, Rage 1, Gnosis 2, Willpower 1

| Breed | Gnosis | | Auspice | Rage | Starting Renown |
|-------|--------|-|---------|------|-----------------|
| Homid | 1 | | Ragabash | 1 | Glory 2, Honor 1 |
| Metis | 3 | | Theurge | 2 | Glory 1, Wisdom 2 |
| Lupus | 5 | | Philodox | 3 | Glory 1, Honor 2 |
| | | | Galliard | 4 | Glory 2, Wisdom 1 |
| | | | Ahroun | 5 | Glory 2, Honor 1 |

**Tribe Willpower**: Black Furies 3, Bone Gnawers 4, Children of Gaia 4, Fianna 3, Get of Fenris 3, Glass Walkers 3, Red Talons 3, Shadow Lords 3, Silent Striders 3, Silver Fangs 3, Stargazers 4, Uktena 3, Wendigo 4

---

## Changing Breeds Quick Reference

| Fera | Animal | WP | Unique Mechanic |
|------|--------|-----|-----------------|
| Ajaba | Hyena | 3 | Aspects (Dawn/Midnight/Dusk) |
| Ananasi | Spider | 3-4 | Blood Pool (no Rage) |
| Bastet | Cats | Varies | Tribes, Pryio |
| Corax | Raven | 3 | Rage 1/Gnosis 6, Eye-drinking |
| Gurahl | Bear | 6 | Progressive Auspices |
| Kitsune | Fox | 5 | Paths, Tails = Rank |
| Mokolé | Reptiles | Varies | Archid, Mnesis |
| Nagah | Serpent | 4 | Sacred Secret, Nests |
| Nuwisha | Coyote | Varies | All Ragabash |
| Ratkin | Rat | Varies | Aspects, Birthing Plague |
| Rokea | Shark | 4 | Kunmind, Immortal |

---

## Umbral Quick Reference

### Near Realms
| Realm | Aspect | Theme |
|-------|--------|-------|
| Arcadia Gateway | Wyld | Fae dreams |
| Flux Realm | Wyld | Pure chaos |
| Pangaea | Wyld | Prehistoric Earth |
| CyberRealm | Weaver | Digital world |
| Malfeas | Wyrm | Heart of corruption |
| Wolfhome | Gaia | Garou sanctuary |

See `references/shared/umbra/` for unified Umbral structure.

### Penumbral Phenomena
| Type | Nature |
|------|--------|
| Blight | Urban Wyrm/Weaver corruption |
| Chimare | Metaphor made real |
| Glen | Wyld purity sanctuary |
| Wylding | Pure chaos zone |

---

## Data Lookup

```bash
# Tribes, Gifts, Rites
python scripts/lookup.py w20.rules tribes "Silver Fangs"
python scripts/lookup.py w20.gift gifts-by-source --find "Sense Wyrm"
python scripts/lookup.py w20.rite rites-by-type "mystic_rites"

# Totems, Spirits, Fetishes
python scripts/lookup.py shared.spirits totems "war"
python scripts/lookup.py shared.spirits types "nature_spirits"
python scripts/lookup.py w20.fetish fetishes-by-level "level_4"

# Umbral Content
python scripts/lookup.py shared.umbra near-realms "cyberrealm"
python scripts/lookup.py w20.umbra tribal-homelands "black_furies"

# Archetypes (shared)
python scripts/lookup.py shared.core archetypes "Rebel"
```

---

## Reference Files

### W20-Specific (`references/w20/`)
- `rules/` — breeds, auspices, tribes, backgrounds
- `character/` — metis-deformities, metis-camps
- `gift/` — gifts-by-source, gifts-changing-ways
- `rite/` — rites-by-type, rites-changing-ways
- `totem/` — totems, totem-creation-guide
- `fetish/` — fetishes-by-level, talens
- `fomor/` — powers-taints, fomori-breeds
- `changing-breeds/` — individual Fera data
- `caern/` — caern-creation-guide
- `sept/` — sept-positions
- `umbra/` — tribal-homelands, phenomena

### Shared (`references/shared/`)
- `spirits/` — hierarchy, charms, types, banes, totems
- `umbra/` — structure, near-realms
- `core/` — archetypes, attributes, abilities
