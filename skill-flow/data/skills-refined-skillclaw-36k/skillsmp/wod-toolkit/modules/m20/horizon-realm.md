# Horizon Realm Module

Create Umbral pocket dimensions for M20.

## Dependencies

**Read `modules/background-expansion.md` for sub-component creation.**

May require sub-documents:
- `modules/sanctum.md` — Sanctums within realm
- `modules/library.md` — Libraries within realm  
- `modules/node.md` — Nodes within realm
- `modules/human-companion.md` — Named inhabitants (People 2+)
- `modules/spirit.md` — Named spirits (Ephemera 3+)

## What is a Horizon Realm?

Pocket dimension in the Umbra, created by Spirit 5 mages. Many Chantries use them as bases.

## Rank, Build Points, Maintenance

| Rank | Build Pts | Base Maint (Q/mo) |
|------|-----------|-------------------|
| 1 | 11 | 1 |
| 2 | 22 | 2 |
| 3 | 33 | 3 |
| 4 | 44 | 4 |
| 5 | 55 | 5 |
| 6 | 70 | 10 |
| 7 | 85 | 15 |
| 8 | 100 | 20 |
| 9 | 115 | 25 |
| 10 | 150 | 50 |

Unspent points → +1 Q/mo maintenance each.

## Structure Traits

| Trait | Cost | Scale |
|-------|------|-------|
| **Size** | 5/dot | 1=room, 2=building, 3=grounds, 4=city, 5=country, 6=world |
| **Environment** | 3/dot | 1=connection, 3=any mundane, 6=anything |
| **Access Points** | 2 each | One free. Bypass Avatar Storm |

## Inhabitant Traits

| Trait | Cost | Description |
|-------|------|-------------|
| **Plants** | 2/dot | 0=none → 5=magical |
| **Animals** | 2/dot | 0=none → 5=magical |
| **People** | 5/dot | 0=none → 5=mixed society |
| **Ephemera** | 4/dot | 0=incidental → 5=diverse |

**People 2+**: Name NPCs. **Ephemera 3+**: Name spirits.

## Magick Traits

| Trait | Cost | Effect |
|-------|------|--------|
| **Resonance** | 2/dot | Aligned magic gets bonuses |
| **Focus** | 4/dot | Practice coincidental/vulgar |
| **Spheres** | 6/dot | ±1 to Sphere ratings |
| **Special Phenomena** | 2/rank | Universal effects (max = Realm Rank) |

## Security Traits

| Trait | Cost | Effect |
|-------|------|--------|
| **Guardians** | 3/dot | 10 Freebie Points per dot |
| **Arcane** | 2/dot | Forgettable, destroys records |

## Additional Traits

| Trait | Cost |
|-------|------|
| Gauntlet Modifier | 2 per ±1 |
| Quintessence Wellspring | 10 per Q/mo (max = Rank) |
| Dimensional Locks | 4 each |
| Seasonal Cycle | 2 per season |

## Merits & Flaws

See `references/horizon-realm/merits-flaws.md`.

**Key**: Quintessence Efficient [7] halves maintenance (stackable). Bleeding Out [-7] doubles maintenance.

## Creation Workflow

1. **Rank** — Power level
2. **Creator(s)** — Requires Spirit 5
3. **Purpose** — Base, sanctuary, research, prison
4. **Primary Earthly Connection** — First connection point
5. **Paradigm** — Magical philosophy
6. **Budget** — Plan allocation
7. **Structure** — Size, Environment, Access
8. **Inhabitants** — Plants, Animals, People, Ephemera
9. **Magick** — Resonance, Focus, Spheres, Phenomena
10. **Security** — Guardians, Arcane
11. **Merits/Flaws**
12. **Calculate Costs**
13. **Sub-Components** — Invoke sanctum/library/node modules
14. **History**

## Cost Calculation

```
Used = Traits + Merits - Flaws
Remaining = Build Points - Used
Converted = Remaining (→ Q/mo maintenance)
Final Maintenance = Base + Converted + Modifiers
```

## Validation

- [ ] Costs ≤ build points
- [ ] Maintenance source identified
- [ ] Quintessence Wellspring ≤ Rank
- [ ] Special Phenomena ≤ Rank
- [ ] Environment supports Plant/Animal ratings
- [ ] Size accommodates features
- [ ] People 2+ has NPCs
- [ ] Ephemera 3+ has spirits
- [ ] Sub-components have documents

## Reference Data

```bash
python scripts/lookup.py rules.resonance-traits resonance-traits "Spirit"
python scripts/lookup.py rules.practices practices --keys
```

See also: `references/horizon-realm/advanced-mechanics.md`, `references/horizon-realm/inhabitant-templates.md`

## Return Format

```
Created: ./horizon_realm/silver_garden.md
Name: The Silver Garden
Rank: 5
Maintenance: 8 Q/mo
```
