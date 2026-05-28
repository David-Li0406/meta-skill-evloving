# Faction Module — The Five Factions

Reference for the five philosophical factions of the fallen.

## Overview

Unlike Houses (which are innate), Factions represent ideological allegiances formed during and after the rebellion. A demon chooses their Faction based on their beliefs about the Fall, God, humanity, and the future.

Faction membership is not absolute—demons can hold mixed views or change allegiances.

---

## The Five Factions

### Faustians
**Philosophy**: Humanity is the key to overthrowing God  
**Symbol**: The broken crown  
**Common Houses**: Devils, Defilers, Malefactors

**Core Beliefs**:
- Human faith has power equal to or greater than divine authority
- Humanity can be guided to replace God
- The fallen should shepherd and direct human potential
- Control and manipulation serve the greater good

**Goals**:
- Cultivate human faith and worship
- Build power bases through mortal institutions
- Eventually use collective human will against Heaven
- Establish demon-led order on Earth

**Methods**:
- Create cults and religions
- Infiltrate positions of influence
- Make pacts that serve long-term goals
- Guide rather than dominate (usually)

**Rivals**:
- **Raveners**: Destroying humanity wastes their potential
- **Cryptics**: Too many questions, not enough action

**Stereotypes**:
- Schemers and manipulators
- Long-term planners
- Pragmatic about morality
- Tend toward hubris

**Roleplaying Notes**:
- Always thinking three steps ahead
- View humans as resources (benevolent or not)
- Uncomfortable with chaos and unpredictability
- May genuinely care for "their" humans

---

### Cryptics
**Philosophy**: The truth about God's plan must be discovered  
**Symbol**: The open eye  
**Common Houses**: Fiends, any

**Core Beliefs**:
- God knew about the rebellion and allowed it
- The Fall may have been part of a divine plan
- Understanding the truth is essential before acting
- Questions matter more than answers

**Goals**:
- Discover why God allowed the Fall
- Understand the true nature of Creation
- Find Lucifer and learn what he knows
- Uncover hidden truths about reality

**Methods**:
- Research and investigation
- Debate and philosophical inquiry
- Exploration of the supernatural world
- Careful observation before action

**Rivals**:
- **Faustians**: Acting without understanding is dangerous
- **Raveners**: Destruction eliminates potential answers

**Stereotypes**:
- Philosophers and scholars
- Indecisive (from outside perspective)
- Obsessed with meaning
- Willing to work with any faction temporarily

**Roleplaying Notes**:
- Always asking "why?"
- Fascinated by mysteries and contradictions
- May delay action to gather more information
- Often serve as neutral mediators

---

### Luciferans
**Philosophy**: Find Lucifer and resume the war against Heaven  
**Symbol**: The morning star  
**Common Houses**: Devourers, Devils

**Core Beliefs**:
- Lucifer was right to rebel
- The war is not over, merely paused
- Loyalty to the Morningstar is paramount
- Heaven can still be challenged

**Goals**:
- Locate Lucifer (who escaped the Abyss somehow)
- Rebuild the armies of the rebellion
- Prepare for renewed conflict with Heaven
- Maintain the honor and traditions of the rebellion

**Methods**:
- Military organization and hierarchy
- Seeking signs of Lucifer's presence
- Building demon alliances
- Preserving rebellion-era knowledge

**Rivals**:
- **Reconcilers**: Traitors to the cause
- **Raveners**: Undisciplined and destructive

**Stereotypes**:
- Soldiers and commanders
- Traditionalists
- Honor-bound
- Sometimes blind to changed circumstances

**Roleplaying Notes**:
- Respect hierarchy and chain of command
- Loyal to comrades-in-arms
- May have difficulty adapting to modern world
- Hope sustains them; doubt is weakness

---

### Reconcilers
**Philosophy**: Seek peace with God and redemption  
**Symbol**: The olive branch  
**Common Houses**: Scourges, Slayers

**Core Beliefs**:
- The rebellion was a mistake (or served its purpose)
- Redemption may be possible
- Helping humanity honors the original purpose
- Even eternal punishment can be accepted with grace

**Goals**:
- Make amends for the Fall's consequences
- Protect and aid humanity without manipulation
- Find evidence that reconciliation is possible
- Accept their fate with dignity if redemption is denied

**Methods**:
- Acts of genuine charity and protection
- Avoiding corruption and manipulation
- Seeking signs of divine mercy
- Building genuine (non-exploitative) relationships

**Rivals**:
- **Luciferans**: Still fighting a lost war
- **Raveners**: The opposite of redemption

**Stereotypes**:
- Idealists (or naive, to critics)
- Genuinely helpful
- Sometimes passive or defeatist
- Carry heavy guilt

**Roleplaying Notes**:
- Struggle with Torment more than most
- Genuinely try to do right (as they understand it)
- May be taken advantage of by other factions
- Hope and despair alternate constantly

---

### Raveners
**Philosophy**: Creation is beyond saving and must be destroyed  
**Symbol**: The broken world  
**Common Houses**: Devourers, any (high-Torment)

**Core Beliefs**:
- God has abandoned Creation
- Everything is meaningless
- The only honest response is destruction
- Better oblivion than endless suffering

**Goals**:
- Destroy as much of Creation as possible
- Spread despair and ruin
- Tear down what the other factions build
- Find an end to their own suffering

**Methods**:
- Violence and destruction
- Corruption and temptation to despair
- Sabotage of other factions' plans
- Embracing and spreading Torment

**Rivals**:
- **All other factions**: They all have hope; Raveners don't
- **Faustians** especially: Raveners destroy what Faustians build

**Stereotypes**:
- Nihilists and destroyers
- High-Torment, often monstrous
- Occasionally pitiable
- Dangerous and unpredictable

**Roleplaying Notes**:
- Not necessarily constantly violent (some are coldly methodical)
- May have moments of doubt or regret
- Often once held other beliefs before despair consumed them
- The "villains" of Demon—but understandable ones

---

## Faction Relationships

| Faction | Works With | Opposes |
|---------|------------|---------|
| Faustian | Luciferans (sometimes) | Raveners, Cryptics |
| Cryptic | Any (temporarily) | — (neutral seekers) |
| Luciferan | Faustians (sometimes) | Reconcilers, Raveners |
| Reconciler | Cryptics (seeking answers) | Luciferans, Raveners |
| Ravener | None (or other Raveners) | All |

---

## Changing Factions

Demons can shift factional allegiance through:
- Profound experiences that change their worldview
- Accumulating or shedding Torment
- Discovering information that challenges beliefs
- Influence from other demons or mortals

Faction change should be a significant story event, not a mechanical swap.

---

## Data Lookup

```bash
# Get full Faction details
python scripts/lookup.py d20.character factions "Cryptic"

# Search by philosophy
python scripts/lookup.py d20.character factions --find "redemption"
```

---

## Output Template (Faction Section)

```markdown
## Faction: [Faction Name]

**Philosophy**: [Core belief in one sentence]

**Goals**:
- [Primary goal]
- [Secondary goal]

**Methods**: [How they pursue their goals]

**Faction Weakness**: [How this philosophy can lead them astray]
```
