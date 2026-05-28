# Shared Spirit Module

Create spirit characters for any World of Darkness game.

## Important Notes

- **Spirits are typically Storyteller NPCs only**
- For player-controlled spirit companions, use game-specific modules (M20 Familiar, W20 Totem, etc.)
- This module provides unified spirit creation across all WoD games

---

## Spirit Traits

| Trait | Description |
|-------|-------------|
| **Willpower** | Mental resilience, resisting control |
| **Rage** | Capacity for violence |
| **Gnosis** | Spiritual awareness, magical potency |
| **Essence** | Life force = Rage + Gnosis + Willpower (W20 formula) |

**Charm dice pools**: Usually Gnosis or Willpower vs difficulty 6.

---

## Spirit Power Levels

| Rank | Name (Middle Umbra) | Name (High Umbra) | Will | Rage | Gnosis | Essence | Charms |
|------|---------------------|-------------------|------|------|--------|---------|--------|
| 1 | Gaffling | Gaffling | 2-4 | 2-4 | 2-4 | 10-20 | 3-5 |
| 2 | Jaggling | Jaggling | 4-6 | 4-6 | 4-6 | 20-40 | 5-8 |
| 3 | Incarna | Lord/Preceptor | 7-9 | 6-9 | 7-9 | 50-100 | 8-12+ |
| 4 | Celestine | Celestine | 10 | 8-10 | 10 | 100+ | Many |

---

## Spirit Categories

| Category | Examples | Typical Games |
|----------|----------|---------------|
| **Elementals** | Fire, water, wind, earth, metal | All |
| **Naturae** | Forest, city, place spirits | All |
| **Conceptuals** | War, love, fear, justice | All |
| **Pattern Spiders** | Weaver servants, order enforcers | W20, M20 |
| **Banes** | Wyrm-corrupted spirits | W20 |
| **Totems** | Wolf, Raven, Spider (pack patrons) | W20 |
| **Paradox Spirits** | Erinyes, Hex, Whisper | M20 |
| **Loa/Orishas** | Baron Samedi, Oshun | M20 |
| **Demons** | Various infernal entities | M20, V20 |

**Note**: Spectres (Wr20) are NOT spirits — they are Shadow-consumed wraiths.

---

## Spirit Nature and Restrictions

### Nature
Determines: available Charms, personality, Essence sources, appearance.

### Chiminage (W20 term)
What the spirit expects in exchange for aid:
- **Wyld spirits**: Chaos, interesting experiences, spontaneity
- **Weaver spirits**: Order, patterns, completed tasks, data
- **Wyrm spirits**: Corruption, suffering (avoid deals)
- **Gaian spirits**: Service to Gaia, nature protection

### Ban (M20 term)
Restriction or compulsion — crucial for binding and negotiation:
- Fire spirits compelled by water
- Deal-makers cannot break sworn bargains
- Ancestor spirits must answer descendants

**Include BOTH Chiminage and Ban** for comprehensive spirits.

---

## Charm Selection

**Reference**: `lookup.py shared.spirits charms`

### Universal (All Spirits)
- Airt Sense — Navigate spirit realms
- Re-Form — Reconstruct after destruction

### Common
- Armor, Blast, Cleanse, Healing, Materialize, Peek, Possession, Shapeshift, Swift Flight, Tracking

### By Type
- **Elementals**: Create Element, related elemental effects
- **Conceptuals**: Charms matching their concept
- **Banes**: Corruption, Incite Frenzy, Bane Protean
- **Weaver**: Calcify, Solidify Reality

---

## Creating Spirit NPCs

1. **Determine Type and Rank**
   - What does this spirit embody?
   - How powerful should it be?

2. **Assign Core Traits**
   - Willpower, Rage, Gnosis (from rank table)
   - Essence = Rage + Gnosis + Willpower

3. **Select Charms**
   - Universal charms (free)
   - 3-12+ additional based on rank
   - Must match spirit nature

4. **Define Chiminage AND Ban**
   - What does the spirit want? (Chiminage)
   - What restricts/compels it? (Ban)

5. **Describe Appearance and Personality**
   - How does it manifest?
   - What are its goals?

6. **Consider Relationships**
   - Brood/hierarchy
   - Allies and enemies
   - Relationship to PCs

---

## Game-Specific Considerations

### W20 (Werewolf)
- Primary game for spirit interaction
- Garou have Spirit Gifts for communication
- Fetishes bind spirits into objects
- Totems serve packs and tribes
- See `modules/w20/spirit.md` for Garou-specific details

### M20 (Mage)
- Spirit Sphere required to interact
- Familiars are spirit companions
- Paradox spirits punish vulgar magic
- See `modules/m20/spirit.md` for mage-specific details

### Wr20 (Wraith)
- Spirits rarely encountered
- Spectres are NOT spirits (different creature type)
- Dark Umbra has its own entities
- See `modules/wr20/spectre.md` for Spectres

### C20 (Changeling)
- Chimera use similar mechanics
- Glamour replaces Gnosis
- Dreaming is separate from Umbra
- See `modules/c20/chimera.md` for Chimera

---

## Output Template

```markdown
# [Spirit Name]

**Type**: [Elemental/Naturae/Conceptual/Totem/etc.]  
**Embodiment**: [What they represent]  
**Rank**: [Gaffling/Jaggling/Incarna/Celestine]  
**Brood**: [If applicable]

## Traits
| Trait | Rating |
|-------|--------|
| Willpower | ●●●●●○○○○○ |
| Rage | ●●●●○○○○○○ |
| Gnosis | ●●●●●●○○○○ |
| Essence | ●●●●● ●●●●● ●●●●● [total] |

## Charms
- [Charm] — [Brief effect]
- [Charm] — [Brief effect]

## Chiminage
[What offerings/services the spirit expects]

## Ban
[What compels or restricts this spirit]

## Appearance
[How the spirit manifests]

## Personality & Goals
[Behavior, motivations, typical interactions]

## Notes
[Relationships, feeding habits, special considerations]
```

---

## Validation Checklist

- [ ] Rank-appropriate trait values
- [ ] Essence = Rage + Gnosis + Willpower
- [ ] Charms match spirit nature
- [ ] Both Chiminage AND Ban defined
- [ ] Appearance described
- [ ] Personality established
