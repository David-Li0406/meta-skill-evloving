# Weapon Module

Create weapons for World of Darkness games (all lines).

## Weapon Categories

| Category | Examples |
|----------|----------|
| **Melee** | Swords, clubs, knives, axes |
| **Ranged** | Firearms, bows, crossbows |
| **Thrown** | Knives, axes, spears |

## Common Statistics

| Stat | Description |
|------|-------------|
| **Difficulty** | Target number to hit (typically 6) |
| **Damage** | Dice pool for damage |
| **Conceal** | P=Pocket, J=Jacket, T=Trenchcoat, N=None |

## Melee Weapons

### Damage Calculation

Base = Strength + Weapon Modifier

| Size | Modifier | Examples |
|------|----------|----------|
| Tiny | +0 | Brass knuckles |
| Small | +1 | Knife, club |
| Medium | +2 | Sword, machete |
| Large | +3 | Bastard sword |
| Huge | +4 | Claymore, greataxe |

### Damage Type

| Type | Effect |
|------|--------|
| **Bashing (B)** | Halved vs supernatural healing |
| **Lethal (L)** | Standard damage |
| **Aggravated (A)** | Hardest to heal, often supernatural |

### Melee Stats Table

| Weapon | Diff | Damage | Conceal | Notes |
|--------|------|--------|---------|-------|
| Knife | 4 | Str+1 L | P | |
| Club | 5 | Str+2 B | T | |
| Sword | 6 | Str+2 L | T | |
| Bastard Sword | 6 | Str+3 L | N | Two-handed option |
| Stake | 6 | Str+1 L | T | +2 diff vs heart |

## Ranged Weapons

### Firearm Stats

| Stat | Description |
|------|-------------|
| **Damage** | Fixed dice pool |
| **Range** | Short/Medium/Long in yards |
| **Rate** | Shots per turn |
| **Clip** | Magazine capacity |

### Common Firearms

| Weapon | Diff | Damage | Range | Rate | Clip | Conceal |
|--------|------|--------|-------|------|------|---------|
| Light Pistol | 4 | 4 L | 12 | 3 | 10 | P |
| Heavy Pistol | 5 | 5 L | 25 | 3 | 8 | J |
| Shotgun | 6 | 8 L | 20 | 1 | 5 | T |
| Rifle | 8 | 8 L | 200 | 1 | 5 | N |
| SMG | 5 | 4 L | 25 | 3+ | 30 | J |

### Range Modifiers

| Range | Modifier |
|-------|----------|
| Point Blank | -2 diff |
| Short | No modifier |
| Medium | +2 diff |
| Long | +4 diff |

## Thrown Weapons

| Weapon | Diff | Damage | Range | Conceal |
|--------|------|--------|-------|---------|
| Knife | 6 | Str L | Str×3 | P |
| Axe | 7 | Str+2 L | Str×2 | T |
| Spear | 6 | Str+2 L | Str×3 | N |

## Special Properties

| Property | Effect |
|----------|--------|
| **Armor Piercing** | Ignores X armor dice |
| **Incendiary** | Fire damage, may ignite |
| **Silver** | Aggravated vs werewolves |
| **Holy** | Aggravated vs vampires (if blessed) |
| **Cold Iron** | Aggravated vs fae |

## Creation Workflow

1. **Category** — Melee, Ranged, or Thrown
2. **Base Type** — Starting template
3. **Modifications** — Special properties
4. **Balance Check** — Compare to similar weapons
5. **Description** — Appearance, history
6. **Validate**

## Output Format

```markdown
# [Weapon Name]

**Type:** [Category] | **Difficulty:** [N] | **Damage:** [Pool] | **Conceal:** [P/J/T/N]

## Description
[Appearance, construction]

## Statistics

| Stat | Value |
|------|-------|
| Difficulty | [N] |
| Damage | [Pool + Type] |
| Conceal | [Level] |
| [Range/Rate/Clip if ranged] | |

## Special Properties
- [Property 1]

## History/Background
[Origin, significance]

## Game Notes
[Usage tips, special rules]
```

## Validation

- [ ] Difficulty 4-9 (typical range)
- [ ] Damage balanced for type
- [ ] Concealability logical for size
- [ ] Special properties justified
- [ ] Comparable to similar weapons

## Reference

See `references/weapon/output-templates.md` for complete templates by type.
