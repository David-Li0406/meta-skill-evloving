# Model Inventory

Complete inventory of models with implementation status.

**Legend:** ✅ Fully implemented | ⚠️ Partial | ❌ Not implemented | N/A Not applicable

## Characters App

### Core Models
| Model | List | Detail | Create | Update |
|-------|:----:|:------:|:------:|:------:|
| Character | ✅ | ✅ | ✅ | ✅ |
| Human | ✅ | ✅ | ✅ | ✅ |
| Group | ✅ | ✅ | ✅ | ✅ |
| Archetype | ✅ | ✅ | ✅ | ✅ |
| MeritFlaw | ✅ | ✅ | ✅ | ✅ |
| Specialty | ✅ | ✅ | ✅ | ✅ |
| Derangement | ✅ | ✅ | ✅ | ✅ |
| Background | ✅ | ✅ | ✅ | ✅ |

### Vampire (VtM)
| Model | List | Detail | Create | Update | Chargen |
|-------|:----:|:------:|:------:|:------:|:-------:|
| Vampire | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ghoul | ✅ | ✅ | ✅ | ✅ | ✅ |
| Revenant | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| VampireClan | ✅ | ✅ | ✅ | ✅ | N/A |
| Discipline | ✅ | ✅ | ✅ | ✅ | N/A |

### Werewolf (WtA)
| Model | List | Detail | Create | Update | Chargen |
|-------|:----:|:------:|:------:|:------:|:-------:|
| Werewolf | ❌ | ✅ | ⚠️ | ✅ | ✅ |
| Kinfolk | ❌ | ✅ | ✅ | ✅ | ✅ |
| Fera | ❌ | ✅ | ✅ | ✅ | ✅ |
| Tribe | ✅ | ✅ | ✅ | ✅ | N/A |
| Gift | ✅ | ✅ | ✅ | ✅ | N/A |
| Totem | ✅ | ✅ | ✅ | ✅ | N/A |

### Mage (MtA)
| Model | List | Detail | Create | Update | Chargen |
|-------|:----:|:------:|:------:|:------:|:-------:|
| Mage | ❌ | ✅ | ✅ | ✅ | ✅ |
| Companion | ❌ | ✅ | ✅ | ✅ | ✅ |
| Sorcerer | ❌ | ✅ | ✅ | ✅ | ✅ |
| Resonance | ✅ | ✅ | ✅ | ✅ | N/A |
| Rote | ✅ | ✅ | ✅ | ✅ | N/A |
| Effect | ✅ | ✅ | ✅ | ✅ | N/A |

### Other Gamelines
| Gameline | Status |
|----------|--------|
| Wraith (WtO) | Detail/Create/Update ✅, List ❌ |
| Changeling (CtD) | Detail/Create/Update ✅, List ❌ |
| Demon (DtF) | Detail/Create/Update ✅, List ❌ |
| Hunter (HtR) | ✅ Full implementation |
| Mummy (MtR) | ⚠️ Detail only |

## Items App

| Category | Models | Status |
|----------|--------|--------|
| Core | ItemModel, Weapon, MeleeWeapon, RangedWeapon | ✅ |
| Vampire | VampireArtifact, Bloodstone | ✅ |
| Werewolf | Fetish, Talen | ✅ |
| Mage | Wonder, Artifact, Charm, Grimoire, Periapt, Talisman | ✅ |
| Wraith | WraithArtifact, WraithRelic | ✅ |
| Changeling | Treasure, Dross | ✅ |
| Demon | Relic | ✅ |
| Hunter | HunterGear, HunterRelic | ✅ |
| Mummy | Ushabti, Vessel, MummyRelic | ❌ |

## Locations App

| Gameline | Models | Status |
|----------|--------|--------|
| Core | LocationModel, City | ✅ |
| Vampire | Haven, Domain, Elysium, TremereChantry, Rack, Barrens | ✅ |
| Werewolf | Caern | ✅ |
| Mage | Node, Sanctum, Chantry, Demesne, HorizonRealm, Library, RealityZone, Sector, ParadoxRealm | ✅ |
| Wraith | Citadel, Haunt, WraithFreehold, Byway, Nihil, Necropolis | ✅ |
| Changeling | Freehold ✅, Holding/Trod/DreamRealm ⚠️ | Mixed |
| Demon | Bastion, Reliquary | ✅ |
| Hunter | Safehouse, HuntingGround | ✅ |
| Mummy | Tomb, UndergroundSanctuary, CultTemple | ❌ |

## Game App

| Model | List | Detail | Create | Update |
|-------|:----:|:------:|:------:|:------:|
| Chronicle | ✅ | ✅ | ⚠️ | ❌ |
| Story | ✅ | ✅ | ✅ | ✅ |
| Week | ✅ | ✅ | ✅ | ✅ |
| Scene | ✅ | ✅ | ⚠️ | ❌ |
| Journal | ✅ | ✅ | ❌ | ⚠️ |

## Implementation Gaps

- **Missing List Views:** Most character types use generic index only
- **Mummy (MtR):** Detail views only, no create/update/forms
- **Missing Reference Views:** Sphere, MageFaction, Fellowship, Instrument, Practice, Paradigm (Mage); WraithFaction, Guild, Arcanos (Wraith)
