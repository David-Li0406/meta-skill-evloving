# Background Expansion Module

Unified reference for expanding backgrounds into full documents. Used by character creation (mage/sorcerer), chantries, and horizon realms.

## When to Use

This module is referenced by:
- `modules/character.md` — Mage PC backgrounds
- `modules/sorcerer.md` — Sorcerer PC backgrounds  
- `modules/chantry.md` — Chantry backgrounds
- `modules/horizon-realm.md` — Realm sub-components

**Rule**: PC-level documents always expand backgrounds. NPC/quick builds may skip.

---

## Background → Module Mapping

### Mystical Resources

| Background | Module | Creates | Notes |
|------------|--------|---------|-------|
| **Library** | `modules/library.md` → `grimoire.md` → `rote.md` | Library + 2-4 grimoires + rotes | Full dependency chain |
| **Node** | `modules/node.md` | Node document | Quintessence source |
| **Sanctum** | `modules/sanctum.md` | Sanctum document | Under Prism: grants Practice support |
| **Wonder** | `modules/wonder.md` → `rote.md` | Wonder + effect rotes | Magical items |
| **Chantry** | `modules/chantry.md` | Full chantry package | Invokes many sub-modules |
| **Horizon Realm** | `modules/horizon-realm.md` | Realm + sub-components | May have own nodes/sanctums/libraries |

### Companions & Allies

| Background | Module | Creates | Notes |
|------------|--------|---------|-------|
| **Familiar** | `modules/familiar.md` | Familiar document | Spirit in physical form; mages only |
| **Allies** (mortal) | `modules/human-companion.md` | 1-3 companion NPCs | Acolyte or Consor level |
| **Allies** (supernatural) | Varies by creature type | Ally profile | Werewolf, vampire, etc. |
| **Retainers** | `modules/human-companion.md` | 1-3 companion NPCs | Acolyte level |
| **Cult** | `modules/human-companion.md` | 2-3 representative cultists | Group representation |
| **Spies** | `modules/human-companion.md` | 1-2 key informants | Intelligence network |
| **Backup** | `modules/human-companion.md` | 1-2 support personnel | Technocracy term |
| **Mentor** (significant) | Character module (NPC mode) | Mentor NPC | Optional; for important mentors |

### Sorcerer-Specific

| Background | Module | Creates | Notes |
|------------|--------|---------|-------|
| **Artifact** | `modules/sorcerer-enchantment.md` | Enchanted item | Sorcerers only |

---

## Expansion Scale by Rating

### Companion Backgrounds (Allies, Retainers, Cult, Spies, Backup)

| Rating | Documents to Create | Scope |
|--------|---------------------|-------|
| 1 | 1 representative NPC | Single contact/helper |
| 2 | 1-2 representative NPCs | Small group |
| 3 | 2 representative NPCs | Reliable network |
| 4 | 2-3 representative NPCs | Significant resources |
| 5 | 3 representative NPCs | Extensive network |

**Note**: You don't need to stat every member of a Cult 5—create 2-3 that represent the range (leader, typical member, specialist).

### Library Background

| Rating | Library Rank | Grimoires | Teaching Cap |
|--------|--------------|-----------|--------------|
| 1 | 1 | 2 | 1 |
| 2 | 2 | 2-3 | 2 |
| 3 | 3 | 3-4 | 3 |
| 4 | 4 | 3-4 | 4 |
| 5 | 5 | 4 | 5 |

### Node Background

| Rating | Node Rank | Quintessence/week |
|--------|-----------|-------------------|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |

### Sanctum Background

| Rating | Sanctum Rank | Practices Supported |
|--------|--------------|---------------------|
| 1 | 1 | 1 Practice at rating 1 |
| 2 | 2 | 1 Practice at rating 2 |
| 3 | 3 | 2 Practices at rating 2-3 |
| 4 | 4 | 2-3 Practices at rating 3-4 |
| 5 | 5 | 3+ Practices at rating 4-5 |

### Wonder Background

| Rating | Wonder Power | Typical Items |
|--------|--------------|---------------|
| 1 | Minor charm/gadget | +1 die items, single-use |
| 2 | Useful talisman | Reusable minor effects |
| 3 | Significant artifact | Major single effect |
| 4 | Powerful talisman | Multiple effects or powerful single |
| 5 | Legendary item | Story-defining artifact |

### Familiar Background

**Freebies**: 10 × Background rating

| Rating | Freebies | Bond Level |
|--------|----------|------------|
| 1 | 10 | Emotional sensing |
| 2 | 20 | Limited telepathy |
| 3 | 30 | Full telepathic bond |
| 4 | 40 | Quintessence sharing |
| 5 | 50 | Near-equal partnership |

**Note**: Standalone familiar PCs get 25 freebies regardless of bond level.

---

## Expansion Workflow

### Step 1: Identify Expandable Backgrounds

Review the character/chantry/realm and list all backgrounds from the mapping table above.

### Step 2: Plan Document Structure

```
[project]/
├── [main].md
├── companions/      ← Allies, Retainers, Familiars
├── libraries/       ← Library backgrounds
│   └── grimoires/
├── nodes/           ← Node backgrounds
├── sanctums/        ← Sanctum backgrounds
├── wonders/         ← Wonder backgrounds
│   └── rotes/
└── rotes/           ← Shared rotes
```

### Step 3: Create in Dependency Order

1. **Rotes first** (no dependencies)
2. **Nodes** (no dependencies)
3. **Sanctums** (no dependencies)
4. **Grimoires** (may reference rotes)
5. **Libraries** (reference grimoires)
6. **Wonders** (reference rotes)
7. **Companions** (no dependencies)
8. **Familiars** (no dependencies)

### Step 4: Link from Parent Document

```markdown
## Backgrounds

| Background | Rating | Document |
|------------|--------|----------|
| Library | ●●●○○ | [The Athenaeum](./libraries/athenaeum.md) |
| Node | ●●○○○ | [Ley Line Nexus](./nodes/ley_nexus.md) |
| Allies | ●●●○○ | [Dr. Sarah Chen](./companions/sarah_chen.md), [Marcus Webb](./companions/marcus_webb.md) |
```

---

## Context-Specific Notes

### For Mage Characters

- **Familiar** is available (sorcerers cannot have familiars)
- **Wonder** uses full mage wonder rules with Arete requirements
- Libraries may contain Sphere-teaching grimoires

### For Sorcerer Characters

- **Artifact** replaces Wonder (uses `sorcerer-enchantment.md`)
- **Familiar** is NOT available
- Libraries contain Path/ritual knowledge, not Sphere knowledge
- Consider creating custom rituals for Paths at 3+ (see `sorcerer-ritual.md`)

### For Chantries

- Multiple instances of same background type are common
- Budget system determines total background points
- All backgrounds should be documented regardless of "PC" status
- Members may share access to chantry backgrounds

### For Horizon Realms

- Backgrounds represent realm features, not personal possessions
- Node = Quintessence Wellspring trait
- Sanctum = workspace areas within realm
- Library = knowledge repositories within realm
- Inhabitants (People 2+, Ephemera 3+) also need documentation

---

## Validation Checklist

For each expandable background:

- [ ] Correct module was read before creation
- [ ] Document exists at expected path
- [ ] Rating/rank matches background dots
- [ ] All sub-dependencies created (grimoires for libraries, rotes for wonders)
- [ ] Link from parent document is valid
- [ ] Content is thematically consistent with parent

---

## Quick Reference: Module Paths

```bash
# Mystical resources
modules/library.md      # → grimoire.md → rote.md
modules/node.md
modules/sanctum.md
modules/wonder.md       # → rote.md
modules/chantry.md      # (invokes all above)
modules/horizon-realm.md

# Companions
modules/familiar.md
modules/human-companion.md

# Sorcerer-specific
modules/sorcerer-enchantment.md
modules/sorcerer-alchemy.md
modules/sorcerer-ritual.md
```
