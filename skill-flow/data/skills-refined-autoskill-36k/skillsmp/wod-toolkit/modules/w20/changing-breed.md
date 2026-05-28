# Changing Breed Module

Create Fera (non-Garou shapeshifters) for W20 Changing Breeds.

## Workflow

1. Select Fera type → Load `lookup.py changing-breeds.[fera] [fera]`
2. Choose breed (homid/animal/metis where applicable)
3. Determine aspect/auspice (varies by Fera)
4. Allocate starting traits per Fera rules
5. Select starting Gifts (breed + aspect/general)
6. Apply Fera-specific rules

## Available Fera

| Fera | Animal | Starting WP | Unique Mechanic |
|------|--------|-------------|-----------------|
| Ajaba | Hyena | 3 | Aspects (Dawn/Midnight/Dusk), Obligation Renown |
| Ananasi | Spider | 3-4 | Blood Pool (no Rage), Aspects + Factions |
| Bastet | Cats | Varies by tribe | Pryio, Tribes, Den-Realms |
| Corax | Raven | 3 | Rage 1/Gnosis 6, Eye-Drinking, Gold allergy |
| Gurahl | Bear | 6 | Progressive auspices, Rage for Str/Sta |
| Kitsune | Fox | 5 | Paths, Tails = Rank, Ju-Fu magic |
| Mokolé | Reptiles | Varies | Solar/Seasonal auspices, Archid Characteristics, Mnesis |
| Nagah | Serpent | 4 | Seasonal auspices, Nests, Ananta |
| Nuwisha | Coyote | Varies | All Ragabash, Faces of Coyote |
| Ratkin | Rat | Varies | Aspects, Plagues, Birthing Madness |
| Rokea | Shark | 4 | Brightwaters/Dimwater/Darkwater, Kunmind frenzy |

## Character Creation Summary

All Changing Breeds use standard Garou allocation unless noted:
- **Attributes**: 7/5/3 (priority)
- **Abilities**: 13/9/5 (cap 3 at creation)
- **Backgrounds**: 5
- **Gifts**: 3 (typically 1 breed + 1 aspect + 1 general)
- **Freebies**: 15

### Freebie Costs (Same as Garou)
| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 |
| Gift (Level 1) | 7 |
| Rage | 1 |
| Gnosis | 2 |
| Willpower | 1 |

## Quick Reference by Fera

### Ajaba
- **Breeds**: Homid/Metis/Hyaenid
- **Aspects**: Dawn (Rage 5/Gnosis 1), Midnight (Rage 3/Gnosis 3), Dusk (Rage 1/Gnosis 5)
- **Renown**: Ferocity, Cunning, Obligation
- **Forms**: Homid, Anthros, Crinos, Crocas, Hyaenid
- **Details**: `lookup.py changing-breeds.ajaba ajaba`

### Ananasi
- **Blood Pool**: 10 (replaces Rage)
- **Breeds**: Homid (WP 3/Gnosis 1), Arachnid (WP 4/Gnosis 5)
- **Aspects**: Tenere (Weaver), Hatar (Wyrm), Kumoti (Wyld)
- **Factions**: Myrmidon (warriors), Viskr (judges/mystics), Wyrsta (questioners)
- **Forms**: Homid, Lilian, Pithus, Crawlerling
- **Special**: No silver vulnerability, can't frenzy normally
- **Details**: `lookup.py changing-breeds.ananasi ananasi`

### Bastet
- **Breeds**: Homid (Gnosis 1), Metis (Gnosis 3), Feline (Gnosis 5)
- **Pryio**: Daylight, Twilight, Night (personality, not auspice)
- **Tribes**: Bagheera, Balam, Bubasti, Ceilican, Khan, Pumonca, Qualmi, Simba, Swara
- **Forms**: Homid, Sokto, Crinos, Chatro, Feline
- **Special**: Cannot step sideways without Gift, solitary
- **Details**: `lookup.py changing-breeds.bastet bastet`

### Corax
- **All Corax**: Rage 1, Gnosis 6, Willpower 3
- **Breeds**: Homid, Corvid (both get Raven's Gifts: +1 Subterfuge/Enigmas/Dodge)
- **Forms**: Homid, Crinos, Corvid (3 forms only)
- **Special**: Silver immunity, Gold vulnerability, Eye-drinking
- **Details**: `lookup.py changing-breeds.corax corax`

### Gurahl
- **Willpower**: 6 (all)
- **Breeds**: Homid (Gnosis 4), Ursine (Gnosis 5)
- **Auspices**: Arcas → Uzmati → Kojubat → Kieh → Rishi (progressive)
- **Forms**: Homid, Arthren, Crinos, Bjornen, Ursus
- **Special**: Rage boosts Str/Sta, 5+ successes to frenzy, Bhernocht
- **Details**: `lookup.py changing-breeds.gurahl gurahl`

### Kitsune
- **Willpower**: 5 (all), +1 free Dexterity
- **Breeds**: Kojin/Homid (Gnosis 3), Shinju/Metis (Gnosis 4), Roko/Fox (Gnosis 5)
- **Paths**: Kataribe (Rage 2), Gukutsushi (Rage 2), Doshi (Rage 3), Eji (Rage 4)
- **Forms**: Hitogata, Sambuhenge, Koto, Juko, Kyubi
- **Special**: Tails = Rank, Ju-Fu paper magic, no regeneration
- **Details**: `lookup.py changing-breeds.kitsune kitsune`

### Mokolé
- **Breeds**: Homid (Gnosis 2), Suchid (Gnosis 4)
- **Solar Auspices**: Rising Sun (WP 3), Noonday Sun (WP 5), Setting Sun (WP 3), Shrouded Sun (WP 4), Midnight Sun (WP 4), Decorated Sun (WP 5), Eclipsed Sun (WP 5)
- **Seasonal Auspices** (Makara/Zhong Lung): Hemanta, Zarad, Grisma, Vasanta
- **Forms**: Homid, Archid, Suchid (varies by varna)
- **Special**: Archid Characteristics = Gnosis, Gold & Silver vulnerability, Mnesis
- **Details**: `lookup.py changing-breeds.mokole mokole`

### Nagah
- **Willpower**: 4 (all)
- **Breeds**: Balaram/Homid (Gnosis 1), Ahi/Metis (Gnosis 3), Vasuki/Serpent (Gnosis 5)
- **Auspices**: Kamakshi/Spring (Rage 3), Kartikeya/Summer (Rage 4), Kamsa/Autumn (Rage 3), Kali/Winter (Rage 4)
- **Forms**: Balaram, Silkaram, Azhi Dahaka, Kali Dahaka, Vasuki
- **Special**: Sacred Secret, Nests, Ananta, Wani patrons
- **Details**: `lookup.py changing-breeds.nagah nagah`

### Nuwisha
- **Breeds**: Homid (Gnosis 1), Latrani (Gnosis 5)
- **Auspices**: All treated as Ragabash (Luna's trick)
- **Forms**: Homid, Tsitsu, Manabozho, Sendeh, Latrani
- **Totems**: Faces of Coyote (Coyote, Kishijoten, Kokopelli, Loki, Oghma, Ptah, Raven, Ti Malice, Xochipilli)
- **Special**: Humor replaces Honor, Umbral Danse
- **Details**: `lookup.py changing-breeds.nuwisha nuwisha`

### Ratkin
- **Breeds**: Homid (Gnosis 1), Metis (—), Rodens (Gnosis 5)
- **Aspects**: Tunnel Runner (Rage 1), Shadow Seer (Rage 2), Knife Skulker (Rage 3), Warrior (Rage 5), Freak Aspects
- **Forms**: Homid, Crinos, Rodens (3 forms, no Glabro/Hispo)
- **Special**: Birthing Plague/Madness, Blood Memory, Plagues organization
- **Details**: `lookup.py changing-breeds.ratkin ratkin`

### Rokea
- **Willpower**: 4 (all)
- **Breeds**: Homid (Gnosis 1, Same-Bito only), Squamus (Gnosis 5)
- **Auspices**: Brightwaters (Rage 5), Dimwater (Rage 4), Darkwater (Rage 3)
- **Forms**: Homid, Glabrus, Gladius, Chasmus, Squamus
- **Special**: Kunmind (2 successes to frenzy, 4+ for Thrall), Sending, immortal
- **Details**: `lookup.py changing-breeds.rokea rokea`

## Validation Checklist

- [ ] Correct breed selected with appropriate restrictions
- [ ] Starting Rage/Gnosis/Willpower match Fera type
- [ ] Gifts appropriate to breed + aspect/path + general lists
- [ ] Fera-specific rules applied (blood pool, no regeneration, etc.)
- [ ] Forms noted with correct statistics
- [ ] Renown type matches Fera (not all use Glory/Honor/Wisdom)
- [ ] Background restrictions observed (varies by Fera)

## Output Format

```markdown
# [Character Name]

**Fera**: [Type]  
**Breed**: [Breed]  
**Aspect/Auspice/Path**: [As appropriate]

## Traits
**Rage**: X | **Gnosis**: X | **Willpower**: X

## Attributes
[Standard format]

## Abilities
[Standard format]

## Backgrounds
[With Fera restrictions noted]

## Gifts
| Gift | Level | Source | System |
|------|-------|--------|--------|

## Forms
| Form | Str | Dex | Sta | Man | App | Special |
|------|-----|-----|-----|-----|-----|---------|

## [Fera-Specific Section]
[Blood pool for Ananasi, Archid for Mokolé, etc.]

## Notes
[Fera-specific restrictions, culture, etc.]
```

---

## Mockery Breeds (Pentex Creations)

Artificial shapeshifters created by Pentex's Project Lycaon. **Not true Fera** - they have different rules and are typically antagonist-only.

| Breed | Forms | Specialty | Reference |
|-------|-------|-----------|-----------|
| War Wolves | 2 (Lupus, Crinos) | Kinfolk hunting | `mockery-breeds.json`, `war-wolves.json` |
| Anurana | 3 | Polluted waterways | `mockery-breeds.json` |
| Samsa | 2 | Urban infiltration | `mockery-breeds.json` |
| Kerasi | 3 | Shock troops (Africa) | `mockery-breeds.json` |
| Yeren | 2 | Corporate espionage | `mockery-breeds.json`, `yeren.json` |

**Key differences from true Fera**:
- Artificial creation (genetic engineering + Bane possession)
- Sterile (except Anurana under specific conditions)
- Most cannot learn Gifts (Yeren are exception)
- No spiritual connection to Gaia
- Wyrm-tainted (detectable)

For full creation rules, see `modules/mockery-breed.md`.

---

## Fallen Fera (Corrupted Changing Breeds)

Each Fera type has members who fell to Wyrm corruption. Unlike Mockery Breeds, these were once true Gaia-serving shapeshifters.

| Fera | Fallen Name | Status | See |
|------|-------------|--------|-----|
| Ananasi | Antara | Hidden among Ananasi | `ananasi.json` |
| Bastet | Histpah (Liar-Kings) | Rare | `bastet.json` |
| Corax | Buzzards | Rare individuals | `corax.json` |
| Mokole | Mnetics | Extremely rare | `mokole.json` |
| Nuwisha | Bitter-Grins | Small groups | `nuwisha.json` |
| Ratkin | Mad Destroyers | Common | `ratkin.json` |
| Rokea | Balefire Sharks | Growing | `rokea.json` |

**Creating Fallen Fera**: Use standard Fera creation, then add:
- Wyrm taint (always detectable)
- Corruption-specific traits (see "fallen" section in each Fera file)
- Derangements (often)
- Changed patron (Wyrm-spirit instead of original totem)

**Redemption**: Theoretically possible for most (unlike Black Spiral Dancers who walked the Spiral), but extremely difficult and often fatal.
