# Sector Module

Create Digital Web locations for M20.

## What is a Sector?

Virtual spaces in the Umbral realm of data. Virtual Adepts, Iteration X, and tech-savvy mages navigate them.

## Sector Class

| Class | Description |
|-------|-------------|
| **Virgin** | Unexplored raw space |
| **Grid** | Standard navigable |
| **C-Sector** | Corrupted/contested |
| **Corrupted** | Heavily degraded |
| **Junklands** | Abandoned, decaying |
| **Haunts** | Inhabited by entities |
| **Trash** | Deleted but not purged |
| **Streamland** | High data flow |
| **Warzone** | Active conflict |

## Core Statistics

### Access Level

| Level | Description |
|-------|-------------|
| **Free** | Open to all |
| **Restricted** | Requires credentials |

### Security Level (0-10)

| Rating | Security |
|--------|----------|
| 0-2 | Minimal (public) |
| 3-4 | Light (basic) |
| 5-6 | Moderate (commercial) |
| 7-8 | Heavy (corporate/gov) |
| 9-10 | Maximum (black sites) |

### Size Rating (1-6)

| Rating | Scale |
|--------|-------|
| 1 | Room |
| 2 | Building |
| 3 | Block |
| 4 | District |
| 5 | City |
| 6 | Region |

### Power Rating

Paradox threshold—effects below this are coincidental.

## Digital Properties

| Property | Options |
|----------|---------|
| **ARO Density** | None, Sparse, Moderate, Dense, Overwhelming |
| **Data Flow Rate** | Trickle, Steady, High, Torrent |
| **Time Dilation** | < 1.0 slower, 1.0 normal, > 1.0 faster |

## Special Features

| Feature | Description |
|---------|-------------|
| Requires Password | Entry needs code |
| Has Lag | Whiteout risk |
| Temporal Instability | Unpredictable time |
| Is Reformattable | Admin can restructure |

## Reality Zone

Sectors can modify Practice difficulties.

```bash
python scripts/lookup.py rules.practices practices --keys
python scripts/lookup.py rules.reality-zones reality-zones "effects"
```

**Typical Digital Web:**
- Favored: Reality Hacking, Hypertech, Cybernetics
- Hindered: Faith, Witchcraft, Shamanism

## Hazards

See `references/sector/hazards.md` for IC types and dangers.

## Creation Workflow

1. **Concept** — Purpose, controller, atmosphere
2. **Class** — Type of space
3. **Access Level** — Free or Restricted
4. **Security Level** — 0-10
5. **Power Rating** — Paradox threshold
6. **Size** — 1-6
7. **Digital Properties** — ARO, Flow, Time
8. **Special Features**
9. **Reality Zone** — Practice modifiers
10. **Hazards** — IC, entities, environmental
11. **Connections** — Links to other Sectors

## Output Format

```markdown
# [Sector Name]

**Class:** [Type] | **Access:** [Level] | **Security:** [0-10] | **Size:** [1-6]

## Concept
## Statistics

| Stat | Value |
|------|-------|
| Class | [Type] |
| Access | [Level] |
| Security | [0-10] |
| Power Rating | [X] |
| Size | [1-6] |

## Digital Properties

| Property | Value |
|----------|-------|
| ARO Density | [Level] |
| Data Flow | [Rate] |
| Time Dilation | [X.X] |

## Special Features
## Reality Zone
## Hazards
## Connections
## Visual Description
```

## Validation

- [ ] Class matches concept
- [ ] Security matches hazards
- [ ] Access appropriate for type
- [ ] Size fits described scope
- [ ] Reality Zone uses valid Practices
- [ ] Connections noted

## Return Format

```
Created: ./sectors/data_haven.md
Name: The Data Haven
Class: Grid
Security: 7
```
