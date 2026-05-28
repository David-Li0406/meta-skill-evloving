# Background Expansion Module

Automatically expand PC backgrounds into linked documents for rich, detailed characters.

## When to Expand

Expansion is **REQUIRED** for PCs. Skip for NPCs unless specifically requested.

## Background → Module Mapping

| Background | Generates | Module |
|------------|-----------|--------|
| Allies | NPC documents | `character.md` (NPC mode) or `mortal.md` |
| Contacts | Contact network | Brief descriptions |
| Haven | Haven document | `haven.md` |
| Herd | Herd description | Narrative description |
| Mentor | NPC mentor | `character.md` (NPC mode) |
| Resources | Resource details | Narrative description |
| Retainers | Ghoul documents | `ghoul.md` |

---

## Scale Guidelines

### Allies

| Rating | NPCs | Power Level |
|--------|------|-------------|
| 1 | 1 ally | Mortal or weak vampire |
| 2 | 1-2 allies | Competent mortal or neonate |
| 3 | 2-3 allies | Influential mortal or ancilla |
| 4 | 3-4 allies | Powerful mortal or respected vampire |
| 5 | 4-5 allies | Major mortal figure or elder |

### Contacts

| Rating | Scope |
|--------|-------|
| 1 | One major contact in specific field |
| 2 | Small network, 2-3 fields |
| 3 | Moderate network, multiple fields |
| 4 | Extensive network, many fields |
| 5 | Vast network, ears everywhere |

### Haven

| Rating | Security/Comfort |
|--------|------------------|
| 1 | A room, minimal security |
| 2 | An apartment, basic security |
| 3 | A house, good security |
| 4 | Large home/compound, strong security |
| 5 | Fortress, exceptional security |

### Herd

| Rating | Vessels | Notes |
|--------|---------|-------|
| 1 | 3 | +1 die hunting |
| 2 | 7 | +2 dice hunting |
| 3 | 15 | +3 dice hunting |
| 4 | 30 | +4 dice hunting |
| 5 | 60 | +5 dice hunting |

### Mentor

| Rating | Mentor Status |
|--------|---------------|
| 1 | Ancilla, limited influence |
| 2 | Respected elder |
| 3 | Primogen member or equivalent |
| 4 | Prince/Archbishop or equivalent |
| 5 | Justicar/Cardinal or equivalent |

### Resources

| Rating | Wealth Level |
|--------|--------------|
| 1 | Working class, stable |
| 2 | Middle class, some luxuries |
| 3 | Comfortable, significant property |
| 4 | Wealthy, rarely touches cash |
| 5 | Extremely wealthy, vast assets |

### Retainers

| Rating | Retainers |
|--------|-----------|
| 1 | 1 retainer |
| 2 | 2 retainers |
| 3 | 3 retainers |
| 4 | 4 retainers |
| 5 | 5 retainers |

---

## Expansion Process

### Step 1: Identify Expandable Backgrounds

Review the character's backgrounds and flag those requiring documents:
- Any Allies dots → NPC(s)
- Any Haven dots → Haven document
- Any Herd dots → Herd description  
- Any Mentor dots → NPC mentor
- Any Retainers dots → Ghoul(s)

### Step 2: Generate Documents

For each expandable background:

1. **Allies**: Create NPC(s) using `character.md` in NPC mode or `mortal.md`
   - Name, concept, basic stats
   - Relationship to PC
   - What they can provide

2. **Haven**: Create haven using `haven.md`
   - Location and description
   - Security measures
   - Special features

3. **Herd**: Create narrative description
   - Type of herd (club scene, cult, etc.)
   - How PC manages them
   - Potential complications

4. **Mentor**: Create NPC using `character.md` in NPC mode
   - Full vampire statistics
   - Teaching specialties
   - Relationship dynamic
   - What they want from the PC

5. **Retainers**: Create ghouls using `ghoul.md`
   - Full ghoul statistics
   - Role and duties
   - Personality
   - How they became ghouls

### Step 3: Link Documents

Add markdown links in the main character document:

```markdown
## Backgrounds

| Background | Rating | Details |
|------------|--------|---------|
| Allies | ●●○○○ | [Marcus Webb](./npcs/marcus_webb.md) (police detective) |
| Haven | ●●●○○ | [The Foundry](./havens/the_foundry.md) |
| Herd | ●●○○○ | [Club Nocturne Regulars](./herd/club_nocturne.md) |
| Mentor | ●●●○○ | [Elena Vasquez](./npcs/elena_vasquez.md) (Primogen) |
| Retainers | ●○○○○ | [Thomas](./ghouls/thomas.md) |
```

---

## Document Naming Convention

- All lowercase
- Underscores for spaces
- Descriptive names

Examples:
- `marcus_webb.md`
- `the_foundry.md`
- `club_nocturne_herd.md`

---

## Validation Checklist

- [ ] All Allies have NPC documents
- [ ] Haven has detailed document
- [ ] Herd has description
- [ ] Mentor has full NPC document
- [ ] All Retainers have ghoul documents
- [ ] All links are valid
- [ ] Documents match rating power level
