# Household Module

Create noble households for C20—the retinues, servants, and holdings of titled changelings.

## What is a Household?

A household is the formal retinue of a titled noble—the servants, advisors, champions, and followers bound by Oath of Fealty. It represents political power and social standing.

## Dependencies

```
household
├── character (noble lord/lady)
├── character (retainers, advisors)
├── oath (Oaths of Fealty)
├── freehold (household seat)
└── treasure (household items)
```

**Read and invoke each sub-module for relevant components.**

---

## Title Background Scale

| Dots | Rank | Household Size | Territory |
|------|------|----------------|-----------|
| 1 | Squire | 0 formal retainers | None (serves another) |
| 2 | Knight | 1-3 retainers | Small holding |
| 3 | Baron/Baroness | 5-10 retainers | Barony |
| 4 | Count/Countess | 15-25 retainers | County |
| 5 | Duke/Duchess | 30+ retainers | Duchy |

---

## Creation Workflow

### Phase 1: The Noble

1. **Create noble character** via `modules/character.md`
2. **Confirm Title background** rating
3. **Select Noble House** affiliation
4. **Define territory** (if Baron+)

### Phase 2: Structure

1. **Determine size** from Title rating
2. **Define roles** needed
3. **Plan hierarchy**
4. **Identify key positions**

### Phase 3: ⛔ CREATE RETAINERS (BLOCKING)

For each key retainer:
- Read `modules/character.md` (NPC mode)
- Create character document
- Save to `./retainers/`

### Phase 4: Oaths

Document the Oaths of Fealty:
- Read `modules/oath.md`
- Create oath documents
- Link to retainers

### Phase 5: Holdings

If household has territory:
- Read `modules/freehold.md`
- Create seat of power
- Document other holdings

### Phase 6: Finalization

1. Household treasures
2. Political relationships
3. Main document
4. Cross-linking
5. Validation

---

## Household Roles

### Core Positions

| Role | Responsibility | Typical Kith |
|------|----------------|--------------|
| **Seneschal** | Manages household | Boggan, Sluagh |
| **Champion** | Military leader | Troll, Satyr, Sidhe |
| **Herald** | Messages, protocol | Eshu, Piskie |
| **Bard** | Entertainment, news | Eshu, Satyr |
| **Steward** | Resources, supplies | Boggan, Nocker |
| **Spymaster** | Intelligence | Sluagh, Pooka |
| **Advisor** | Counsel | Sidhe, Eiluned |

### Support Positions

| Role | Responsibility |
|------|----------------|
| Guards | Security |
| Servants | Daily tasks |
| Grooms | Animals, mounts |
| Craftsmen | Repairs, creation |
| Messengers | Communication |

---

## Household by Rank

### Squire (Title 1)
- No formal household
- Serves another noble
- May have 1 personal servant

### Knight (Title 2)
**Retainers**: 1-3
- Personal squire
- 1-2 guards/servants
- Small holding or rooms in lord's freehold

### Baron/Baroness (Title 3)
**Retainers**: 5-10
- Seneschal
- Champion
- 2-3 guards
- 2-3 servants
- Personal freehold (seat)

### Count/Countess (Title 4)
**Retainers**: 15-25
- Full advisory council
- Captain of guards (5-10 guards)
- Household staff (5-10)
- Multiple holdings
- Vassal knights

### Duke/Duchess (Title 5)
**Retainers**: 30+
- Complete court structure
- Military force
- Extensive staff
- Major territory
- Multiple vassal nobles

---

## Household Politics

### Internal Dynamics

| Dynamic | Description |
|---------|-------------|
| Loyal | Retainers devoted to lord |
| Factional | Competing groups within household |
| Ambitious | Some seek to rise |
| Troubled | Dissent or discontent |

### External Relations

| Relation | Description |
|----------|-------------|
| Allied households | Political friends |
| Rival households | Competing nobles |
| Liege | Lord the household serves |
| Vassals | Those who serve the household |

---

## File Structure

```
[household]/
├── [household].md          ← Main document
├── noble/
│   └── [lord_name].md
├── retainers/
│   ├── [retainer1].md
│   └── [retainer2].md
├── oaths/
│   └── fealty_oaths.md
├── holdings/
│   └── [freehold].md
└── treasures/
```

---

## Output Format

```markdown
# House [Name] / The [Name] Household

**Noble**: [Lord/Lady Name]
**House**: [Noble House]
**Rank**: [Title]
**Territory**: [Domain name and location]
**Court**: [Seelie/Unseelie]

## Overview
[Description of this household's character and reputation]

## The Noble

| Attribute | Value |
|-----------|-------|
| Name | [Full name and titles] |
| Kith | [Kith] |
| House | [Noble House] |
| Document | [Link](./noble/name.md) |

## Hierarchy

### Advisory Council
| Position | Name | Kith | Document |
|----------|------|------|----------|
| Seneschal | [Name] | [Kith] | [Link](./retainers/name.md) |
| Champion | [Name] | [Kith] | [Link](./retainers/name.md) |

### Household Staff
| Role | Name/Number | Notes |
|------|-------------|-------|
| Guards | [N] | Led by [Captain] |
| Servants | [N] | Managed by [Head Servant] |

## Oaths of Fealty

| Retainer | Oath Date | Document |
|----------|-----------|----------|
| [Name] | [Date] | [Link](./oaths/fealty_oaths.md) |

## Holdings

| Holding | Type | Document |
|---------|------|----------|
| [Name] | [Seat/Secondary] | [Link](./holdings/name.md) |

## Treasures

| Treasure | Type | Document |
|----------|------|----------|
| [Name] | [Type] | [Link](./treasures/name.md) |

## Territory
[Description of lands, boundaries, notable features]

## Political Situation

### Allies
| House/Noble | Relationship |
|-------------|--------------|
| [Name] | [Nature of alliance] |

### Rivals
| House/Noble | Conflict |
|-------------|----------|
| [Name] | [Source of rivalry] |

### Liege
**[Name and Title]**
[Nature of relationship]

### Vassals
| Noble | Rank | Territory |
|-------|------|-----------|
| [Name] | [Rank] | [Area] |

## History

### Founding
[How the household was established]

### Notable Events
| Date | Event |
|------|-------|
| [When] | [What] |

## Current Situation
[Present-day status, challenges, opportunities]

## Household Culture
[Traditions, customs, expectations]
```

---

## Validation

- [ ] Noble character documented
- [ ] Title rating matches household size
- [ ] Noble House specified
- [ ] All key retainers documented
- [ ] Oaths of Fealty documented
- [ ] Holdings documented (if Baron+)
- [ ] Political relationships noted
- [ ] All links valid

---

## Reference Data

```bash
# Household roles
python scripts/lookup.py rules.household-roles household-roles "Seneschal"

# Title ranks
python scripts/lookup.py rules.noble-ranks noble-ranks --all

# Example households
python scripts/lookup.py freehold.example-households example-households "Gwydion"
```
