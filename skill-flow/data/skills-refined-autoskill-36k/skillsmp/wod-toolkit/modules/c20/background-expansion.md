# Background Expansion Module

Unified reference for expanding backgrounds into full documents. Used by character creation (Kithain, Kinain), freeholds, and motleys.

## When to Use

This module is referenced by:
- `modules/character.md` — Kithain PC backgrounds
- `modules/kinain.md` — Kinain PC backgrounds
- `modules/freehold.md` — Freehold backgrounds
- `modules/motley.md` — Shared motley resources

**Rule**: PC-level documents always expand backgrounds. NPC/quick builds may skip.

---

## Background → Module Mapping

### Mystical Resources

| Background | Module | Creates | Notes |
|------------|--------|---------|-------|
| **Chimera** | `modules/chimera.md` | Chimera document(s) | Companions or items |
| **Holdings** | `modules/freehold.md` | Freehold document | Includes balefire |
| **Treasure** | `modules/treasure.md` | Treasure document(s) | Crafted or imbued |

### Social Resources

| Background | Module | Creates | Notes |
|------------|--------|---------|-------|
| **Title** | `modules/household.md` | Household + retainer NPCs | Noble rank |
| **Retinue** | Character module (NPC mode) | 1-3 companion NPCs | Servants, guards |
| **Mentor** | Character module (NPC mode) | Mentor NPC | Teacher, guide |
| **Dreamers** | Simple profiles | Mortal Dreamer profiles | Glamour sources |

### Non-Expandable Backgrounds

These backgrounds don't require sub-documents:
- **Contacts** — Described in main document
- **Resources** — Wealth rating only
- **Remembrance** — Past-life memories

---

## Expansion Scale by Rating

### Chimera Background

| Rating | Type | Description |
|--------|------|-------------|
| 1 | Minor companion or item | Small chimerical pet, simple voile item |
| 2 | Useful companion or item | Loyal companion, functional weapon/tool |
| 3 | Significant chimera | Intelligent companion, powerful item |
| 4 | Powerful chimera | Strong companion, legendary item |
| 5 | Legendary chimera | Near-sentient, artifact-level |

**Documents**: 1 chimera document per dot (or combine into single multi-aspect chimera)

### Holdings Background

| Rating | Freehold | Description |
|--------|----------|-------------|
| 1 | Access | Can enter and use a freehold |
| 2 | Resident | Live at freehold, some influence |
| 3 | Significant stake | Partial ownership, key member |
| 4 | Major owner | Primary owner/ruler of freehold |
| 5 | Multiple holdings | Control significant territory |

**Documents**: 1 freehold document (or multiple at rating 5)

### Title Background

| Rating | Rank | Retainers | Description |
|--------|------|-----------|-------------|
| 1 | Squire | 0 | Apprentice noble |
| 2 | Knight | 1 | Landed knight |
| 3 | Baron/Baroness | 1-2 | Minor nobility |
| 4 | Count/Countess | 2-3 | Significant territory |
| 5 | Duke/Duchess+ | 3+ | Major realm ruler |

**Documents**: Household document + retainer NPC documents

### Treasure Background

| Rating | Power Level | Description |
|--------|-------------|-------------|
| 1 | Token | Minor magical trinket |
| 2 | Useful item | Functional magical item |
| 3 | Significant treasure | Powerful, reusable item |
| 4 | Major artifact | Multiple powers or legendary |
| 5 | Legendary relic | Story-defining artifact |

**Documents**: 1 treasure document per significant item

### Retinue Background

| Rating | Followers | Description |
|--------|-----------|-------------|
| 1 | 1 servant | Single loyal helper |
| 2 | 2-3 servants | Small household staff |
| 3 | 5-10 followers | Significant entourage |
| 4 | 20+ followers | Small army |
| 5 | 50+ followers | Major force |

**Documents**: 1-3 representative NPC documents (not every individual)

### Mentor Background

| Rating | Mentor Power | Description |
|--------|--------------|-------------|
| 1 | Competent | Knows basics, limited availability |
| 2 | Skilled | Solid teacher, moderate availability |
| 3 | Expert | Highly skilled, good availability |
| 4 | Master | Exceptional, regular contact |
| 5 | Legend | Among the best, close relationship |

**Documents**: 1 mentor NPC document

### Dreamers Background

| Rating | Dreamers | Glamour/Week |
|--------|----------|--------------|
| 1 | 1 Dreamer | 1 Glamour |
| 2 | 2-3 Dreamers | 2 Glamour |
| 3 | 5+ Dreamers | 3 Glamour |
| 4 | Network | 4 Glamour |
| 5 | Community | 5 Glamour |

**Documents**: Brief profiles in main document (no separate files needed)

---

## Expansion Workflow

### Step 1: Identify Expandable Backgrounds

Review the character/freehold/motley and list all backgrounds from the mapping table above.

### Step 2: Plan Document Structure

```
[project]/
├── [main].md
├── chimera/           ← Chimera backgrounds
├── treasures/         ← Treasure backgrounds
├── companions/        ← Retinue, Mentor
├── freehold/          ← Holdings backgrounds
└── household/         ← Title backgrounds
```

### Step 3: Create in Dependency Order

1. **Treasures first** (no dependencies)
2. **Chimera** (no dependencies)
3. **Freehold** (may contain chimera/treasures)
4. **Household** (may reference freehold)
5. **NPC Companions** (Retinue, Mentor)

### Step 4: Link from Parent Document

```markdown
## Backgrounds

| Background | Rating | Document |
|------------|--------|----------|
| Chimera | ●●●○○ | [Whisperwind](./chimera/whisperwind.md) |
| Holdings | ●●○○○ | [The Hollow Oak](./freehold/hollow_oak.md) |
| Treasure | ●●○○○ | [Moonsilver Blade](./treasures/moonsilver_blade.md) |
| Retinue | ●●○○○ | [Tomás](./companions/tomas.md), [Elara](./companions/elara.md) |
```

---

## Context-Specific Notes

### For Kithain Characters

- **Chimera** companions can be sentient or non-sentient
- **Holdings** typically represents share in a communal freehold
- **Title** requires Noble House affiliation (or exceptional commoner ennoblement)
- Consider creating voile (chimerical clothing) for free—doesn't require Chimera background

### For Kinain Characters

- **Chimera** background is rare (usually requires Fae affinity)
- **Dreamers** background represents Kinain's own Glamour production
- **Mentor** is often a full Kithain relative

### For Freeholds

- All freehold features should be documented regardless of PC status
- **Balefire** rating determines freehold's Glamour production
- Guardian chimera are common and should have documents
- Shared treasures belong to the freehold, not individuals

### For Motleys/Oathcircles

- Shared resources should note proportional ownership
- **Holdings** shared by motley = fractional dots per member
- Oathbonds themselves may need `modules/oath.md` documentation

---

## Validation Checklist

For each expandable background:

- [ ] Correct module was read before creation
- [ ] Document exists at expected path
- [ ] Rating/rank matches background dots
- [ ] All sub-dependencies created
- [ ] Link from parent document is valid
- [ ] Content is thematically consistent with parent

---

## Quick Reference: Module Paths

```bash
# Resources
modules/chimera.md          # Companion/item chimera
modules/treasure.md         # Magical items
modules/freehold.md         # Freeholds and holdings

# Organizations
modules/household.md        # Noble households
modules/motley.md           # Motleys and oathcircles

# Characters
modules/character.md        # Kithain (for NPCs)
modules/kinain.md           # Kinain (for NPC companions)
```
