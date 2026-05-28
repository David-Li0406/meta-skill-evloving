# Fomor Module

Create fomori (Bane-possessed humans/supernaturals) for W20.

## Creation Rule

**Total Taint value must equal or exceed total Power cost.**

## Fomori Types

### Standard Fomori
Humans possessed by Banes, either willingly (cultists) or forced (Pentex subjects).

### Fomori Breeds
Standardized "strains" created through Pentex processes:

| Breed | Specialty | Typical Use |
|-------|-----------|-------------|
| **Enticers** | Social predators, appear perfect | Seduction, recruitment |
| **Freakfeet** | Amphibious, webbed extremities | Underwater operations |
| **Hollow Men** | Empty husks, minimal personality | Disposable labor |
| **Toads** | Corporate infiltrators, grotesque in private | White-collar sabotage |

### Fomorachs
Unique, powerful fomori created through experimental processes. Each Fomorach is one-of-a-kind, often rivals Garou in power.

### Supernatural Fomori
Bane-possessed supernatural beings - vampires, mages, werewolves, changelings. Much rarer and more dangerous than human fomori.

## Powers (Examples)

### Combat Powers
| Power | Cost | Effect |
|-------|------|--------|
| Armored Skin | 4 | +2 soak |
| Berserker | 4 | Rage-like state |
| Claws | 3 | Str+1 agg |
| Extra Limbs | 5 | Additional arms/tentacles |
| Fangs | 2 | Str agg bite |
| Venomous Bite | 4 | Poison damage |

### Movement Powers
| Power | Cost | Effect |
|-------|------|--------|
| Extra Speed | 3/6 | +5/+10 yards per turn |
| Wall Walking | 3 | Climb any surface |
| Wings | 5 | Flight |
| Webbing | 3 | Spider-climb, web creation |

### Sensory Powers
| Power | Cost | Effect |
|-------|------|--------|
| Darksight | 2 | See in total darkness |
| Sense Prey | 3 | Track specific target type |
| Spirit Sight | 4 | See into Umbra |
| Scent Tracking | 2 | Enhanced smell |

### Special Powers
| Power | Cost | Effect |
|-------|------|--------|
| Body Expansion | 5 | Grow to large size |
| Regeneration | 7 | Heal like Garou |
| Chameleon Coloration | 3 | Camouflage |
| Infectious Touch | 5 | Spread corruption |
| Psychic Powers | Variable | Mind abilities |
| Immunity (Type) | 3-7 | Immune to specific damage |

## Taints (Examples)

### Physical Taints
| Taint | Value | Effect |
|-------|-------|--------|
| Deformity (Minor) | -1 | Concealable |
| Deformity (Major) | -3 | Obvious, -1 Social |
| Deformity (Severe) | -5 | Monstrous, -2 Social |
| Deterioration | -5 | Slowly dying |
| Phobia | -2 | Fear trigger |
| Allergic Reaction | -2 to -4 | Harmful substance |

### Mental Taints
| Taint | Value | Effect |
|-------|-------|--------|
| Madness | -3 | Derangement |
| Compulsion | -2 | Must obey trigger |
| Amnesia | -2 | Lost memories |
| Flashbacks | -2 | Trauma triggers |

### Spiritual Taints
| Taint | Value | Effect |
|-------|-------|--------|
| Wyrm Taint | -1 | Detectable (always present) |
| Bane Bondage | -3 | Bane can command |
| Spirit Magnet | -3 | Attracts hostile spirits |

## Supernatural Fomori Rules

When supernatural beings are Bane-possessed:

### Vampires
- Bane feeds on blood alongside vampire
- Beast and Bane may conflict
- Some Disciplines enhanced, others corrupted
- Blood bond doesn't protect against Bane influence

### Werewolves (Extremely Rare)
- Usually occurs during failed Rite of Passage
- Garou instinctively try to reject Bane
- Result is usually death or BSD conversion
- Survivors are hunted by all Garou

### Mages
- Avatar becomes Wyrm-tainted
- Resonance shifts to entropic
- Paradox often manifests as Wyrm corruption
- Technocracy and Traditions both hunt them

### Changelings
- Bane consumes Glamour
- Banal and Wyrm-tainted simultaneously
- Often go mad from contradictions
- Nightmare creatures even among fae

## Output Format

```markdown
# [Fomor Name]

**Type**: [Standard/Breed/Fomorach/Supernatural]
**Origin**: [How created - Pentex project/cult/forced possession]
**Allegiance**: [Pentex/Black Spirals/Independent/etc.]

## Base Being
[For supernatural fomori: original type and relevant traits]

## Attributes
Physical: Str X, Dex X, Sta X
Social: Cha X, Man X, App X
Mental: Per X, Int X, Wits X

## Powers ([X] points)
| Power | Cost | Effect |
|-------|------|--------|
| [Power] | [X] | [Description] |

## Taints ([X] points)
| Taint | Value | Manifestation |
|-------|-------|---------------|
| Wyrm Taint | -1 | [Always present] |
| [Taint] | [X] | [Description] |

## Appearance
[How corruption manifests visibly]

## Behavior
[Personality, goals, methods]

## Bane
[Type of Bane possessing them, if known]
```

## Reference Files

- `lookup.py fomor.powers-taints powers-taints` - Full power/taint lists
- `lookup.py fomor.fomori-breeds fomori-breeds` - Breed stat blocks
- `lookup.py fomor.fomorachs fomorachs` - Unique fomorach examples
- `lookup.py fomor.supernatural-fomori supernatural-fomori` - Rules for possessed supernaturals
