# Redemption Module

Rules for redeeming Spectres—returning the Shadow-eaten to their state as Restless. Rarer than Transcendence.

## Overview

Redemption is possible but dangerous. It requires:
- A willing Psyche (or one that can be convinced)
- A skilled Pardoner
- Extended, grueling process
- Minimum 7 permanent Pathos in the Spectre

**Warning**: This knowledge is highly restricted. Widespread awareness could destabilize the Shadowlands.

---

## Prerequisites

### Spectre Requirements
| Requirement | Details |
|-------------|---------|
| **Pathos** | 7+ permanent Pathos required |
| **Psyche** | Must be intact (dormant or struggling) |
| **Willing** | Psyche must participate (may need convincing) |

### Redeemable Castes
| Caste | Redeemability |
|-------|---------------|
| **Mortwrights** | Most common candidates; often seek out Redeemers |
| **Doppelgangers** | Second most frequent; infiltration may enable contact |
| **Shades** | Rare; requires exceptional circumstances |
| **Dark Spirits** | Fates of those who try remain unknown |
| **Striplings** | Not yet successfully Redeemed |
| **Indwelling** | Not yet successfully Redeemed |
| **Chosen** | Not yet successfully Redeemed |
| **Nephwracks** | No confirmed Redemptions; theoretical only |

---

## The Five Phases

Each phase lasts at least one chapter. Use of torture increases difficulty of ALL subsequent phases by +1.

### Phase One: Assessment

**Pardoner Actions**:
1. Use **Soulsight** to assess the Spectre
2. Use **Catechize** to question the Psyche

**Rolls**:
- Both parties: Stamina (difficulty 6)
- **Pardoner botch**: +1 difficulty to Castigation for scene/phase
- **Psyche botch**: +1 difficulty to all Psyche rolls for scene/phase

### Phase Two: Initial Purification

**Pardoner Actions**:
1. Use **Soulsight** to assess progress
2. Use **Purify**
3. Optionally use **Trimming the Black Rose** (if known)

**Rolls**:
- Both parties: Stamina (difficulty 6)
- **Pardoner botch**: +1 difficulty to Castigation for scene/phase
- **Psyche botch**: +2 difficulty to all Psyche rolls for scene/phase

### Phase Three: Deepening

**Pardoner Actions**:
1. Use **Purify**
2. Optionally use **Trimming the Black Rose**

**Rolls**:
- Both parties: Stamina (difficulty 7)
- Same botch effects as Phase Two

### Phase Four: Crisis

**Pardoner Actions**:
1. Use **Purify**
2. Optionally use **Trimming the Black Rose**
3. May use **Cooling The Blood** (if known)

**Rolls**:
- Both parties: Stamina (difficulty 7)
- Same botch effects as Phase Two

### Phase Five: Resolution

**Pardoner Actions**:
1. Use **Purify**
2. Optionally use **Trimming the Black Rose**
3. May use **Defiance** and **Purge**

**Rolls**:
- Both parties: Stamina (difficulty 8)
- **Pardoner botch at Castigation ••• or above**: Cannot use Defiance/Purge on this Spectre for months equal to botched dice
- **Psyche**: All rolls +2 difficulty

**Playing With Fire**: May be used at any point in any phase

---

## Resistance

The Spectre may resist throughout the process:

### Phases 1-3
- **Spectre**: Roll Angst (difficulty 6)
- **If successful**: Forces contested Willpower roll (difficulty 6) from Pardoner
- **If either succeeds**: +1 difficulty to Pardoner's Castigation for phase

### Phases 4-5
- **Spectre**: Roll Angst (difficulty 7)
- **Pardoner**: Willpower (difficulty 8)

---

## Assistance from Other Guilds

Other wraiths may assist with applicable Arcanoi. Each assistant can provide **-1 difficulty to one roll** within a single phase (maximum).

### Applicable Arcanoi
| Arcanos | Applicable Levels |
|---------|-------------------|
| Fatalism | •, ••, ••• |
| Intimation | •, ••• |
| Keening | •• |
| Lifeweb | •, ••, ••• |
| Mnemosynis | ••, ••• |
| Pandemonium | •• |
| Usury | •, ••, •••, •••• |

### Exceptional Aid (Requires Storyteller Approval)
| Arcanos | Level | Notes |
|---------|-------|-------|
| Fatalism | ••••• | Breathing the Mists or Ensnare |
| Intimation | •••• | Must be applied carefully |
| Keening | ••••• | Can cause disastrous long-term consequences |
| Mnemosynis | ••••• | |
| Pandemonium | ••••• | |
| Usury | ••••• | |

---

## Organizations

### The Darksiders
Pardoners Guild Doomslayer order specializing in Redemption. Main organized force.

### The Helldivers
Some Doomslayer units engage in Redemption research and operations.

### Illuminate
Secret order pursuing Redemption knowledge.

### The Martyr Knights
Historical Redemption researchers (many early disasters attributed to them).

### The Obliviographic Institute
Academic body studying Oblivion, including Redemption possibilities.

### Legion of Fate
Some agents quietly pursue Redemption research.

---

## Dangers

### Research Disasters
- Empowered Shadows
- Post-traumatic stress
- Freed research subjects
- Total research team casualties

### Process Failures
- Spectre breaks free
- Pardoner consumed
- Psyche destroyed permanently
- Surrounding wraiths endangered

---

## Outcome

**Success**: The Spectre returns to Restless state
- Shadow returns to normal function (antagonist, not dominant)
- Psyche regains control
- May retain memories of Spectral existence
- Often deeply traumatized
- High Angst likely

**Failure**: Various outcomes
- Spectre unchanged
- Spectre more powerful/aggressive
- Pardoner harmed
- All participants Harrowed

---

## Validation

- [ ] Spectre has 7+ permanent Pathos
- [ ] Psyche exists (dormant or struggling)
- [ ] Pardoner has required Castigate levels
- [ ] Each phase lasts at least one chapter
- [ ] Stamina rolls tracked for both parties
- [ ] Resistance rolls tracked
- [ ] Assistance bonuses limited to -1 per phase
- [ ] Torture penalty applied if used (+1 all subsequent phases)

---

## Reference Data

```bash
# Redemption rules
python scripts/lookup.py spectres.redemption redemption "phases"
python scripts/lookup.py spectres.redemption redemption "assistance"

# Castigate Arcanoi
python scripts/lookup.py arcanoi.castigate castigate --keys

# Redemption organizations
python scripts/lookup.py spectres.redemption redemption "organizations"
```
