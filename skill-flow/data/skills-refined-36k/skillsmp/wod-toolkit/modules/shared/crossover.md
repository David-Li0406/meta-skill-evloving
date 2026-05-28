# Shared Crossover Module

Guidelines for running multi-splat World of Darkness games and creating content that spans gamelines.

---

## Core Principles

### 1. Mage Rules Generally Win
When mechanical systems conflict, M20 rules typically take precedence because:
- Sphere magic is the most flexible system
- Mages can theoretically affect anything
- Other supernaturals have specific, limited powers

**Exception**: Entities follow their source game (Totems use W20, Spectres use Wr20, etc.)

### 2. Respect the Source Game
When creating content for a specific creature type, use that game's rules:
- Vampire powers → V20 Discipline mechanics
- Werewolf Gifts → W20 Gift mechanics
- Wraith Arcanoi → Wr20 Arcanoi mechanics

### 3. Keep Point Costs Per-Game
Don't mix character creation systems:
- V20/W20/Wr20/C20: 5 Background dots
- M20: 7 Background dots
- Different freebie costs per game

---

## The Umbra in Crossover

### Unified Structure

```
Physical World
     ↓ Gauntlet/Shroud
     ↓
┌────────────────────────────────────┐
│ Middle Umbra (Penumbra/Near/Deep)  │ ← W20 primary, M20 access
│   - Spirits, Totems, Banes         │
│   - CyberRealm = Digital Web       │
└────────────────────────────────────┘
     ↕ (connections)
┌────────────────────────────────────┐
│ High Umbra (Astral Reaches)        │ ← M20 primary
│   - Conceptual realms              │
│   - Mental/philosophical space     │
└────────────────────────────────────┘
     ↕ (connections)
┌────────────────────────────────────┐
│ Dark Umbra (Shadowlands/Tempest)   │ ← Wr20 primary
│   - Wraiths, Spectres              │
│   - Far Shores, Oblivion           │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ The Dreaming (separate)            │ ← C20 primary
│   - Connected but distinct         │
│   - Near/Far/Deep Dreaming         │
└────────────────────────────────────┘
```

### Access by Game

| Realm | V20 | W20 | M20 | Wr20 | C20 |
|-------|-----|-----|-----|------|-----|
| Middle Umbra | Rare (Auspex 5) | Primary | Spirit 3+ | No | Via Trods |
| High Umbra | No | Rare | Mind/Spirit | No | No |
| Dark Umbra | No | Rare, dangerous | Spirit 4+ | Primary | No |
| The Dreaming | No | Via Arcadia Gateway | Rare | No | Primary |

---

## Creature Interactions

### Vampires and Others

| With | Relationship | Notes |
|------|--------------|-------|
| Werewolves | **Hostile** | Wyrm-tainted in Garou eyes |
| Mages | **Varies** | Vampires are "pattern corruption" |
| Wraiths | **Limited** | Different realms; Necromancy connects |
| Changelings | **Rare** | Vampires have no Glamour |

### Werewolves and Others

| With | Relationship | Notes |
|------|--------------|-------|
| Vampires | **Hostile** | Leeches serve the Wyrm |
| Mages | **Wary** | Weaver-touched, but sometimes allies |
| Wraiths | **Distant** | Different Umbral layer |
| Changelings | **Respectful** | Wyld-touched; potential allies |

### Mages and Others

| With | Relationship | Notes |
|------|--------------|-------|
| Vampires | **Varies** | Useful pawns or dangerous threats |
| Werewolves | **Respectful** | Spirit allies; share Umbra |
| Wraiths | **Research** | Interesting phenomena |
| Changelings | **Curious** | Dreaming is fascinating |

---

## Mechanical Conflicts & Resolutions

### Spirit Mechanics
**Resolution**: Use W20 formula for Essence (Rage + Gnosis + Willpower)

Both W20 and M20 have spirit rules. When they conflict:
- Spirit hierarchy: W20 naming (Gaffling/Jaggling/Incarna/Celestine)
- High Umbra only: May use Lord/Preceptor for Incarna-rank
- Spirit template: Include both Chiminage (W20) AND Ban (M20)

### True Faith
**Resolution**: Shared mechanics, game-specific effects

True Faith works against all supernaturals but with different expressions:
- V20: Forces vampires to flee, damages at high levels
- W20: Resists Wyrm corruption
- M20: Functions as countermagick
- Wr20: Protects against possession

See `lookup.py shared.core true-faith`

### Spectres vs Spirits
**Resolution**: Distinct categories

- **Spectres** (Wr20): Shadow-consumed wraiths serving Oblivion
- **Spirits** (W20/M20): Ephemeral beings from the Umbra

Never use "Spectre" for hostile spirits. Use "Bane" or "hostile spirit" instead.

### Ancestor Spirits vs Wraiths
**Resolution**: Distinct categories

- **Ancestor Spirits**: W20 concept; spirit beings representing lineage
- **Wraiths**: Wr20 concept; actual ghosts of dead individuals

These are NOT the same beings viewed differently—they are separate creature types.

### Digital Web / CyberRealm
**Resolution**: Same place, different names

- W20 calls it the CyberRealm
- M20 calls it the Digital Web
- Use whichever name fits the game context

### Wyrm and Oblivion
**Resolution**: Leave ambiguous

Source material is intentionally vague about whether these are connected. Don't definitively state they are or aren't the same force.

---

## Creating Crossover Content

### Multi-Splat NPCs

When an NPC interacts with multiple creature types:
1. Stat them in their primary game system
2. Note how they appear to other creatures
3. Define their attitudes toward each creature type

Example:
```markdown
## Mikhail Voronstev

**Primary**: V20 Vampire (Tremere)
**How Garou See Him**: Wyrm-tainted leech, blood magic stinks of corruption
**How Mages See Him**: Interesting phenomenon, useful information source
**How Wraiths See Him**: Predator who feeds on life; some Necromancy awareness
```

### Cross-Game Locations

When a location is accessible to multiple creature types:
1. Define its physical characteristics
2. Note Umbral reflection (Penumbra)
3. Note Shadowlands reflection
4. Define Gauntlet/Shroud ratings
5. Note any Dreaming connections

Example:
```markdown
## The Crossroads Diner

**Physical**: Run-down roadside diner, always open, strange clientele
**Penumbra**: Reflects as a meeting place; spirits of travel/transaction gather
**Shadowlands**: Ghost of original owner still serves; several Fetters here
**Gauntlet**: 6 (moderate; many believe in "weird stuff" happening here)
**Shroud**: 5 (death echo from multiple murders over decades)
**Dreaming**: Minor trod crosses parking lot; Eshu sometimes stop by
```

### Cross-Game Organizations

Organizations that span creature types need:
- Clear membership criteria
- How different supernaturals interact within the group
- Power structure that accommodates different abilities

---

## Power Level Comparisons

These are rough guidelines only—individual characters vary wildly.

### Combat Capability (Raw)
| Creature | Low | Mid | High |
|----------|-----|-----|------|
| Mortal | — | — | — |
| Vampire | Neonate | Ancilla | Elder |
| Werewolf (Crinos) | Cliath | Fostern/Adren | Athro/Elder |
| Mage | Arete 1-2 | Arete 3-4 | Arete 5+ |
| Wraith | New | Established | Ancient |
| Changeling | Childling | Wilder | Grump w/Arts |

### Versatility
| Creature | Rating | Notes |
|----------|--------|-------|
| Mortal | ★ | Limited to mundane |
| Vampire | ★★★ | Disciplines cover specific areas |
| Werewolf | ★★★ | Gifts are specific but numerous |
| Mage | ★★★★★ | Spheres can do almost anything |
| Wraith | ★★ | Arcanoi are specialized |
| Changeling | ★★★ | Arts need Realms but flexible |

### Social Influence
| Creature | Mortal World | Supernatural World |
|----------|--------------|-------------------|
| Vampire | ★★★★★ | ★★★★ |
| Werewolf | ★ | ★★★ |
| Mage | ★★★ | ★★★ |
| Wraith | ★ | ★★ |
| Changeling | ★★ | ★★★ |

---

## Running Crossover Games

### Session Zero Considerations
1. Which games are represented?
2. How will different power levels be balanced?
3. What's the shared threat or goal?
4. How did these characters come together?
5. What house rules handle mechanical conflicts?

### Common Crossover Hooks
- **Shared Enemy**: Something threatens all creature types
- **Neutral Ground**: A location where truce is enforced
- **Mutual Interest**: Information or resources all sides need
- **Apocalyptic Threat**: End of the world concerns everyone

### Potential Issues
- **Spotlight Balance**: Mages can overshadow others
- **Tone Clash**: V20 horror vs W20 action vs C20 wonder
- **Mechanical Complexity**: Five different rule systems
- **Lore Contradictions**: Different games explain things differently

---

## Output Template (Crossover Content)

```markdown
# [Content Name]

**Primary Game**: [Which game's rules apply]
**Relevant Games**: [All games this content affects]

## Description
[Physical/basic description]

## By Game

### V20 Perspective
[How vampires view/interact with this]

### W20 Perspective
[How werewolves view/interact with this]

### M20 Perspective
[How mages view/interact with this]

### Wr20 Perspective
[How wraiths view/interact with this]

### C20 Perspective
[How changelings view/interact with this]

## Mechanics
[Any mechanical details, noting which game's rules apply]

## Story Hooks
[Plot possibilities involving multiple creature types]
```
