# Background Expansion Module

Unified reference for expanding backgrounds into full documents. Used by wraith character creation and Circle creation.

## When to Use

This module is referenced by:
- `modules/wraith.md` — Wraith PC backgrounds
- `modules/risen.md` — Risen PC backgrounds
- `modules/circle.md` — Shared Circle backgrounds

**Rule**: PC-level documents always expand backgrounds. NPC/quick builds may skip.

---

## Background → Module Mapping

### Mystical Resources

| Background | Module | Creates | Notes |
|------------|--------|---------|-------|
| **Haunt** | `modules/haunt.md` | Haunt document | Personal or shared refuge |
| **Relic** | `modules/relic.md` | Relic document(s) | Ghost of an object |
| **Artifact** | `modules/artifact.md` | Artifact document(s) | Powered ghostly item |

### Companions & Allies

| Background | Module | Creates | Notes |
|------------|--------|---------|-------|
| **Allies** (wraith) | `modules/wraith.md` (NPC mode) | 1-3 ally NPCs | Fellow wraiths |
| **Allies** (mortal) | `modules/ally.md` | 1-3 ally NPCs | Living contacts |
| **Contacts** (important) | `modules/ally.md` | Key contact NPCs | Information sources |
| **Mentor** (significant) | `modules/wraith.md` (NPC mode) | Mentor NPC | For important mentors |

### Social Standing

| Background | Module | Creates | Notes |
|------------|--------|---------|-------|
| **Status** | Note only | Legion rank noted | Hierarchy position |
| **Guild** | Note only | Guild membership noted | Access to Initiate powers |
| **Notoriety** | Note only | Reputation description | Fame among Restless |

### Spiritual Resources

| Background | Module | Creates | Notes |
|------------|--------|---------|-------|
| **Memoriam** | Narrative | Description of who remembers | Affects Pathos |
| **Legacy** | Narrative | Description of lasting works | Healing resource |
| **Eidolon** | Note only | Spiritual strength rating | Resistance to Shadow |

---

## Expansion Scale by Rating

### Companion Backgrounds (Allies, Contacts)

| Rating | Documents to Create | Scope |
|--------|---------------------|-------|
| 1 | 1 representative NPC | Single contact/helper |
| 2 | 1-2 representative NPCs | Small network |
| 3 | 2 representative NPCs | Reliable allies |
| 4 | 2-3 representative NPCs | Significant resources |
| 5 | 3 representative NPCs | Extensive network |

**Note**: Create representative NPCs, not every contact.

### Haunt Background

| Rating | Haunt Size | Shroud Reduction |
|--------|------------|------------------|
| 1 | Small (closet, phone booth) | -1 |
| 2 | Survival-sized room | -2 |
| 3 | Fair-sized, accommodates guests | -3 |
| 4 | Opulent, fits 4 wraiths; OR special (mobile/defended) | -4 |
| 5 | Majestic (haunted mansion) | -5 |

### Relic/Artifact Background

| Rating | Item Power | Typical Items |
|--------|------------|---------------|
| 1 | Minor useful item | Personal effects, simple tools |
| 2 | Useful item | Weapons, valuable objects |
| 3 | Significant item | Important possessions |
| 4 | Powerful item | Major artifacts |
| 5 | Legendary item | Story-defining objects |

### Mentor Background

| Rating | Mentor Status | Connections |
|--------|---------------|-------------|
| 1 | Young mentor, few connections | Basic guidance |
| 2 | Some importance, little power | Limited advocacy |
| 3 | Old and wise, some clout | Moderate influence |
| 4 | Politically powerful | String-pulling ability |
| 5 | Near-omniscient (Ferryman, high Hierarch) | Major influence |

---

## Expansion Workflow

### Step 1: Identify Expandable Backgrounds

Review the character and list all backgrounds from the mapping table above.

### Step 2: Plan Document Structure

```
[character]/
├── [character].md
├── shadow.md           ← ALWAYS required
├── haunts/
├── relics/
├── artifacts/
└── companions/         ← Allies, Mentor
```

### Step 3: Create in Dependency Order

1. **Shadow** (always first for PCs)
2. **Haunts** (no dependencies)
3. **Relics** (no dependencies)
4. **Artifacts** (no dependencies)
5. **Companions** (no dependencies)

### Step 4: Link from Parent Document

```markdown
## Backgrounds

| Background | Rating | Document |
|------------|--------|----------|
| Haunt | ●●●○○ | [The Old Mill](./haunts/old_mill.md) |
| Relic | ●●○○○ | [Father's Watch](./relics/fathers_watch.md) |
| Allies | ●●●○○ | [Marcus Chen](./companions/marcus_chen.md), [Lisa Webb](./companions/lisa_webb.md) |
```

---

## Context-Specific Notes

### For Wraith Characters

- **Shadow** document is ALWAYS required for PCs
- Haunt reduces local Shroud rating
- Relics are ghosts of objects important in life
- Artifacts have special powers

### For Risen Characters

- **Shadow** is dormant but should still be documented
- Haunt less relevant (Risen operate in Skinlands)
- May have living Allies more readily

### For Circles

- Multiple wraiths may share a Haunt
- Backgrounds represent group resources
- Document shared resources separately from personal ones

---

## Validation Checklist

For each expandable background:

- [ ] Correct module was read before creation
- [ ] Document exists at expected path
- [ ] Rating/rank matches background dots
- [ ] Link from parent document is valid
- [ ] Content is thematically consistent with parent

---

## Quick Reference: Module Paths

```bash
# Required
modules/shadow.md           # ALWAYS for PCs

# Mystical resources
modules/haunt.md
modules/relic.md
modules/artifact.md

# Companions
modules/ally.md             # Mortal contacts
modules/wraith.md           # Wraith allies (NPC mode)

# Factions/Organizations
modules/legion.md           # Legion details
modules/guild.md            # Guild details
```
