# Legion Module

Reference for the Eight Legions of Stygia—the organizational structure of the Hierarchy.

## What are Legions?

Legions are the primary organizational divisions of Stygian society. Wraiths are assigned to Legions based on **how they died**, not by choice.

---

## The Eight Legions

### The Emerald Legion
**Death by Chance/Accident**

| Aspect | Detail |
|--------|--------|
| **Deathlord** | The Emerald Lord |
| **Seat** | Seat of Thorns |
| **Deathmarks** | Green tinge, random injury marks |
| **Deaths** | Accidents, mishaps, wrong place/wrong time |
| **Reputation** | Fatalistic, superstitious, pragmatic |

**Values**:
1. Luck is fickle—be prepared
2. Community supports survival
3. Take what you can get
4. Talk emeralds (opportunities), not thorns (problems)

---

### The Skeletal Legion
**Death by Pestilence/Disease**

| Aspect | Detail |
|--------|--------|
| **Deathlord** | The Skeletal Lord |
| **Seat** | Seat of Dust |
| **Deathmarks** | Sores, lesions, pallor, visible illness |
| **Deaths** | Disease, plague, infection |
| **Reputation** | Patient, methodical, macabre humor |

**Notable**: Largest Legion, often rivals the Grim Legion.

---

### The Grim Legion
**Death by Violence/Combat**

| Aspect | Detail |
|--------|--------|
| **Deathlord** | The Smiling Lord |
| **Seat** | Seat of Burning Waters |
| **Deathmarks** | Wounds, scars, battle damage |
| **Deaths** | Murder, war, violence |
| **Reputation** | Martial, aggressive, honorable |

**Notable**: Largest military force, constant rivalry with Skeletal Legion.

---

### The Penitent Legion
**Death by Passion**

| Aspect | Detail |
|--------|--------|
| **Deathlord** | The Ashen Lady |
| **Seat** | Seat of Succor |
| **Deathmarks** | Signs of excess, broken hearts |
| **Deaths** | Love, jealousy, crimes of passion |
| **Reputation** | Emotional, redemption-focused |

**Notable**: Many seek atonement; strong counseling tradition.

---

### The Iron Legion
**Death by Age/Natural Causes**

| Aspect | Detail |
|--------|--------|
| **Deathlord** | The Quiet Lord |
| **Seat** | Seat of Shadows |
| **Deathmarks** | Aged appearance, weathered features |
| **Deaths** | Old age, natural decline |
| **Reputation** | Wise, conservative, bureaucratic |

**Notable**: Many ancient wraiths; strong institutional knowledge.

---

### The Silent Legion
**Death by Despair/Suicide**

| Aspect | Detail |
|--------|--------|
| **Deathlord** | The Quiet (collective) |
| **Seat** | Seat of Silence |
| **Deathmarks** | Self-inflicted wounds, rope marks, etc. |
| **Deaths** | Suicide, despair, giving up |
| **Reputation** | Contemplative, supportive, understanding |

**Notable**: Strong counseling focus; prevents "re-suicide."

---

### The Legion of Paupers
**Death by Poverty/Neglect**

| Aspect | Detail |
|--------|--------|
| **Deathlord** | The Beggar Lord |
| **Seat** | Seat of Golden Tears |
| **Deathmarks** | Malnourishment, exposure damage |
| **Deaths** | Starvation, exposure, neglect |
| **Reputation** | Resourceful, resentful, community-minded |

**Notable**: Often overlooked; strong mutual aid networks.

---

### The Legion of Fate
**Death by Destiny/Mystery**

| Aspect | Detail |
|--------|--------|
| **Deathlord** | The Lady of Fate |
| **Seat** | Mobile/Hidden |
| **Deathmarks** | Cryptic, often unclear |
| **Deaths** | Mysterious, prophetic, fate-driven |
| **Reputation** | Enigmatic, prophetic, respected |

**Notable**: Smallest Legion; the Lady of Fate predates Charon.

---

## Legion Ranks

### Standard Hierarchy

| Rank | Role |
|------|------|
| **Deathlord** | Legion supreme leader |
| **Anacreon** | Regional commander |
| **Overlord** | City-level leader |
| **Marshal** | Military commander |
| **Centurion** | Unit leader |
| **Legionnaire** | Standard member |
| **Conscript** | New recruit |

### Necropolis Ranks

| Rank | Role |
|------|------|
| **Governor** | Necropolis ruler (usually Anacreon) |
| **Regent** | Deputy/administrator |
| **Proctor** | District supervisor |
| **Legate** | Liaison between Legions |

---

## Legion Assignment

### Automatic Assignment
Wraiths are assigned based on death type. There's usually no choice.

### Edge Cases
- Multiple causes: Dominant cause determines Legion
- Unclear death: Legion of Fate or Investigation
- Refusal: Renegade status

### Changing Legions
Extremely rare. Requires:
- Deathlord approval (both)
- Exceptional circumstances
- Political maneuvering

---

## Status Background

The **Status** background reflects Legion rank:

| Rating | Approximate Rank |
|--------|------------------|
| 1 | Recognized Legionnaire |
| 2 | Trusted member, minor duties |
| 3 | Centurion or equivalent |
| 4 | Marshal or Overlord |
| 5 | Anacreon or higher |

---

## Legion Relations

### Allied
- Emerald + Paupers (common ground)
- Skeletal + Iron (bureaucratic cooperation)
- Penitent + Silent (emotional support focus)

### Rival
- Skeletal vs Grim (largest Legions, constant competition)
- Iron vs all others (conservative resistance)

### Neutral
- Fate (remains apart from politics)

---

## Reference Data

```bash
# Legion details
python scripts/lookup.py factions.legions legions "Emerald Legion"
python scripts/lookup.py factions.legions legions --keys

# Legion ranks
python scripts/lookup.py factions.hierarchy-ranks hierarchy-ranks --keys
```
