# Chantry Module

Create complete M20 chantry packages.

## Dependencies

**Read `modules/background-expansion.md` for the complete background → module mapping and expansion scales.**

```
chantry
├── node (for each Node background)
├── library (for each Library)
│   └── grimoire (2-4 per library)
│       └── rote
├── sanctum (for each Sanctum)
├── horizon-realm (if applicable)
├── wonder (for items)
│   └── rote
└── rote (signature rotes)
```

**Read and invoke each sub-module for its respective backgrounds.**

## What This Creates

1. Main Document — Statistics, links
2. History — Timeline, events
3. Members — Mage profiles
4. Nodes — Via `modules/node.md`
5. Libraries — Via `modules/library.md`
6. Sanctums — Via `modules/sanctum.md`
7. Horizon Realms — Via `modules/horizon-realm.md`
8. Rotes — Via `modules/rote.md`
9. Items — Via `modules/wonder.md`
10. Locations — Important areas

## Rank and Budget

| Points | Rank | Description |
|--------|------|-------------|
| 1-10 | 1 | Small, new |
| 11-20 | 2 | Established |
| 21-30 | 3 | Significant |
| 31-70 | 4 | Major |
| 71+ | 5 | Legendary |

## Background Costs

| Cost/dot | Backgrounds |
|----------|-------------|
| 2 | Allies, Arcane, Library, Retainers |
| 3 | Node, Resources |
| 5 | Sanctum |
| 10 | Horizon Realm |

## Creation Workflow

### Phase 1-2: Planning
1. **Concept** — Faction, budget, purpose, location
2. **Research Faction** — Query titles, practices

### Phase 3: Plan Components
List all backgrounds requiring sub-modules.

### Phase 4-9: ⛔ CREATE SUB-DOCUMENTS (BLOCKING)

**Phase 4: Nodes**
- Read `modules/node.md`
- Create document per Node background
- Save to `./nodes/`

**Phase 5: Libraries**
- Read `modules/library.md` → `modules/grimoire.md` → `modules/rote.md`
- Full dependency chain
- Save to `./libraries/`, `./grimoires/`, `./rotes/`

**Phase 6: Sanctums**
- Read `modules/sanctum.md`
- Under Prism of Focus: Each Sanctum dot grants Practice support
- Sanctum Practices define what's Coincidental within
- Save to `./sanctums/`

**Phase 7: Horizon Realm** (if applicable)
- Read `modules/horizon-realm.md`
- May require its own nodes, libraries, sanctums
- Save to `./horizon_realm/`

**Phase 8: Wonders** (if applicable)
- Read `modules/wonder.md` → `modules/rote.md`
- Save to `./items/`, `./rotes/`

**Phase 9: Signature Rotes**
- Read `modules/rote.md`
- Create wards, communication, rituals
- Save to `./rotes/`

### Phases 10-15: Finalization
10. History Document
11. Member Profiles
12. Location Files
13. Main Document (after all sub-components)
14. Cross-Linking Pass
15. Validation

## File Structure

```
[chantry]/
├── [chantry].md            ← Links to ALL
├── history.md
├── members/
├── nodes/
├── libraries/              ← Links to ../grimoires/
├── grimoires/              ← Links to ../rotes/
├── sanctums/
├── horizon_realm/
├── rotes/
├── items/                  ← Links to ../rotes/
└── locations/
```

## Link Tables (Main Document)

```markdown
## Backgrounds

| Background | Rating | Document |
|------------|--------|----------|
| Node | ●●●○○ | [The Wellspring](./nodes/wellspring.md) |
| Library | ●●●●○ | [The Archive](./libraries/archive.md) |

## Signature Rotes

| Rote | Spheres | Document |
|------|---------|----------|
| [Chantry Ward](./rotes/ward.md) | Prime 3, Forces 2 | Barrier |

## Common Property

| Item | Type | Document |
|------|------|----------|
| [Staff](./items/staff.md) | Talisman 4 | Leadership symbol |
```

## Reference Data

```bash
python scripts/lookup.py rules.faction-chantry-names faction-chantry-names "Order of Hermes"
python scripts/lookup.py rules.faction-titles faction-titles "Verbena"
python scripts/lookup.py rules.faction-practices faction-practices "Virtual Adepts"
```

## Validation

- [ ] All Node backgrounds have documents
- [ ] All Library backgrounds have library + grimoire + rote documents
- [ ] All Sanctum backgrounds have documents
- [ ] Horizon Realm (if any) has document
- [ ] All items have wonder + rote documents
- [ ] All signature rotes have documents
- [ ] All links valid
- [ ] Point budget balanced
