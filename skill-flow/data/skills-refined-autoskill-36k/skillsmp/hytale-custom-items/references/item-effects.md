# Hytale Item Effects Reference

Complete reference for item effects, buffs, and debuffs in the Hytale server.

## Entity Effects

Effects that can be applied to entities through items or combat.

### Effect Properties

| Property | Type | Description |
|----------|------|-------------|
| `duration` | Float | Effect duration in seconds |
| `infinite` | Boolean | Never expires |
| `debuff` | Boolean | Is a negative effect |
| `overlapBehavior` | Enum | How stacking works |
| `damageCalculatorCooldown` | Float | Cooldown between applications |
| `statModifiers` | Map | Stat modifications during effect |
| `valueType` | Enum | How value is applied |

### Overlap Behavior

```java
enum OverlapBehavior {
    Extend,    // Add duration to existing
    Overwrite, // Replace existing effect
    Ignore     // Don't apply if already active
}
```

### Value Type

```java
enum ValueType {
    Percent,   // Percentage-based value
    Absolute   // Fixed numeric value
}
```

---

## Wielding/Blocking Effects

Effects applied while actively wielding (blocking) with an item.

### WieldingInteraction Properties

| Property | Type | Description |
|----------|------|-------------|
| `KnockbackModifiers` | Map | Knockback modifications |
| `DamageModifiers` | Map | Damage modifications |
| `AngledWielding` | Object | Directional block configuration |
| `StaminaCost` | Float | Stamina per second while blocking |
| `BlockedEffects` | List | Effects to block/prevent |

---

## Damage Interaction Effects

Effects that occur on dealing damage.

### DamageEntityInteraction Properties

| Property | Type | Description |
|----------|------|-------------|
| `DamageCalculator` | String | Damage formula reference |
| `AngledDamage` | Object | Directional damage config |
| `TargetedDamage` | Object | Target-specific damage |
| `EntityStatsOnHit` | Map | Stats to apply on hit |

---

## Cosmetic Effects

Visual customization that can be hidden by armor.

### Cosmetic Types

```java
enum Cosmetic {
    Haircut,        // Hair style
    FacialHair,     // Beard/mustache
    Undertop,       // Under-armor top
    Overtop,        // Over-armor top
    Pants,          // Pants/leggings
    Overpants,      // Over-armor pants
    Shoes,          // Footwear
    Gloves,         // Hand coverings
    Cape,           // Back cape
    HeadAccessory,  // Head decorations
    FaceAccessory,  // Face decorations
    EarAccessory,   // Ear decorations
    Ear             // Ear type
}
```

---

## Effect Application

### On-Hit Effects

Items can apply effects when hitting entities:

```json
{
  "EntityStatsOnHit": {
    "Poison": {
      "Duration": 5.0,
      "Amount": 2.0,
      "ValueType": "Absolute"
    }
  }
}
```

### Passive Effects

Items can apply effects while equipped:

```json
{
  "StatModifiers": {
    "Speed": {
      "CalculationType": "Multiplicative",
      "Amount": 1.2,
      "Target": "Max"
    }
  }
}
```

### Consumable Effects

Items can apply effects when consumed:

```json
{
  "Consumable": true,
  "Effects": [
    {
      "Type": "Regeneration",
      "Duration": 10.0,
      "Amount": 1.0
    }
  ]
}
```

---

## Effect Controller Component

Manages active effects on an entity.

### Component Properties

| Property | Type | Description |
|----------|------|-------------|
| `activeEffects` | Map | Currently active effects |
| `pendingEffects` | Queue | Effects waiting to apply |
| `immunities` | Set | Effect types entity is immune to |

### Effect Management

```java
// Apply effect
effectController.apply(effectType, duration, source);

// Remove effect
effectController.remove(effectType);

// Check if effect active
effectController.hasEffect(effectType);

// Get remaining duration
effectController.getRemainingDuration(effectType);
```

---

## Common Effect Types

Based on source analysis, common effect categories include:

### Positive Effects (Buffs)

| Effect | Description |
|--------|-------------|
| `Speed` | Increased movement speed |
| `Strength` | Increased damage |
| `Resistance` | Reduced damage taken |
| `Regeneration` | Health regeneration |
| `JumpBoost` | Higher jumps |
| `NightVision` | See in darkness |
| `WaterBreathing` | Breathe underwater |
| `FireResistance` | Immune to fire damage |
| `Invisibility` | Invisible to entities |
| `Saturation` | Food satisfaction |

### Negative Effects (Debuffs)

| Effect | Description |
|--------|-------------|
| `Slowness` | Reduced movement speed |
| `Weakness` | Reduced damage |
| `Poison` | Damage over time (non-lethal) |
| `Wither` | Damage over time (lethal) |
| `Blindness` | Reduced vision |
| `Nausea` | Screen distortion |
| `Hunger` | Increased hunger drain |
| `MiningFatigue` | Slower mining |
| `Burning` | Fire damage |
| `Bleeding` | Bleed damage over time |

---

## Effect Particles

Visual indicators for active effects.

### ModelParticle Configuration

| Property | Type | Description |
|----------|------|-------------|
| `systemId` | String | ParticleSystem reference |
| `targetEntityPart` | Enum | Body part to attach |
| `targetNodeName` | String | Model bone name |
| `color` | Color | Particle tint |
| `scale` | Float | Size multiplier |
| `positionOffset` | Vector3f | Position adjustment |
| `rotationOffset` | Direction | Rotation adjustment |
| `detachedFromModel` | Boolean | World-space particles |

---

## Effect Sounds

Audio cues for effects.

### SoundEvent Integration

```json
{
  "ApplicationSound": "Effects/Poison_Apply",
  "TickSound": "Effects/Poison_Tick",
  "RemovalSound": "Effects/Poison_Remove"
}
```

---

## Damage Calculation

How damage is calculated with effects.

### Damage Flow

1. Base damage from weapon/attack
2. Apply attacker's damage modifiers (strength, enchants)
3. Apply damage class multipliers
4. Apply target's resistance modifiers (armor, effects)
5. Apply knockback resistance
6. Calculate final damage value

### DamageCalculator Reference

Referenced by name in item configurations:

```json
{
  "DamageCalculator": "Standard_Melee",
  "DamageClass": "LIGHT"
}
```

---

## Effect Immunity

Entities can be immune to certain effects.

### Immunity Sources

- **Entity Type**: Some NPCs immune to certain effects
- **Equipment**: Armor can provide immunity
- **Active Effects**: Some effects grant immunity to others
- **Game Mode**: Creative mode immune to damage effects

---

## Plugin Effect Registration

Creating custom effects in plugins:

```java
// Register custom effect type
@Override
public void onSetup() {
    EntityStatType customEffect = new EntityStatType.Builder("CustomBuff")
        .initialValue(0)
        .max(100)
        .regenerating(false)
        .build();
    
    getAssetRegistry().register(customEffect);
}
```

---

## Source Files

- `com/hypixel/hytale/protocol/EntityEffect.java`
- `com/hypixel/hytale/server/core/entity/EffectControllerComponent.java`
- `com/hypixel/hytale/server/core/modules/interaction/interaction/config/client/WieldingInteraction.java`
- `com/hypixel/hytale/server/core/modules/interaction/interaction/config/server/DamageEntityInteraction.java`
- `com/hypixel/hytale/server/core/modules/interaction/interaction/config/server/combat/DamageEffects.java`
- `com/hypixel/hytale/server/core/asset/type/model/config/ModelParticle.java`
