# Weapon Creation Module

Design mechanically valid weapons for World of Darkness games. These rules apply across all gamelines (V20, W20, M20, Wr20, C20).

## Weapon Types

| Type | Roll | Damage | Special Stats |
|------|------|--------|---------------|
| **Melee** | Dex + Melee | Str + X | — |
| **Ranged** | Dex + Firearms or Athletics* | Fixed or Str + X | Range, Rate, Clip |
| **Thrown** | Dex + Athletics | Str + X | Range = Str × 3/6/9 yards |

*Firearms use Dex + Firearms; muscle-powered (bows, crossbows) use Dex + Athletics

---

## Core Statistics

### Difficulty
Base difficulty is 6, modified by weapon balance/handling.

| Mod | Meaning |
|-----|---------|
| -1 | Easy, well-balanced |
| 0 | Standard |
| +1 | Awkward, requires skill |
| +2 | Very difficult |

### Damage Type

| Code | Type | Examples |
|------|------|----------|
| B | Bashing | Clubs, fists, rubber bullets |
| L | Lethal | Blades, bullets, arrows |
| A | Aggravated | Fire, supernatural (rare) |

### Concealability

| Code | Level | Examples |
|------|-------|----------|
| P | Pocket | Knife, derringer, shuriken |
| J | Jacket | Pistol, stake, throwing axe |
| T | Trenchcoat | Sword, SMG, sawed-off shotgun |
| N | None | Rifle, two-handed sword, spear |

---

## Type-Specific Guidelines

### Melee Weapons

**Damage** (added to Strength):

| Damage | Category | Examples |
|--------|----------|----------|
| +0 | Minimal | Brass knuckles, small improvised |
| +1 | Light | Knife, small club |
| +2 | Medium | Sword, axe, baseball bat |
| +3 | Heavy | Large sword, fire axe |
| +4+ | Exceptional | Two-handed, masterwork |

**Categories**: Light (fast, concealable), Medium (balanced), Heavy (powerful, obvious), Improvised (+1 diff)

### Ranged Weapons

**Firearms** (Dex + Firearms, fixed damage):

| Damage | Examples |
|--------|----------|
| 4 | Light pistol (.22, .25) |
| 5 | Medium pistol (9mm) |
| 6 | Heavy pistol (.45, .357) |
| 7 | Shotgun, SMG |
| 8 | Rifle |
| 9+ | Heavy weapons |

**Bows/Crossbows** (Dex + Athletics):
- Bows: Str +1 to +3 (draw strength matters)
- Crossbows: Fixed damage 5-6 (mechanical draw)

**Range** (yards):

| Range | Examples |
|-------|----------|
| 12-30 | Pistols |
| 40 | SMGs |
| 50 | Shotguns |
| 60-120 | Bows, crossbows |
| 200+ | Rifles |

**Rate** (shots/turn): 1 (bolt/crossbow) to 4+ (full auto)

**Clip**: Ammunition capacity (firearms only)

### Thrown Weapons

**Damage** (added to Strength):

| Damage | Examples |
|--------|----------|
| Str +0 | Stones, darts |
| Str +1 | Throwing knives, shuriken |
| Str +2 | Throwing axes, spears |
| Str +3 | Heavy javelins |

**Range** (based on thrower's Strength):
- Short: Str × 3 yards (no penalty)
- Medium: Str × 6 yards (+1 diff)
- Long: Str × 9 yards (+2 diff)

---

## Supernatural Weapons

### Fetishes (W20)
Werewolf fetishes follow standard weapon stats but may have additional spiritual effects. See `modules/w20/fetish.md`.

### Wonders (M20)
Mage wonders can have custom weapon effects. See `modules/m20/wonder.md`.

### Treasures (C20)
Changeling treasures often have chimerical weapon forms. See `modules/c20/treasure.md`.

### Artifact Weapons (V20)
Vampiric artifact weapons may deal aggravated damage or have blood-related effects.

---

## Creation Workflow

1. **Concept**: What weapon? Make/model or type? Cultural origin?
2. **Type**: Melee, Ranged, or Thrown?
3. **Difficulty**: Based on balance/handling
4. **Damage**: Based on size/caliber/design
5. **Damage Type**: Usually L for blades/bullets, B for blunt
6. **Concealability**: Based on physical size
7. **Type-specific**: Range/Rate/Clip for ranged; range mod for thrown
8. **Supernatural**: Does it have fetish/wonder/treasure properties?
9. **Description**: Appearance, history, combat role

---

## Validation Checklist

- [ ] Damage matches weapon size/caliber
- [ ] Difficulty reflects handling complexity
- [ ] Concealability matches physical dimensions
- [ ] Damage type appropriate (blades=L, blunt=B)
- [ ] Ranged: Range/Rate/Clip realistic for weapon type
- [ ] Thrown: Range modifier noted if non-standard
- [ ] Supernatural effects noted if applicable

---

## Output Format

See `references/weapon-output-templates.md` for detailed templates.

**Quick stat line formats:**

- **Melee**: `Damage: Str +X [L/B] | Diff: 6±X | Conceal: [P/J/T/N]`
- **Ranged**: `Damage: X L | Range: X | Rate: X | Clip: X | Conceal: [P/J/T/N]`
- **Thrown**: `Damage: Str +X [L/B] | Diff: 6±X | Conceal: [P/J/T/N]`
