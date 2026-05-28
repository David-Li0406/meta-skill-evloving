# Court Module

Create demon organizations and infernal courts.

## Overview

Despite their independence, demons often organize into courts—loose hierarchies based on power, faction, or territory. Courts provide structure for demon society and are the primary political unit in the setting.

---

## Court Types

### Territorial Court
Based on geographic control.
- **Leader**: Tyrant or council
- **Membership**: All demons in territory
- **Purpose**: Mutual defense, resource allocation
- **Stability**: Moderate

### Factional Court
Based on shared ideology.
- **Leader**: Ideological champion
- **Membership**: Those who share beliefs
- **Purpose**: Pursue faction goals
- **Stability**: High (shared purpose)

### House Court
Based on celestial House.
- **Leader**: Eldest or most powerful of House
- **Membership**: Single House only
- **Purpose**: Preserve House traditions
- **Stability**: Low (old rivalries)

### Coalition Court
Mixed membership with specific purpose.
- **Leader**: Negotiated
- **Membership**: Whoever joins
- **Purpose**: Specific goal
- **Stability**: Very Low (dissolves when done)

---

## Court Structure

### Positions

| Position | Role | Power Level |
|----------|------|-------------|
| **Tyrant** | Ruler (often unwilling title) | Highest |
| **Ministers** | Advisors and deputies | High |
| **Barons** | Territory holders | Moderate |
| **Courtiers** | Regular members | Low |
| **Supplicants** | Petitioners, newcomers | None |

### Responsibilities

| Position | Duties |
|----------|--------|
| Tyrant | Final decisions, external relations, arbitration |
| Minister of War | Defense, enforcement, combat |
| Minister of Secrets | Intelligence, counterintelligence |
| Minister of Pacts | Mortal relations, thrall oversight |
| Minister of Whispers | Internal communication, rumors |
| Baron | Manage assigned territory |

---

## Creating a Court

### Step 1: Type and Purpose

What kind of court is this and why does it exist?

| Purpose | Description |
|---------|-------------|
| **Defense** | Mutual protection from threats |
| **Territory** | Control and exploit an area |
| **Ideology** | Pursue faction goals |
| **Revenge** | Target specific enemy |
| **Search** | Find something (Lucifer, artifacts, etc.) |
| **Power** | Accumulate influence |

### Step 2: Membership

Who belongs to this court?

| Factor | Consideration |
|--------|---------------|
| **Houses** | Which Houses represented? |
| **Factions** | Which ideologies? |
| **Size** | How many demons? |
| **Territory** | Geographic scope |
| **Requirements** | What's needed to join? |

### Step 3: Leadership

How is the court ruled?

| Structure | Description |
|-----------|-------------|
| **Autocracy** | Single Tyrant rules |
| **Council** | Group of equals decides |
| **Oligarchy** | Inner circle controls |
| **Democracy** | All members vote (rare) |
| **Anarchy** | No formal structure |

### Step 4: Territory

What does the court control?

| Resource | Examples |
|----------|----------|
| **Physical** | Buildings, neighborhoods, cities |
| **Mortal** | Cults, businesses, institutions |
| **Supernatural** | Haunts, reliquaries, artifacts |
| **Information** | Secrets, histories, True Names |

### Step 5: Relationships

How does this court relate to others?

| Relationship | Description |
|--------------|-------------|
| **Allied** | Mutual support, shared enemies |
| **Neutral** | Formal non-aggression |
| **Rival** | Competition without open war |
| **Enemy** | Active conflict |
| **Vassal** | Subordinate to larger court |
| **Overlord** | Commands smaller courts |

---

## Court Politics

### Power Dynamics

| Source of Power | Description |
|-----------------|-------------|
| **Faith** | More Faith = more influence |
| **Lore** | Knowledge is power |
| **Thralls** | Mortal resources matter |
| **Alliances** | Support from others |
| **Legacy** | Ancient reputation |
| **Fear** | Reputation for violence |

### Common Conflicts

| Conflict Type | Description |
|---------------|-------------|
| **Territory** | Who controls what |
| **Thralls** | Poaching mortals |
| **Ideology** | Factional disagreements |
| **Old Grudges** | Pre-Fall rivalries |
| **Resources** | Artifacts, information |
| **Pride** | Personal insults |

### Resolution Methods

| Method | When Used |
|--------|-----------|
| **Negotiation** | Minor disputes |
| **Arbitration** | Neutral third party |
| **Challenge** | Personal honor matters |
| **Council Vote** | Democratic courts |
| **War** | Irreconcilable differences |

---

## Court Resources

### Common Court Assets

| Resource | Value |
|----------|-------|
| **Haunt** | Central meeting place |
| **Information Network** | Spies and informants |
| **Mortal Influence** | Pull in human society |
| **Supernatural Allies** | Other entities |
| **Artifacts** | Magical items |
| **War Thralls** | Empowered fighters |

### Court Weaknesses

| Vulnerability | Description |
|---------------|-------------|
| **Internal Division** | Factional conflicts |
| **Weak Leader** | Contested authority |
| **External Enemies** | Rivals, hunters |
| **Resource Poor** | Limited Faith sources |
| **Exposed** | Too visible |

---

## Notable Court Archetypes

### The Hidden Kingdom
- Underground, secretive
- Focused on survival
- Minimal mortal contact
- Often Cryptic-dominated

### The Empire
- Large territory
- Many thralls and resources
- Visible (relatively)
- Often Faustian-dominated

### The War Council
- Military structure
- Aggressive expansion
- Focused on conflict
- Often Luciferan-dominated

### The Sanctuary
- Safe haven
- Accepts refugees
- Neutral ground
- Often Reconciler-influenced

### The Ruin
- Ravener-dominated or influenced
- Destructive
- Unstable
- Short-lived

---

## Data Lookup

```bash
# Get court templates
python scripts/lookup.py d20.setting courts "territorial"

# Search by faction
python scripts/lookup.py d20.setting courts --find "Faustian"
```

---

## Output Template

```markdown
# Court: [Court Name]

**Type**: [Territorial/Factional/House/Coalition]
**Territory**: [Geographic area]
**Size**: [Number of demons]
**Founded**: [When]

## Purpose

[Why this court exists]

## Leadership

### [Tyrant Name]
- **House**: [House]
- **Faction**: [Faction]
- **Rule Style**: [How they lead]

### Ministers

| Position | Name | House | Responsibility |
|----------|------|-------|----------------|
| Minister of War | [Name] | [House] | [Duties] |
| Minister of Secrets | [Name] | [House] | [Duties] |
| Minister of Pacts | [Name] | [House] | [Duties] |

## Membership

### By House
| House | Members | Influence |
|-------|---------|-----------|
| Devils | [N] | [Description] |
| ... | | |

### By Faction
| Faction | Members | Influence |
|---------|---------|-----------|
| Faustian | [N] | [Description] |
| ... | | |

### Notable Members
- [Member 1] — [Role/Description]
- [Member 2] — [Role/Description]

## Territory

### Physical Holdings
- [Location 1]
- [Location 2]

### Mortal Resources
- [Resource 1]
- [Resource 2]

### Supernatural Assets
- [Asset 1]
- [Asset 2]

## Laws and Customs

[Court rules and traditions]

## External Relations

### Allies
- [Court/Entity] — [Nature of alliance]

### Rivals
- [Court/Entity] — [Nature of rivalry]

### Enemies
- [Court/Entity] — [Nature of conflict]

## History

[Court's founding and significant events]

## Current Situation

[Present challenges and opportunities]

## Hooks

[Story ideas involving this court]
```
