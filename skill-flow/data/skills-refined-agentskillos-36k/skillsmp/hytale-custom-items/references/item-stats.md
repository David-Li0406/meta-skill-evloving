# Hytale Item Stats Reference

Complete reference for item statistics and properties in the Hytale server.

## Base Item Properties

All items inherit from the base `Item` class:

| Property | Type | Description |
|----------|------|-------------|
| `maxDurability` | Integer | Maximum durability before breaking |
| `durabilityLossOnHit` | Integer | Durability lost when hitting entities |
| `fuelQuality` | Float | Fuel value for furnaces/smelting |
| `maxStack` | Integer | Maximum stack size (default: 64) |
| `itemLevel` | Integer | Required level to use item |
| `qualityId` | String | Reference to ItemQuality asset |
| `consumable` | Boolean | Whether item is consumed on use |
| `variant` | String | Visual variant identifier |

---

## Weapon Stats (ItemWeapon)

| Property | Type | Description |
|----------|------|-------------|
| `StatModifiers` | Map | Stat modifications when equipped |
| `EntityStatsToClear` | List | Stats to clear when equipped |
| `RenderDualWielded` | Boolean | Allow dual-wield rendering |

---

## Armor Stats (ItemArmor)

| Property | Type | Description |
|----------|------|-------------|
| `ArmorSlot` | Enum | Slot: `Head`, `Chest`, `Hands`, `Legs` |
| `DamageResistance` | Map | Resistance by damage type |
| `DamageEnhancement` | Map | Damage bonus by type |
| `DamageClassEnhancement` | Map | Bonus by damage class |
| `KnockbackResistances` | Map | Knockback reduction |
| `KnockbackEnhancements` | Map | Knockback bonus |
| `Regenerating` | Boolean | Auto-regenerates durability |
| `BaseDamageResistance` | Float | Base damage reduction |
| `StatModifiers` | Map | Stat modifications |
| `InteractionModifiers` | Map | Interaction modifications |
| `CosmeticsToHide` | List | Cosmetics hidden when worn |

### Armor Slots

```java
enum ItemArmorSlot {
    Head,   // Helmets, hats
    Chest,  // Chestplates, robes
    Hands,  // Gloves, gauntlets
    Legs    // Leggings, pants
}
```

---

## Tool Stats (ItemTool)

| Property | Type | Description |
|----------|------|-------------|
| `Specs` | List<ItemToolSpec> | Tool specifications |
| `Speed` | Float | Tool use speed |
| `DurabilityLossBlockTypes` | List | Block types that cause durability loss |
| `HitSoundLayer` | String | Sound when hitting |

### Tool Specification (ItemToolSpec)

| Property | Type | Description |
|----------|------|-------------|
| `GatherType` | String | Type of gathering (mining, chopping, etc.) |
| `Power` | Integer | Mining/gathering power level |
| `Quality` | Integer | Quality tier |
| `IsIncorrect` | Boolean | Wrong tool for job flag |

---

## Glider Stats (ItemGlider)

| Property | Type | Description |
|----------|------|-------------|
| `TerminalVelocity` | Float | Maximum fall speed |
| `FallSpeedMultiplier` | Float | Fall speed modifier |
| `HorizontalSpeedMultiplier` | Float | Horizontal glide speed modifier |
| `Speed` | Float | Overall glide speed |

---

## Utility Item Stats (ItemUtility)

| Property | Type | Description |
|----------|------|-------------|
| `Usable` | Boolean | Can be used/activated |
| `Compatible` | List | Compatible item/block types |
| `StatModifiers` | Map | Stat modifications |
| `EntityStatsToClear` | List | Stats to clear on use |

---

## Damage System

### Damage Causes

Asset-based damage cause types:

| Cause | Description |
|-------|-------------|
| `Physical` | Melee combat damage |
| `Projectile` | Ranged projectile damage |
| `Command` | Damage from commands |
| `Drowning` | Water/liquid drowning |
| `Environment` | Environmental hazards |
| `Fall` | Fall damage |
| `OutOfWorld` | Void damage |
| `Suffocation` | Block suffocation |

### Damage Classes

```java
enum DamageClass {
    UNKNOWN,   // Unclassified damage
    LIGHT,     // Light/quick attacks
    CHARGED,   // Charged/heavy attacks
    SIGNATURE  // Signature/special attacks
}
```

### Damage Effects Configuration

| Property | Type | Description |
|----------|------|-------------|
| `ModelParticles` | List | Particles on hit |
| `WorldParticles` | List | World particles on hit |
| `SoundEvents` | List | Sounds on hit |
| `Knockback` | Knockback | Knockback configuration |
| `CameraEffect` | String | Camera shake effect |
| `StaminaDrainMultiplier` | Float | Stamina cost modifier |

### Knockback Configuration

| Property | Type | Description |
|----------|------|-------------|
| `Force` | Float | Knockback strength |
| `Duration` | Float | Knockback duration (seconds) |
| `VelocityType` | Enum | `Add` or `Set` velocity |
| `VelocityConfig` | Object | Velocity parameters |

---

## Modifier System

### Modifier Base

| Property | Type | Description |
|----------|------|-------------|
| `Target` | ModifierTarget | Which value to modify |

### Modifier Targets

```java
enum ModifierTarget {
    Min,  // Modify minimum value
    Max   // Modify maximum value
}
```

### Static Modifier

| Property | Type | Description |
|----------|------|-------------|
| `CalculationType` | Enum | `Additive` or `Multiplicative` |
| `Amount` | Float | Modification amount |

### Calculation Types

```java
enum CalculationType {
    Additive,       // Add to value: value + amount
    Multiplicative  // Multiply value: value * amount
}
```

---

## Entity Stat Types

Entity stats that items can modify:

| Property | Type | Description |
|----------|------|-------------|
| `InitialValue` | Float | Starting value |
| `Min` | Float | Minimum allowed value |
| `Max` | Float | Maximum allowed value |
| `Shared` | Boolean | Shared across instances |
| `Regenerating` | Boolean | Auto-regenerates |
| `MinValueEffects` | List | Effects at minimum |
| `MaxValueEffects` | List | Effects at maximum |
| `ResetType` | Enum | Reset behavior |
| `IgnoreInvulnerability` | Boolean | Bypass invulnerability |

### Reset Behavior

```java
enum EntityStatResetBehavior {
    InitialValue,  // Reset to initial
    MaxValue       // Reset to maximum
}
```

---

## Item Quality Tiers

| Property | Type | Description |
|----------|------|-------------|
| `QualityValue` | Integer | Numeric quality tier |
| `Texture` | String | Quality overlay texture |
| `Color` | Color | Quality color tint |
| `LocalizationKey` | String | Translated name key |

---

## Interaction Types

Items can respond to these interaction types:

| Type | Description |
|------|-------------|
| `Primary` | Left-click action |
| `Secondary` | Right-click action |
| `Ability1-3` | Special ability slots |
| `Use` | General use action |
| `Pick` | Pick up action |
| `Pickup` | Automatic pickup |
| `CollisionEnter` | On collision start |
| `CollisionLeave` | On collision end |
| `Collision` | During collision |
| `EntityStatEffect` | On stat effect trigger |
| `SwapTo` | When switching to item |
| `SwapFrom` | When switching away |
| `Death` | On entity death |
| `Wielding` | While wielding/blocking |
| `ProjectileSpawn` | On projectile creation |
| `ProjectileHit` | On projectile impact |
| `ProjectileMiss` | On projectile miss |
| `ProjectileBounce` | On projectile bounce |
| `Held` | While held in main hand |
| `HeldOffhand` | While in off-hand |
| `Equipped` | While armor equipped |
| `Dodge` | On dodge action |
| `GameModeSwap` | On game mode change |

---

## Pullback Configuration (ItemPullbackConfig)

For bows, crossbows, and charged weapons:

| Property | Type | Description |
|----------|------|-------------|
| `PositionOverrides` | Map | Position adjustments per phase |
| `RotationOverrides` | Map | Rotation adjustments per phase |

---

## Source Files

- `com/hypixel/hytale/server/core/asset/type/item/config/Item.java`
- `com/hypixel/hytale/server/core/asset/type/item/config/ItemWeapon.java`
- `com/hypixel/hytale/server/core/asset/type/item/config/ItemArmor.java`
- `com/hypixel/hytale/server/core/asset/type/item/config/ItemTool.java`
- `com/hypixel/hytale/server/core/asset/type/item/config/ItemToolSpec.java`
- `com/hypixel/hytale/server/core/asset/type/item/config/ItemGlider.java`
- `com/hypixel/hytale/server/core/asset/type/item/config/ItemUtility.java`
- `com/hypixel/hytale/server/core/asset/type/item/config/ItemQuality.java`
- `com/hypixel/hytale/server/core/modules/entity/damage/DamageCause.java`
- `com/hypixel/hytale/server/core/modules/interaction/interaction/config/server/combat/DamageClass.java`
- `com/hypixel/hytale/server/core/modules/entitystats/modifier/Modifier.java`
- `com/hypixel/hytale/server/core/modules/entitystats/modifier/StaticModifier.java`
