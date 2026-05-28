# Spirit Module

Create spirit characters: ephemeral entities from across the Gauntlet.

## Important: Storyteller Characters

**Spirits are typically Storyteller NPCs only.** For player-controlled spirits, use the **Familiar module** instead.

---

## Spirit Traits

| Trait | Description |
|-------|-------------|
| **Willpower** | Mental resilience |
| **Rage** | Capacity for violence |
| **Gnosis** | Spiritual awareness, magical potency |
| **Essence** | Life force (Willpower × 5 minimum) |

**Charm dice pools**: Usually Gnosis or Willpower vs difficulty 6.

---

## Spirit Power Levels

| Rank | Willpower | Rage | Gnosis | Essence | Charms |
|------|-----------|------|--------|---------|--------|
| **Gaffling** (minor) | 2-4 | 2-4 | 2-4 | 10-20 | 3-5 |
| **Jaggling** (standard) | 4-6 | 4-6 | 4-6 | 20-40 | 5-8 |
| **Lord/Preceptor** | 7-9 | 6-9 | 7-9 | 50-100 | 8-12+ |
| **Celestine** | 10 | 8-10 | 10 | 100+ | Many |

---

## Spirit Categories

| Category | Examples |
|----------|----------|
| **Elementals** | Fire, water, wind, earth |
| **Naturae** | Forest, city, place spirits |
| **Conceptuals** | War, love, fear, justice |
| **Ancestors** | Ghosts, wraiths |
| **Totems** | Wolf, Raven, Spider |
| **Demons** | Various infernal |
| **Loa/Orishas** | Baron Samedi, Oshun |
| **Paradox Spirits** | Erinyes, Hex, Whisper |

---

## Spirit Charms

**Lookup**: `python scripts/lookup.py companion.spirit-charms spirit-charms --keys`

### Universal Charms
| Charm | Effect |
|-------|--------|
| Airt Sense | Navigate spirit realms |
| Materialize | Appear in physical world |
| Peek | Observe physical from Umbra |
| Re-Form | Reconstruct after destruction |

### Common Charms
| Charm | Essence | Effect |
|-------|---------|--------|
| Armor | 1 | +1 soak per Essence |
| Blast | 1 | Gnosis damage ranged attack |
| Cleanse | 2+ | Purify corruption |
| Create Element | 1-10 | Conjure appropriate element |
| Disorient | 1 | Target loses sense of place |
| Healing | 1+ | Heal 1 HL per Essence |
| Possession | varies | Control mortal host |
| Shapeshift | 1+ | Change form |

### New Charms (Gods & Monsters)
| Charm | Essence | Effect |
|-------|---------|--------|
| Bad Luck Curse | 1 | Turn successes into 1s |
| Bargain | 2 | +2 diff to binding rolls |
| Create Water | 1-10 | Conjure water |
| Deflect Harm | 1/HL | Block damage |
| False Wealth | varies | Illusory riches |
| Good Luck Charm | varies | Grant reroll |
| Jack In | — | Interface with electronics |
| Mirage | varies | Create illusions |
| Mislead | varies | Confuse decision-making |
| Plant Command | varies | Control plant life |
| Sand Storm | 8 | Elemental storm |
| Smoke Screen | 2 | Concealing fog |
| Spirit Gossip | 5 | Gather info from spirits |
| Teleport | 10/20 | Instant movement |

---

## Spirit Nature and Ban

### Nature
Determines: available Charms, personality, Essence sources, appearance.

### Ban
Restriction or compulsion — crucial for binding and negotiation. Examples:
- Fire spirits compelled by water
- Deal-makers cannot break sworn bargains
- Ancestor spirits must answer descendants

---

## Interacting with Physical World

| Method | Effect |
|--------|--------|
| **Manifestation** | Visible/audible but not solid |
| **Materialization** | Gains physical form (Essence drain) |
| **Possession** | Control mortal host (contested) |
| **Fetish** | Bound into physical object |

---

## Creating Spirit NPCs

1. **Determine Type and Rank**
2. **Assign Core Traits** (Willpower, Rage, Gnosis, Essence)
3. **Select Charms** (match spirit nature)
4. **Define Ban** (meaningful weakness/compulsion)
5. **Describe Appearance and Personality**
6. **Consider Relationships** (allies, enemies, mages)

---

## Spirit Archetypes

### Totem Spirits
High Gnosis, grant benefits to bonded groups.

### Elemental Spirits
Control/create their element, weakness to opposing element.

### Ancestor Spirits
High Gnosis, must answer descendants, cannot lie about past.

### Paradox Spirits
Related to Sphere that triggered them, punish/teach mages.

### Loa/Orishas
Wide variety of powers, specific offerings and protocols required.

---

## Output Template

```markdown
# [Spirit Name]

**Type**: [Elemental/Naturae/Conceptual/etc.]  
**Embodiment**: [What they represent]  
**Rank**: [Gaffling/Jaggling/Lord/Celestine]  

## Traits
**Willpower**: ●●●●●○○○○○  
**Rage**: ●●●●○○○○○○  
**Gnosis**: ●●●●●●○○○○  
**Essence**: ●●●●● ●●●●● ●●●●● ●●●●●

## Charms
- [Charm] — [Brief effect]
- [Charm] — [Brief effect]

## Ban
[What compels or restricts this spirit]

## Appearance
[How the spirit appears]

## Personality
[Behavior, goals, interactions]

## Notes
[Feeding habits, allies, enemies]
```
